#!/usr/bin/env python3
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import discord
import os
import re

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Initialize the bot with the necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

class Matcher:
    def __init__(self, regex, netloc=None, allowlist=None):
        self.pattern = re.compile(regex)
        self.netloc = netloc
        self.allowlist = allowlist if allowlist else []

    def match_and_transform(self, message_content):
        match = self.pattern.search(message_content)
        if not match:
            return None
        parsed_url = urlparse(match.group(1))
        query_params = {k: v for k, v in parse_qsl(parsed_url.query) if k in self.allowlist}
        new_query = urlencode(query_params)
        return urlunparse(parsed_url._replace(netloc=self.netloc, query=new_query))

# List of Matcher instances
matchers = [
    Matcher(r'(https?://(?:www\.)?instagram\.com/[^\s]+)', 'ddinstagram.com'),
    Matcher(r'(https?://(?:www\.)?(twitter|x)\.com/[^\s]+)', 'fixupx.com'),
    Matcher(r'(https?://(?:www\.)?threads\.net/[^\s]+)', 'threads.net'),
    Matcher(r'(https?://(?:www\.)?tiktok\.com/[^\s]+)', 'vxtiktok.com'),
    Matcher(r'(https?://(?:www\.|m\.)?youtube\.com/watch[^\s]+)', 'youtube.com', allowlist=['v', 't']),
    Matcher(r'(https?://youtu\.be/[^\s]+)', 'youtu.be', allowlist=['v', 't']),
]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # FIXME? This will match the first URL in the message, even if there are multiple URLs
    for matcher in matchers:
        new_url = matcher.match_and_transform(message.content)
        if new_url:
            await message.reply(f'itym {new_url}')
            # Hide the original unfurl
            await message.edit(suppress=True)
            break  # Exit the loop after the first match

# Run the bot
client.run(TOKEN)
