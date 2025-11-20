import argparse
import logging
import os
import re
import requests
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Configuration: prefer environment variables, fall back to empty values
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "2ccfa44449a84e21b2a93ae373bd4cc8")
TOPIC = os.getenv("TOPIC", "India Pakistan conflict")
TWILIO_SID = os.getenv("TWILIO_SID", "ACc3450fe281347759d798b77f0e91fbec")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "74e1babcb9c30098266aa9f0f1291f7a")
# Safety toggle: by default do NOT send messages unless SEND_MESSAGES=1 or --send is passed
SEND_MESSAGES = os.getenv("SEND_MESSAGES", "0")


def normalize_whatsapp_number(value: str) -> str:
    """Return a sanitized WhatsApp address in the form 'whatsapp:+<number>'."""
    if not value:
        return value
    # Remove whitespace and common invisible chars
    cleaned = re.sub(r"[\s\u200B\u200C\u200D\uFEFF]+", "", value)
    if not cleaned.startswith("whatsapp:"):
        cleaned = "whatsapp:" + cleaned
    return cleaned


# Defaults (safe canonical form)
FROM_WHATSAPP_NUMBER = normalize_whatsapp_number(os.getenv("FROM_WHATSAPP_NUMBER", "whatsapp:+14155238886"))
TO_WHATSAPP_NUMBER = normalize_whatsapp_number(os.getenv("TO_WHATSAPP_NUMBER", "whatsapp:+919566930488"))


class TwilioClientFactory:
    """Lazy Twilio client factory to avoid failing at import time."""

    def __init__(self, sid: str, token: str):
        self.sid = sid
        self.token = token
        self._client = None

    def get(self):
        if self._client is not None:
            return self._client
        if not (self.sid and self.token):
            logging.warning("Twilio credentials not configured; message sending will be skipped.")
            return None
        try:
            from twilio.rest import Client

            self._client = Client(self.sid, self.token)
            return self._client
        except Exception:
            logging.exception("Failed to create Twilio Client with provided credentials")
            return None


client_factory = TwilioClientFactory(TWILIO_SID, TWILIO_AUTH_TOKEN)


def get_latest_news(topic: str | None = None):
    """Fetch latest news for `topic`. If topic is None, uses the global TOPIC.

    Returns a string (either the formatted news or an error message starting with '⚠').
    """
    q = (topic or TOPIC) if (topic or TOPIC) else ""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": q,
        "language": "en",
        "pageSize": 3,
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        logging.exception("Network error while fetching news")
        return f"⚠ Network error fetching news: {e}"

    if not response.ok:
        logging.error("News API returned non-200 status: %s - %s", response.status_code, response.text[:200])
        return f"⚠ News API error: HTTP {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        logging.error("Failed to parse JSON from News API. Response content: %s", response.text[:400])
        return "⚠ News API returned unexpected response (non-JSON)."

    if data.get("status") == "ok" and data.get("articles"):
        messages = []
        for article in data["articles"][:3]:
            title = article.get("title", "(no title)")
            source = article.get("source", {}).get("name", "Unknown")
            pub_date = article.get("publishedAt", "(no date)")
            link = article.get("url", "(no link)")
            messages.append(f"🗞 {title}\n📍{source} | 🕒 {pub_date}\n🔗 {link}")
        header = f"**Top results for: {q}**\n\n" if q else ""
        return header + "\n\n".join(messages)

    logging.info("News API returned no results or non-ok status: %s", data)
    return "⚠ No news found."


def send_whatsapp_message(message: str, dry_run: bool = False, send_allowed: bool = True) -> bool:
    """Send `message` via Twilio WhatsApp. If `dry_run` is True, log but don't send.

    Returns True if send was attempted or simulated, False on error.
    """
    client = client_factory.get()
    if dry_run:
        logging.info("[dry-run] Message would be sent: %s", message[:200].replace('\n', ' '))
        return True

    if not send_allowed:
        logging.info("Sending disabled (env/CLI). Skipping actual send. Message preview: %s", message[:200].replace('\n', ' '))
        return True

    if client is None:
        logging.error("Twilio client is not configured. Skipping send.")
        return False

    try:
        client.messages.create(
            from_=FROM_WHATSAPP_NUMBER,
            body=message,
            to=TO_WHATSAPP_NUMBER,
        )
        logging.info("Message sent (or request issued) to Twilio")
        return True
    except Exception:
        logging.exception("Failed to send WhatsApp message via Twilio")
        return False


