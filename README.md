Market Data API
=====================================

<URL>

How does this work?
----------------

Market Data API retrieves data from Redis Server to parse to user of API. Data from Redis is constantly populated by Market Data Poller from multiple exchanges.

Application Flow
-------

Client UI <-> Market Data API <-> Redis Server <-> Market Data Poller


Available End points
-------
- GET  /v1/markets?pairs=<pairs>&base_currency=<base_currency>

ENV parameters
-------
Available at ./instructions/env.md

## Instructions

To run in development mode:

```bash
$ source venv/bin/activate
$ python ./src/main.py
```

To run in production mode:

```bash
$ nohup gunicorn3 -b 127.0.0.1:8000 src.wsgi:app &
```
