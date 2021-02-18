import asyncio
from asyncpraw.models import Comment
from discord import utils
from discord.ext import commands
from src.BaseCog import BaseCog
from src.DB import DB


class ReportsStream(BaseCog):
    @commands.Cog.listener()
    async def on_ready(self):
        server = self.bot.get_guild(int(self.config["Discord"]["ServerID"]))
        channel = utils.get(
            server.channels, name=self.config["Discord"]["ReportsChannel"]
        )
        subreddit = await self.reddit.praw().subreddit(
            self.config["Reddit"]["Subreddit"]
        )

        while not self.bot.is_closed():
            async for submission in subreddit.mod.modqueue():
                if not DB.get().is_report_added(submission.id):
                    if isinstance(submission, Comment):
                        em = self.create_comment_em(submission)
                    else:
                        em = self.create_post_em(submission, reports=True)
                    await channel.send(embed=em)
                    DB.get().add_report(submission.id)
                elif DB.get().report_was_resolved(submission.id):
                    if isinstance(submission, Comment):
                        em = self.create_comment_em(submission)
                    else:
                        em = self.create_post_em(submission, reports=True)
                    await channel.send(embed=em)
                    DB.get().unresolve_report(submission.id)
            await asyncio.sleep(10)