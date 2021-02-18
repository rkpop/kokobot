import asyncpraw
from src.DB import DB

class Reddit:

    def __init__(self, config):
        self.reddit = asyncpraw.Reddit(
            client_id=config["Reddit"]["ClientID"],
            client_secret=config["Reddit"]["ClientSecret"],
            password=config["Reddit"]["Password"],
            user_agent="KoKoBot/0.1 by Kilenaitor",
            username=config["Reddit"]["Username"],
        )

    def praw(self):
        return self.reddit

    # Posts
    async def remove_post(self, post_id, reasons=None, is_report=False):
        submission = await self.reddit.submission(id=post_id)
        await submission.mod.remove()
        if reasons is not None:
            reply = await submission.reply(reasons)
            await reply.mod.distinguish()
            await submission.mod.lock()
        if is_report:
            DB.get().mark_report_resolved(post_id)
        else:
            DB.get().mark_post_resolved(post_id)

    async def approve_post(self, post_id, is_report=False):
        submission = await self.reddit.submission(id=post_id)
        await submission.mod.approve()
        if is_report:
            DB.get().mark_report_resolved(post_id)
        else:
            DB.get().mark_post_resolved(post_id)

    # Comments
    async def approve_comment(self, comment_id):
        comment = await self.reddit.comment(id=comment_id)
        await comment.mod.approve()
        DB.get().mark_report_resolved(comment_id)

    async def remove_comment(self, comment_id):
        comment = await self.reddit.comment(id=comment_id)
        await comment.mod.remove()
        DB.get().mark_report_resolved(comment_id)