def main():
    parser = argparse.ArgumentParser(description="Fetch news and send via WhatsApp (Twilio)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch news but don't actually send messages")
    parser.add_argument("--send", action="store_true", help="Allow sending messages via Twilio (overrides SEND_MESSAGES env var)")
    parser.add_argument("--once", action="store_true", help="Run a single iteration and exit")
    parser.add_argument("--interval", type=int, default=3600, help="Seconds between polls (default: 3600)")
    parser.add_argument("--news-api-key", type=str, default=None, help="Override NEWS_API_KEY")
    # Accept an optional bare positional API key to avoid errors when user supplies it without the flag
    parser.add_argument("positional_api_key", nargs="?", help="Optional positional NEWS_API_KEY (convenience)")
    parser.add_argument("--twilio-sid", type=str, default=None, help="Override TWILIO_SID")
    parser.add_argument("--twilio-token", type=str, default=None, help="Override TWILIO_AUTH_TOKEN")
    parser.add_argument("--from", dest="from_whatsapp", type=str, default=None, help="Override FROM_WHATSAPP_NUMBER")
    parser.add_argument("--to", dest="to_whatsapp", type=str, default=None, help="Override TO_WHATSAPP_NUMBER")
    parser.add_argument("--topics", type=str, default=None, help="Comma-separated list of topics (e.g. 'sports,gold price,movies')")
    args = parser.parse_args()

    # Allow overrides from CLI
    global NEWS_API_KEY, TWILIO_SID, TWILIO_AUTH_TOKEN, FROM_WHATSAPP_NUMBER, TO_WHATSAPP_NUMBER, client_factory

    # Positional key wins if provided, then explicit flag
    if args.positional_api_key:
        NEWS_API_KEY = args.positional_api_key
    elif args.news_api_key:
        NEWS_API_KEY = args.news_api_key

    if args.twilio_sid:
        TWILIO_SID = args.twilio_sid
    if args.twilio_token:
        TWILIO_AUTH_TOKEN = args.twilio_token

    if args.from_whatsapp:
        FROM_WHATSAPP_NUMBER = normalize_whatsapp_number(args.from_whatsapp)
    if args.to_whatsapp:
        TO_WHATSAPP_NUMBER = normalize_whatsapp_number(args.to_whatsapp)

    # Recreate client factory with possibly-updated credentials
    client_factory = TwilioClientFactory(TWILIO_SID, TWILIO_AUTH_TOKEN)

    if not NEWS_API_KEY:
        logging.warning("NEWS_API_KEY is not set — News requests may fail.")

    # Determine whether sending is allowed (env var or CLI flag)
    send_enabled = args.send or (str(SEND_MESSAGES).lower() in ("1", "true", "yes"))

    def is_error_message(msg: str) -> bool:
        if not msg:
            return True
        return str(msg).lstrip().startswith("⚠")

    # Build topic list: CLI --topics wins, otherwise environment TOPIC (single)
    if args.topics:
        topic_list = [t.strip() for t in args.topics.split(",") if t.strip()]
    else:
        topic_list = [TOPIC] if TOPIC else []

    while True:
        # Fetch news for each requested topic and send each as a separate message
        for t in topic_list:
            news = get_latest_news(topic=t)
            if is_error_message(news):
                logging.warning("Skipping send due to news fetch error for '%s': %s", t, news)
                continue
            send_whatsapp_message(news, dry_run=args.dry_run, send_allowed=send_enabled)

        if args.once:
            break
        time.sleep(max(1, args.interval))


if __name__ == "__main__":
    main()