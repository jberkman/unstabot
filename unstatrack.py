#!/usr/bin/env python3
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse
import discord
import discord
import os
import re

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class Matcher:
    def __init__(self, regex, netloc=None, unfurl=True):
        self.pattern = re.compile(regex)
        self.netloc = netloc
        self.unfurl = unfurl

    def match_and_transform(self, message_content):
        match = self.pattern.search(message_content)
        if not match:
            return None
        parsed_url = urlparse(match.group(1))
        netloc = self.netloc if self.netloc else parsed_url.netloc
        url = urlunparse(parsed_url._replace(netloc=netloc, query=''))
        return url if self.unfurl else f'<{url}>'

# List of Matcher instances
matchers = [
    Matcher(r'(https?://(?:www\.)?instagram\.com/[^\s]+)', 'ddinstagram.com'),
    Matcher(r'(https?://(?:www\.)?(twitter|x)\.com/[^\s]+)', 'fixupx.com'),
    Matcher(r'(https?://(?:www\.)?threads\.net/[^\s]+)', unfurl=False),
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
            break  # Exit the loop after the first match

# Run the bot
client.run(TOKEN)
