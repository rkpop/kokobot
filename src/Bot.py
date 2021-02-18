import configparser
from discord.ext import commands
import os
from src.Cleanup import Cleanup
from src.Commands import Commands
from src.PostsStream import PostsStream
from src.ReportsStream import ReportsStream


class Bot:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.environ.get("CONFIG_PATH"))
        self.config = config

        bot = commands.Bot(command_prefix="/kkb ", help_command=None)

        bot.add_cog(Cleanup(bot, config))
        bot.add_cog(Commands(bot, config))
        bot.add_cog(PostsStream(bot, config))
        bot.add_cog(ReportsStream(bot, config))

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("------")

    def run(self):
        self.bot.run(self.config["Discord"]["Token"])
