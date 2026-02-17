import os

import pytest

from twitter.scraper import Scraper


@pytest.fixture(scope="session")
def twitter_cookies() -> dict:
    ct0 = os.environ.get("TWITTER_CT0")
    auth_token = os.environ.get("TWITTER_AUTH_TOKEN")
    if not ct0 or not auth_token:
        pytest.skip("TWITTER_CT0 and TWITTER_AUTH_TOKEN env vars required")
    return {"ct0": ct0, "auth_token": auth_token}


@pytest.fixture(scope="session")
def scraper(twitter_cookies) -> Scraper:
    return Scraper(cookies=twitter_cookies, save=False, pbar=False, debug=0)
