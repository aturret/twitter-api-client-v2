# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python client library for X/Twitter v1, v2, and GraphQL APIs. Supports authentication, automation (tweeting, DMs, follows), scraping (users, tweets, media), search with pagination, and Twitter Spaces (live audio/transcripts).

## Build & Install

```bash
# Install from source (development)
pip install -e .

# Install from PyPI
pip install twitter-api-client-v2 -U

# Build and publish (maintainer)
python -m build && python -m twine upload dist/*
```

There is also a `setup.py` maintained as a fallback for legacy tools.

**Python:** >=3.10.10 (setup.py fallback), >=3.12 (pyproject.toml primary)

## Testing

No formal test suite exists. Validation is done via `examples/example.ipynb` and `examples/simple_example.py` against live Twitter APIs.

## Architecture

Four core modules in `twitter/`, each handling a distinct concern:

- **`account.py`** — Authenticated write operations (Account class): tweet, DM, follow, like, media upload, profile updates, list management. Uses `gql()` for GraphQL mutations and `v1()` for REST endpoints.
- **`scraper.py`** — Read-only data collection (Scraper class): user/tweet fetching, timelines, followers, media downloads, Spaces audio/transcripts, trends. Heavily async with batch support.
- **`search.py`** — Search with auto-pagination (Search class): queries by category (Top/Latest/People/Photos/Videos), cursor-based pagination, retry with backoff.
- **`login.py`** — Authentication flows: credential-based login, guest token init, 2FA handling, optional Proton Mail email verification.

Supporting modules:

- **`util.py`** — Shared helpers: `init_session()` (guest sessions), `find_key()` (recursive JSON key search), `batch_ids()`, `get_cursor()`, header/cookie management.
- **`constants.py`** — 330+ GraphQL operation definitions as `Operation.<name> = (variables, query_id, op_name)` tuples, media size limits, logging config, user agents.

## Key Patterns

**Authentication:** Three methods — credentials (email/username/password), cookie dict (`ct0` + `auth_token`), or cookie JSON file. All constructors (Account, Scraper, Search) accept the same auth args.

**GraphQL Operations:** Defined in `constants.py` as `Operation` dataclass fields. Each is a tuple of `(default_variables_dict, query_id_string, operation_name_string)`. The `gql()` and `v1()` methods on Account/Scraper dispatch requests using these tuples.

**Async patterns:** Core I/O uses `httpx.AsyncClient`. Public methods call `asyncio.run()` internally so callers use sync APIs. `nest_asyncio` patches the event loop for Jupyter compatibility. `uvloop` is used on non-Windows platforms.

**Batch endpoints:** `tweets_by_ids` and `users_by_ids` handle ~220 items per request with higher rate limits. Always prefer these over single-item variants. `batch_ids()` in util.py splits ID lists to avoid 431 errors.

**Response handling:** Twitter GraphQL responses are deeply nested. `find_key(obj, key)` recursively extracts values by key name from arbitrary nesting depths.

**Rate limits:** Tracked per-operation in the `rate_limits` dict attribute on Account. Keys are real GraphQL operation names.

## Updating GraphQL Operations

`scripts/update.py` is a discovery script that scrapes Twitter's JS bundles to extract current GraphQL query IDs and operations. Run it when Twitter updates their API to refresh `constants.py`.
