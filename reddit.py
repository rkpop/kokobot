import praw
import asyncio
import sqlite3
import posts
import configparser

posts = posts.Posts()
conn = sqlite3.connect('kokobot.db')
config = configparser.ConfigParser()
config.read('config.ini');

class Reddit:

    reddit = praw.Reddit(client_id=config['Reddit']['ClientID'],
                         client_secret=config['Reddit']['ClientSecret'],
                         password=config['Reddit']['Password'],
                         user_agent='KoKoBot/0.1 by Kilenaitor',
                         username=config['Reddit']['Username'])
    def praw(self):
        return self.reddit

    # Posts
    async def remove_post(self, post_id, reasons=None, is_report=False):
        try:
            submission = self.reddit.submission(id=post_id)
            submission.mod.remove()
        except Exception as e:
            raise ValueError(str(e))
        if reasons is not None:
            submission.reply(reasons).mod.distinguish()
            submission.mod.lock()
        if is_report:
            response = await posts.mark_report_resolved(post_id)
        else:
            response = await posts.mark_post_resolved(post_id)
        return response

    async def approve_post(self, post_id, is_report=False):
        try:
            submission = self.reddit.submission(id=post_id)
            submission.mod.approve()
        except Exception as e:
            raise ValueError(str(e))
        if is_report:
            response = await posts.mark_report_resolved(post_id)
        else:
            response = await posts.mark_post_resolved(post_id)
        return response

    # Comments
    async def approve_comment(self, comment_id):
        try:
            comment = self.reddit.comment(id=comment_id)
            comment.mod.approve()
        except Exception as e:
            raise ValueError(str(e))
        response = await posts.mark_report_resolved(comment_id)
        return response

    async def remove_comment(self, comment_id):
        try:
            comment = self.reddit.comment(id=comment_id)
            comment.mod.remove()
        except Exception as e:
            raise ValueError(str(e))
        response = await posts.mark_report_resolved(comment_id)
        return response

