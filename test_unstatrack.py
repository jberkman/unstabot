import unittest
from urllib.parse import urlparse
from unstatrack import Matcher

# Define global matchers
instagram_matcher = Matcher(r'(https?://(?:www\.)?instagram\.com/[^\s]+)', 'ddinstagram.com')
twitter_matcher = Matcher(r'(https?://(?:www\.)?(twitter|x)\.com/[^\s]+)', 'fixupx.com')
youtube_matcher = Matcher(r'(https?://(?:www\.|m\.)?youtube\.com/(?:watch|shorts)[^\s]+)', allowlist=['v', 't'])
youtu_be_matcher = Matcher(r'(https?://youtu\.be/[^\s]+)', allowlist=['v', 't'])
spotify_matcher = Matcher(r'(https?://(?:open|play)\.spotify\.com/[^\s]+)')
reddit_matcher = Matcher(r'(https?://(?:www\.|old\.)?reddit\.com/[^\s]+)', 'old.reddit.com')

class TestMatcher(unittest.TestCase):
    def test_instagram(self):
        result = instagram_matcher.match_and_transform('Check this out: https://www.instagram.com/p/xyz123')
        self.assertEqual(result, 'https://ddinstagram.com/p/xyz123')

    def test_twitter(self):
        result = twitter_matcher.match_and_transform('Check this out: https://twitter.com/user/status/123456')
        self.assertEqual(result, 'https://fixupx.com/user/status/123456')

    def test_youtube(self):
        result = youtube_matcher.match_and_transform('Check this out: https://www.youtube.com/watch?v=abc123&t=10s')
        self.assertEqual(result, None)

    def test_youtu_be(self):
        result = youtu_be_matcher.match_and_transform('Check this out: https://youtu.be/abc123?t=10s')
        self.assertEqual(result, None)

    def test_spotify(self):
        result = spotify_matcher.match_and_transform('Check this out: https://open.spotify.com/track/xyz123')
        self.assertEqual(result, None)

    def test_reddit(self):
        result = reddit_matcher.match_and_transform('Check this out: https://www.reddit.com/r/test/comments/123456')
        self.assertEqual(result, 'https://old.reddit.com/r/test/comments/123456')

if __name__ == '__main__':
    unittest.main()