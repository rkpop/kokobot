import asyncio
from src.BaseCog import BaseCog
from src.DB import DB
from discord import utils
from discord.ext import commands


class PostsStream(BaseCog):
    @commands.Cog.listener()
    async def on_ready(self):
        server = self.bot.get_guild(int(self.config["Discord"]["ServerID"]))
        channel = utils.get(
            server.channels, name=self.config["Discord"]["PostsChannel"]
        )
        subreddit = await self.reddit.praw().subreddit(
            self.config["Reddit"]["Subreddit"]
        )

        while not self.bot.is_closed():
            async for submission in subreddit.mod.unmoderated():
                if not DB.get().is_post_added(submission.id):
                    em = self.create_post_em(submission)
                    await channel.send(embed=em)
                    DB.get().add_post(submission.id)
            await asyncio.sleep(10)