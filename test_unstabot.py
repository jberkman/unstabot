import unittest
from urllib.parse import urlparse
from unstabot import Matcher

class TestMatcher(unittest.TestCase):
    def test_instagram(self):
        result = Matcher.INSTAGRAM.match_and_transform('Check this out: https://www.instagram.com/p/xyz123')
        self.assertEqual(result, 'https://ddinstagram.com/p/xyz123')

    def test_twitter(self):
        result = Matcher.TWITTER.match_and_transform('Check this out: https://twitter.com/user/status/123456')
        self.assertEqual(result, 'https://fixupx.com/user/status/123456')

    def test_youtube(self):
        result = Matcher.YOUTUBE.match_and_transform('Check this out: https://www.youtube.com/watch?v=abc123&t=10s')
        self.assertEqual(result, None)

    def test_youtu_be(self):
        result = Matcher.YOUTU_BE.match_and_transform('Check this out: https://youtu.be/abc123?t=10s')
        self.assertEqual(result, None)

    def test_spotify(self):
        result = Matcher.SPOTIFY.match_and_transform('Check this out: https://open.spotify.com/track/xyz123')
        self.assertEqual(result, None)

    def test_reddit(self):
        result = Matcher.REDDIT.match_and_transform('Check this out: https://www.reddit.com/r/test/comments/123456')
        self.assertEqual(result, 'https://old.reddit.com/r/test/comments/123456')

if __name__ == '__main__':
    unittest.main()
