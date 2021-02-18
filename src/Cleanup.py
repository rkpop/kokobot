import asyncio
from src.BaseCog import BaseCog
from src.DB import DB
from discord import utils
from discord.ext import commands


class Cleanup(BaseCog):
    @commands.Cog.listener()
    async def on_ready(self):
        server = self.bot.get_guild(int(self.config["Discord"]["ServerID"]))
        self.reports_channel = utils.get(
            server.channels, name=self.config["Discord"]["ReportsChannel"]
        )
        self.posts_channel = utils.get(
            server.channels, name=self.config["Discord"]["PostsChannel"]
        )
        self.subreddit = await self.reddit.praw().subreddit(
            self.config["Reddit"]["Subreddit"]
        )

        while not self.bot.is_closed():
            await asyncio.gather(
                self.purge_resolved_posts(),
                self.purge_resolved_reports(),
            )
            await asyncio.sleep(300)

    async def purge_resolved_reports(self):
        unresolved_reports = DB.get().get_unresolved_reports()

        current_report_ids = []
        async for submission in self.subreddit.mod.modqueue():
            current_report_ids.append(submission.id)

        resolved_reports = []
        for report in unresolved_reports:
            if report[0] not in current_report_ids:
                resolved_reports.append(report[0])

        messages_to_delete = []
        for report_id in resolved_reports:
            DB.get().mark_report_resolved(report_id)
            messages_to_delete.append(
                self.delete_message(self.reports_channel, report_id)
            )
        await asyncio.gather(*messages_to_delete)

    async def purge_resolved_posts(self):
        unresolved_posts = DB.get().get_unresolved_posts()

        current_unmoderated_ids = []
        async for post in self.subreddit.mod.unmoderated():
            current_unmoderated_ids.append(post.id)

        resolved_posts = []
        for post in unresolved_posts:
            if post[0] not in current_unmoderated_ids:
                resolved_posts.append(post[0])

        messages_to_delete = []
        for post_id in resolved_posts:
            DB.get().mark_post_resolved(post_id)
            messages_to_delete.append(self.delete_message(self.posts_channel, post_id))
        await asyncio.gather(*messages_to_delete)
