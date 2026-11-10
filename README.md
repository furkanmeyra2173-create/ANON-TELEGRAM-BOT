# ANON H4X Telegram Bot

A multilingual Telegram bot foundation for the ANON H4X project.

## Included in this first version

- First-use language selection: Turkish, Kurdish (Kurmanji), English, Arabic, French, German, Hindi, Chinese, Japanese and Korean.
- Saved language preference in SQLite.
- Localized main menu, language change and help commands.
- Admin-only panel and `/stats` command.
- Initial SQLite tables for users, wallet credits and memberships.
- AI, premium and payment buttons are placeholders until their providers and rules are configured; no fake AI replies or payments are performed.

## Run locally

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

Set environment variables (never commit the real token):

- `BOT_TOKEN`: token from @BotFather.
- `ADMIN_IDS`: comma-separated numeric Telegram user IDs allowed to use admin commands.
- `DATABASE_PATH`: optional SQLite file path.

Then run:

```bash
python bot.py
```

For GitHub Actions or a hosting provider, add `BOT_TOKEN` and `ADMIN_IDS` as encrypted secrets/environment variables. A GitHub repository alone does not keep a bot online; it needs a running host or a properly configured worker.

## Security

Do not publish your BotFather token. If it is exposed, revoke it with @BotFather and generate a new one. Never place secrets in source code or commit history.
