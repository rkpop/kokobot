from discord import Embed
from discord.ext import commands
from src.Reddit import Reddit


class BaseCog(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.reddit = Reddit(config)

    def create_comment_em(self, submission):
        report_string = ""
        for report in submission.mod_reports:
            report_string += "{}: {}\n".format(report[1], report[0])
        for report in submission.user_reports:
            report_string += "{}: {}\n".format(report[1], report[0])
        em = Embed(
            title="Comment by {}".format(submission.author),
            description="{}\n\n{}".format(submission.body, report_string),
            url="https://reddit.com{}".format(submission.permalink),
            color=0xEEEEEE,
        )
        em.add_field(name="reddit_id", value=submission.id)
        em.set_author(
            name="u/{}".format(submission.author),
            icon_url=self.bot.user.default_avatar_url,
        )
        return em

    def create_post_em(self, submission, reports=False):
        if reports:
            report_string = ""
            for report in submission.mod_reports:
                report_string += "{}: {}\n".format(report[1], report[0])
            for report in submission.user_reports:
                report_string += "{}: {}\n".format(report[1], report[0])
            description = report_string
        else:
            description = ""
        if submission.is_self:
            title_string = "{}".format(submission.title)
        else:
            title_string = "{} ({})".format(submission.title, submission.domain)
        em = Embed(
            title=title_string,
            description=description,
            url="https://redd.it/{}".format(submission.id),
            colour=0x00BCD4,
        )
        if not submission.is_self and hasattr(submission, "preview"):
            em.set_thumbnail(
                url=submission.preview["images"][0]["resolutions"][0]["url"]
            )
        em.add_field(name="reddit_id", value=submission.id)
        em.set_author(
            name="u/{}".format(submission.author),
            icon_url=self.bot.user.default_avatar_url,
        )
        return em

    async def delete_message(self, channel, submission_id):
        async for message in channel.history(limit=200):
            if len(message.embeds) != 1:
                continue
            for field in message.embeds[0].fields:
                if field.name == "reddit_id" and field.value == submission_id:
                    await message.delete()
                    return