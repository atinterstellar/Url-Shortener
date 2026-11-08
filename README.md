# Url-Shortener

A small URL shortener built with Flask and SQLite. Paste a long link, get a 6-character short link that redirects to it. Submitting the same URL twice returns the same short code.

<!-- Add a screenshot here: ![Screenshot](docs/screenshot.png) -->

## Features

- Shorten any `http`/`https` URL to a random 6-character code (letters and digits)
- Redirect from the short link to the original URL
- Same URL always maps to the same short code (no duplicate rows)
- Look up the short code for a long URL, and the long URL for a short code
- Input validation: scheme whitelist, length cap, hostname checks, URL normalization

## Tech stack

- Python 3, Flask
- SQLite via the standard library `sqlite3` module (no ORM, plain parameterized SQL)

## Getting started

```bash
git clone https://github.com/atinterstellar/Url-Shortener.git
cd Url-Shortener

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
```

Open http://localhost:5005. The database file `urls.db` is created automatically on first run.

To enable Flask's debug mode while developing, run `FLASK_DEBUG=1 python app.py`. Debug mode is off by default because the Werkzeug debugger allows arbitrary code execution if exposed.

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page |
| `/index` | GET, POST | Form to create a short link |
| `/<code>` | GET | Redirects to the original URL, or 404 |
| `/check-long` | GET, POST | Find the original URL for a short code |
| `/check-short` | GET, POST | Find the short code for an original URL |

## Project structure

```
app.py          Flask routes and URL validation
db.py           SQLite access layer (schema, lookups, inserts)
templates/      HTML templates
requirements.txt
```

## Schema

```sql
CREATE TABLE urls (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url  TEXT NOT NULL UNIQUE,
    short_url TEXT NOT NULL UNIQUE
);
```

## Design decisions

- **`UNIQUE` on both columns.** The database enforces that a long URL has one code and a code maps to one URL, instead of relying only on application-level checks. Collisions and duplicate submissions surface as `IntegrityError`, which can be handled and retried safely.
- **One short-lived connection per operation.** `sqlite3` connections can't be shared across threads, and Flask's development server handles requests in threads, so a single global connection fails under real use.
- **Parameterized queries only.** All SQL uses `?` placeholders. No query is built from user input with string formatting, which prevents SQL injection.
- **Exact-match lookups.** Lookups use `=`, not `LIKE`. `LIKE` treats `%` and `_` as wildcards, and URLs contain both, so it could match the wrong row.
- **URL normalization before storage and lookup.** The input is stripped, `https://` is added if no scheme is given, only `http`/`https` are accepted, and the host is lowercased. This keeps `example.com`, `HTTP://EXAMPLE.COM` and `https://example.com/` from becoming separate entries.
- **Cryptographically random codes.** Codes come from `secrets`, so they can't be predicted or enumerated from earlier ones. With 62 characters and length 6 there are about 56.8 billion possible codes.

## Limitations

- No rate limiting or abuse protection. Anyone who can reach the app can create unlimited links, and open redirects can be misused for phishing. Add rate limiting and a blocklist before exposing it publicly.
- No authentication, link expiry, deletion or click analytics.
- SQLite fits a single-server app. Heavy concurrent writes would need a client/server database such as PostgreSQL.
- The Flask development server is not for production. Use a WSGI server such as gunicorn behind a reverse proxy.

## Possible next steps

- Automated tests (pytest) for the database layer and `normalize_url`
- Custom aliases and link expiry
- Click counts per link
- Deployment (for example Render or Fly.io) with a live demo link
