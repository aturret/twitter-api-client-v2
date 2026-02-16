from twitter.scraper import Scraper
from twitter.util import find_key


# @elonmusk's "the bird is freed" tweet — a well-known, stable public tweet
TWEET_ID = 1585341984679469056


class TestTweetResultByRestId:
    def test_tweets_by_id_returns_data(self, scraper: Scraper):
        """Test that tweets_by_id returns non-empty results for a valid tweet ID."""
        result = scraper.tweets_by_id([TWEET_ID])
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tweets_by_id_contains_correct_tweet(self, scraper: Scraper):
        """Test that the returned data contains the requested tweet's rest_id."""
        result = scraper.tweets_by_id([TWEET_ID])
        rest_ids = find_key(result, "rest_id")
        assert str(TWEET_ID) in rest_ids

    def test_tweets_by_id_contains_tweet_text(self, scraper: Scraper):
        """Test that the returned tweet contains text content."""
        result = scraper.tweets_by_id([TWEET_ID])
        full_text = find_key(result, "full_text")
        assert len(full_text) > 0
        assert any("bird" in t.lower() for t in full_text if isinstance(t, str))
