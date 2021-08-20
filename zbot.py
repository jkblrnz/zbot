import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

def main():
    # connect
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = commands.Bot(command_prefix='!')
    client.load_extension("cogs.lookUp")
    client.run(TOKEN)

if __name__ == "__main__":
    main()
