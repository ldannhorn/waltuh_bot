import asyncio
import discord
from discord.ext import commands
from discord.guild import Guild
from discord.user import ClientUser
from discord.member import Member
from discord.permissions import Permissions
from discord.channel import TextChannel
from random import choice
from pathlib import Path
from typing import Any
import json


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='waltuh ', intents=intents, help_command=None)


@bot.event
async def on_ready():
    print('Logged in.')

    # Sync slash commands
    #await bot.tree.sync()

    # Load texts
    content_file_path = Path(__file__).parent / 'res' / 'messages.json'
    with open(content_file_path, 'r', encoding='utf-8') as f:
        content: dict[str,Any] = json.load(f)

    # Get bot user
    user: (ClientUser | None) = bot.user
    if user is None: return
    user_id: int = user.id

    # Iterate guilds
    for guild in bot.guilds:
        # Get guild
        g: (Guild | None) = bot.get_guild(guild.id)
        if g is None: continue

        # Get bot member
        member: (Member | None) = g.get_member(user_id)
        if member is None: continue

        # Find channels with send perms
        candidates: list[TextChannel] = [ch for ch in g.text_channels if ch.permissions_for(member).send_messages]

        # Choose random channel
        channel = choice(candidates)

        # Send random message
        message: str = choice(content.get('rand_daily', ['waltuh ist kaputt :c']))
        print(message)
        await channel.send(message)
        




async def main():
    with open('token.json', 'r', encoding='utf-8') as f:
        token = json.load(f)['token']

    async with bot:
        await bot.start(token)

        

      

if __name__ == '__main__':
    asyncio.run(main())