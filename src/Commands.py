import asyncio
from discord.ext import commands
from src.BaseCog import BaseCog
from src.DB import DB
from src.Reasons import Reasons


class Commands(BaseCog):
    def __init__(self, bot, config):
        super().__init__(bot, config)
        self.reasons = Reasons()

    HELP_MESSAGE = """
    Command: `/kkb <action> [args]`

    All messages sent by the bot will contain a "reddit_id" field.
    Use that ID for all of the below commands.

    Comments will be marked with a White color.
    Posts will be marked with a Blue color.

    Approve/Remove Comment:

        `approvec [comment_id,]`
            e.g. `/kkb approvec 7abc351`
            e.g. `/kkb approvec 7asb472,7bashf2`

        `removec [comment_id,]`

    Approve Posts:

        `approve [post_id,]`

    Remove Posts:

        `remove [post_id,]`

        OR

        `remove [post_id,] reasons [#]`

        e.g. `/kkb remove 7bas4e reasons 2 5 19`

        If the reason requires input from you, include the text after that number

        e.g. `/kkb remove 7bas4e reasons 1 r/kpoppers`

        You can also use the 'custom' reason for freeform response

        e.g. `/kkb remove 7bas4e reasons custom "My custom reason"`

        Make sure to use DOUBLE QUOTES instead of single quotes.

    Get help:

        `/kkb help`

    """

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.channel.send(str(error), delete_after=15)
        await asyncio.sleep(15)
        await ctx.message.delete()

    @commands.command()
    async def help(self, ctx):
        await asyncio.gather(
            ctx.message.delete(),
            ctx.send(self.HELP_MESSAGE, delete_after=30),
        )

    @commands.command()
    async def approvec(self, ctx, comment_id_list):
        comment_ids = comment_id_list.split(",")
        if len(comment_ids) == 0:
            raise ValueError("No comment IDs were given")
        for comment_id in comment_ids:
            await self.reddit.approve_comment(comment_id)
        await asyncio.gather(
            ctx.message.delete(),
            self.delete_message(ctx.channel, comment_id),
        )

    @commands.command()
    async def removec(self, ctx, comment_id_list, *reasons):
        comment_ids = comment_id_list.split(",")
        if len(comment_ids) == 0:
            raise ValueError("No comment IDs were given")
        for comment_id in comment_ids:
            await self.reddit.remove_comment(comment_id)
        await asyncio.gather(
            ctx.message.delete(),
            self.delete_message(ctx.channel, comment_id),
        )

    @commands.command()
    async def approve(self, ctx, post_id_list):
        post_ids = post_id_list.split(",")
        if len(post_ids) == 0:
            raise ValueError("No posts were given")
        for post_id in post_ids:
            is_report = False
            if DB.get().is_post_resolved(post_id):
                is_report = True
            await self.reddit.approve_post(post_id, is_report=is_report)
        await asyncio.gather(
            ctx.message.delete(),
            self.delete_message(ctx.channel, post_id),
        )

    @commands.command()
    async def remove(self, ctx, post_id_list, *reasons):
        post_ids = post_id_list.split(",")
        if len(post_ids) == 0:
            raise ValueError("No posts were given")

        if len(reasons) < 2:
            reasons = []
        else:
            if reasons[0] != "reasons":
                raise ValueError('Invalid command format. Expected "reasons".')
            reasons = reasons[1:]

        if len(reasons) == 0:
            for post_id in post_ids:
                is_report = False
                if DB.get().is_post_resolved(post_id):
                    is_report = True
                await self.reddit.remove_post(post_id, is_report=is_report)
            await ctx.message.delete()
            return

        if len(post_ids) > 1:
            raise ValueError("Reasons are not supported when removing multiple posts")

        post_id = post_ids[0]
        reason_body = self.parse_reasons(reasons)
        submission = await self.reddit.praw().submission(id=post_id)
        header = self.reasons.get_header(submission.author, "post")
        footer = self.reasons.get_footer()
        reason_text = "{}{}{}".format(header, reason_body, footer)

        is_report = False
        if DB.get().is_post_resolved(post_id):
            is_report = True
        await asyncio.gather(
            self.reddit.remove_post(post_id, reason_text, is_report=is_report),
            ctx.message.delete(),
            self.delete_message(ctx.channel, post_id),
        )

    def parse_reasons(self, reason_input):
        # 1 'r/kpoppers' 2 3 6 9 'https://redd.it/7fb1r5' custom 'Custom reason!'

        reason_string = ""

        user_input = False
        for index, reason in enumerate(reason_input):
            if user_input:
                user_input = False
                continue

            if self.reasons.needs_text(reason):
                if len(reason_input) <= index + 1:
                    raise ValueError("Reason {} required text.".format(reason))

                if reason_input[index + 1] == "custom":
                    raise ValueError("Reason {} required text.".format(reason))

                reason_string += (
                    self.reasons.add_reason(reason, reason_input[index + 1]) + "\n\n"
                )
                user_input = True

            else:
                reason_string += self.reasons.add_reason(reason) + "\n\n"

        return reason_string
