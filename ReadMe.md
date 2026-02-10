# pass-gen

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) ![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
## Deployment


[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/KarimBesserSchool/pass-gen/tree/main)

----
A small, self-contained Flask service and simple UI for generating secure random passwords and checking password strength. Designed to be easy to run locally or host behind a lightweight web server.

Table of contents
- [What this project does](#what-this-project-does)
- [Why it's useful](#why-its-useful)
- [Features](#features)
- [Quick start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Run (development)](#run-development)
  - [Run (production with gevent)](#run-production-with-gevent)
  - [Notes about launch.py](#notes-about-launchpy)
- [Configuration / Environment variables](#configuration--environment-variables)
- [HTTP API](#http-api)
  - [Generate password](#generate-password)
  - [Check password strength](#check-password-strength)
- [Authentication & rate limiting](#authentication--rate-limiting)
- [Where to get help](#where-to-get-help)
- [Maintainers & contributing](#maintainers--contributing)
- [License](#license)

## What this project does

pass-gen provides:
- A REST API to generate secure random passwords.
- An endpoint to evaluate password strength against a small ruleset (length, character classes, and sequence checks).
- A minimal static UI (prev.html) that can be served from the root endpoint.

The main application entry point is `main.py` which runs a Flask app exposing the endpoints described below.

## Why it's useful

- Quickly generate passwords that include lower/upper/digits/symbols and avoid simple sequences.
- Quickly check whether a password meets basic strength expectations.
- Small, portable codebase suitable for local use, demos, or as a microservice in a larger toolkit.

## Features

- /api/generate_password?n=NUM → deterministic-length password generator (min 8, max 64)
- /api/check_password → password strength checking with JSON response (ok, score, req)
- Optional API key protection and rate limiting via environment variables
- Lightweight, few dependencies: Flask (+ python-dotenv for local envs), optional gevent for production

## Quick start

### Prerequisites

- Python 3.8+
- pip

### Install

1. Clone the repository
   - git clone https://github.com/KarimBesserSchool/pass-gen
   - cd pass-gen

2. Create and activate a virtual environment (recommended)
   - python -m venv .venv
   - source .venv/bin/activate  (Linux / macOS)
   - .venv\Scripts\activate     (Windows PowerShell)

3. Install dependencies
   - pip install Flask python-dotenv
   - Optional (production gevent server): pip install gevent

> Note: There is no requirements.txt in the repository. The above lists the libraries used by the project.

### Run (development)

Start the app with default development settings:

```bash
python main.py
```

By default the app listens on port 5000. Open http://127.0.0.1:5000/ to view the UI (`prev.html`) or use the API endpoints below.

### Run (production with gevent)

Set environment variable `STAGE=PROD` (and optionally `PORT`) and run:

```bash
export STAGE=PROD
export PORT=8000
python main.py
```

When `STAGE` is `PROD`, the app uses gevent's WSGI server (install gevent as noted above).

### Notes about launch.py

There is a `launch.py` which attempts to run `api.py` and open `prev.html` in a browser. The current API server file is `main.py`. Prefer running `main.py` directly — `launch.py` appears to be an older helper script and may reference a non-existent `api.py`.

## Configuration / Environment variables

The app is configured via environment variables (and optionally a `.env` file when using python-dotenv):

- API_KEY — (optional) when set, API endpoints under `/api/` require the header `X-API-Key: <API_KEY>`.
- RATELIMIT — (optional) number of requests allowed per WINDOW per key/ip (defaults to 80).
- STAGE — set to `PROD` to use the gevent WSGI server; defaults to `DEV` (Flask dev server).
- PORT — port to bind (default 5000).

Example `.env`:

```
API_KEY=replace-me
RATELIMIT=100
STAGE=DEV
PORT=5000
```

## HTTP API

All API endpoints are under `/api/`. Responses are JSON.

### Generate password

GET /api/generate_password?n=NUM

- n (optional): desired password length (int). The server enforces 8 ≤ n ≤ 64. Default: 12.

Example:

```bash
curl "http://127.0.0.1:5000/api/generate_password?n=16"
# Response:
# {"password":"aB3$..."}
```

### Check password strength

POST /api/check_password

Accepts JSON or form-encoded data. Returns JSON describing whether the password is acceptable, a numeric score, and the requirements object.

Example (JSON):

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"password":"MyP@ssw0rd123"}' \
  http://127.0.0.1:5000/api/check_password

# Example response:
# {
#   "ok": true,
#   "score": 4,
#   "req": {
#     "len": true,
#     "lower": true,
#     "upper": true,
#     "digit": true,
#     "sym": true,
#     "seq": true
#   }
# }
```

## Authentication & rate limiting

- When `API_KEY` is set, API requests must include header: `X-API-Key: <API_KEY>`.
- Rate limiting is enforced per API key or per client IP (when API key not present) using a sliding window.
- Responses include these headers when applicable:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `Retry-After` (when rate limited)

If an invalid API key is provided, the API will return HTTP 401 with a JSON error.

## Where to get help

- Raise an issue in this repository's Issues tracker.
- For urgent local problems, inspect logs printed to the console when running `main.py`.
- The code is small and commented; check `main.py` and `auth.py` for implementation details.

## Maintainers & contributing

Maintainer: KarimBesserSchool (see repository owner)

If you'd like to contribute, please:
- Open an issue to discuss larger changes before implementation.
- Submit clear, focused pull requests.
- Add tests where applicable and keep changes small and well-documented.

See CONTRIBUTING.md for more detail (create one in the repo root) or open an issue to start a discussion.

## License

This project is released under the MIT License — see the LICENSE file.
