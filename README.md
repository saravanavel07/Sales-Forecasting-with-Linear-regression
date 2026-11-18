<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=900&color=F04F4F&center=true&vCenter=true&width=780&lines=Python+News+Alerts;NewsAPI+%E2%86%92+WhatsApp;Automated+updates+with+Twilio" alt="Animated project title" />
</p>

<p align="center">
  <img src="assets/particles.svg" alt="Animated red particles" width="100%" />
</p>

<h1 align="center">News Alerts to WhatsApp</h1>

<p align="center">
  A lightweight Python command-line app that fetches the latest articles for a topic and can deliver them to WhatsApp through Twilio.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/NewsAPI-articles-222222" alt="NewsAPI" />
  <img src="https://img.shields.io/badge/Twilio-WhatsApp-F22F46?logo=twilio&logoColor=white" alt="Twilio WhatsApp" />
  <img src="https://img.shields.io/badge/Interface-CLI-555555" alt="Command-line interface" />
</p>

## What it does

- Fetches up to three recent English articles for a topic from NewsAPI.
- Formats each article with its title, source, publication date, and link.
- Can send the results to a WhatsApp number using Twilio.
- Supports one-time runs, periodic polling, multiple topics, and a dry-run mode.
- Keeps message sending disabled by default unless explicitly enabled.

## Tech stack

| Category | Tools and technologies |
| --- | --- |
| Language | Python |
| APIs / integrations | NewsAPI, Twilio REST API (WhatsApp) |
| Python packages | `requests`; `twilio` for WhatsApp sending |
| Standard library | `argparse`, `logging`, `os`, `re`, `time` |
| Frameworks | No web or application framework; this is a command-line script |

## Get started

Install the dependencies:

```bash
python -m pip install requests twilio
```

Configure credentials as environment variables rather than putting secrets in source code:

```bash
export NEWS_API_KEY="your-newsapi-key"
export TWILIO_SID="your-twilio-account-sid"
export TWILIO_AUTH_TOKEN="your-twilio-auth-token"
export FROM_WHATSAPP_NUMBER="whatsapp:+14155238886"
export TO_WHATSAPP_NUMBER="whatsapp:+your-number"
```

Run once without sending a message:

```bash
python app.py --once --dry-run
```

Fetch and send updates for one or more topics (sending must be explicitly enabled):

```bash
python app.py --topics "technology,markets" --once --send
```

Run continuously, checking every hour by default:

```bash
python app.py --topics "technology,markets" --interval 3600 --send
```

Use `--help` to see all available options. WhatsApp delivery also requires a correctly configured Twilio WhatsApp sender and recipient.

## Configuration

| Variable / option | Purpose |
| --- | --- |
| `NEWS_API_KEY` | NewsAPI key |
| `TOPIC` | Default topic when `--topics` is omitted |
| `TWILIO_SID`, `TWILIO_AUTH_TOKEN` | Twilio credentials |
| `FROM_WHATSAPP_NUMBER`, `TO_WHATSAPP_NUMBER` | WhatsApp sender and recipient addresses |
| `SEND_MESSAGES=1` or `--send` | Explicitly allow sending messages |
| `--dry-run` | Fetch results and log a preview without sending |
| `--once`, `--interval` | Run once or set the polling interval in seconds |

> **Security:** Keep API keys and Twilio credentials private. If credentials have ever been committed to a public repository, revoke and rotate them, then load the replacements from environment variables.

## Project file

- `app.py` — fetches news, formats results, and optionally sends WhatsApp messages.
- `README.md` — project documentation.
- `assets/particles.svg` — animated particle banner used above.

---

<p align="center">Made with Python · NewsAPI · Twilio</p>
