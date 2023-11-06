import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os
import logging
from amogus_server_bot.rolebot_cog import Rolebot

load_dotenv()

logging.basicConfig(level=logging.INFO)


GUILD_ID = os.getenv("GUILD_ID")

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


bot.add_cog(Rolebot(bot))
bot.run(os.getenv("TOKEN"))
