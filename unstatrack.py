import discord
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Regular expression to match Instagram and Twitter URLs
instagram_url_pattern = re.compile(r'(https?://(?:www\.)?instagram\.com/[^\s]+)')
twitter_url_pattern = re.compile(r'(https?://(?:www\.)?(twitter|x)\.com/[^\s]+)')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Search for Instagram URLs in the message
    match = instagram_url_pattern.search(message.content)
    if match:
        url = match.group(1)
        parsed_url = urlparse(url)
        #query_params = parse_qs(parsed_url.query)

        # Check if 'igsh' query parameter exists
        #if 'igsh' in query_params:
        #    # Remove 'igsh' query parameter
        #    query_params.pop('igsh', None)

        #new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(netloc='ddinstagram.com', query=''))

        # Reply with the modified URL
        await message.reply(f'itym {new_url}')

    # Search for Twitter/X URLs in the message
    match = twitter_url_pattern.search(message.content)
    if match:
        url = match.group(1)
        parsed_url = urlparse(url)
        new_url = urlunparse(parsed_url._replace(netloc='fixupx.com', query=''))

        # Reply with the modified URL
        await message.reply(f'itym {new_url}')

# Run the bot with the token from the .env file
client.run(TOKEN)
