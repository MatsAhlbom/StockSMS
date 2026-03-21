# StockSMS

A small Python project for managing stock price alerts.

The project contains:
- a Flask web interface for viewing and updating targets
- a SQLite database for storing targets
- a background worker that checks stock prices and triggers notifications

## Features

- Add, update, remove, and list stock targets from the web UI
- Supports three rule types:
  - `ceiling`
  - `floor`
  - `bb` (Bollinger Band)
- Stores data in SQLite
- Background checker polls prices and marks targets as inactive when triggered
- Optional Discord notification support

## Project structure

```text
.
├── data/
│   └── stocksms.db
├── scripts/
│   ├── __init__.py
│   ├── web_app.py
│   ├── command_handler.py
│   ├── db_handler.py
│   ├── target_handler.py
│   └── discord_notifier.py
├── .env
├── requirements.txt
└── README.md