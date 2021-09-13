import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

def main():
    # connect
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # set up command prefix and enable slash commands
    client = commands.Bot(command_prefix='.')
    slash = SlashCommand(client, sync_commands = True, sync_on_cog_reload = True)

    client.load_extension("cogs.lookUp")
    client.run(TOKEN)

if __name__ == "__main__":
    main()
