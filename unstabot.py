#!/usr/bin/env python3
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import discord
import os
import re

class Matcher:
    INSTAGRAM = None
    TWITTER = None
    THREADS = None
    TIKTOK = None
    YOUTUBE = None
    YOUTU_BE = None
    SPOTIFY = None
    REDDIT = None
    
    def __init__(self, regex, netloc=None, allowlist=None):
        self.pattern = re.compile(regex)
        self.netloc = netloc
        self.allowlist = allowlist if allowlist else []

    def match_and_transform(self, message_content):
        match = self.pattern.search(message_content)
        if not match:
            return None
        old_url = match.group(1)
        parsed_url = urlparse(old_url)
        netloc = self.netloc if self.netloc else parsed_url.netloc
        query_params = {k: v for k, v in parse_qsl(parsed_url.query) if k in self.allowlist}
        new_query = urlencode(query_params)
        new_url = urlunparse(parsed_url._replace(netloc=netloc, query=new_query))
        return new_url if new_url != old_url else None

    @staticmethod
    def get_matchers():
        return [
            Matcher.INSTAGRAM,
            Matcher.TWITTER,
            Matcher.THREADS,
            Matcher.TIKTOK,
            Matcher.YOUTUBE,
            Matcher.YOUTU_BE,
            Matcher.SPOTIFY,
            Matcher.REDDIT,
        ]

Matcher.INSTAGRAM = Matcher(r'(https?://(?:www\.)?instagram\.com/[^\s]+)', 'ddinstagram.com')
Matcher.TWITTER = Matcher(r'(https?://(?:www\.)?(twitter|x)\.com/[^\s]+)', 'fixupx.com')
Matcher.THREADS = Matcher(r'(https?://(?:www\.)?threads\.net/[^\s]+)')
Matcher.TIKTOK = Matcher(r'(https?://(?:www\.)?tiktok\.com/[^\s]+)', 'vxtiktok.com')
Matcher.YOUTUBE = Matcher(r'(https?://(?:www\.|m\.)?youtube\.com/(?:watch|shorts)[^\s]+)', allowlist=['v', 't'])
Matcher.YOUTU_BE = Matcher(r'(https?://youtu\.be/[^\s]+)', allowlist=['v', 't'])
Matcher.SPOTIFY = Matcher(r'(https?://(?:open|play)\.spotify\.com/[^\s]+)')
Matcher.REDDIT = Matcher(r'(https?://(?:www\.|old\.)?reddit\.com/[^\s]+)', 'old.reddit.com')

# Run the bot
if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    # Initialize the bot with the necessary intents
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        # FIXME? This will match the first URL in the message, even if there are multiple URLs
        for matcher in Matcher.get_matchers():
            new_url = matcher.match_and_transform(message.content)
            if new_url:
                await message.reply(f'itym {new_url}')
                # Hide the original unfurl
                await message.edit(suppress=True)
                break  # Exit the loop after the first match

    client.run(TOKEN)
