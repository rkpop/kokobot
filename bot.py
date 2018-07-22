from client import get_client
import configparser
from discord import Embed, utils
import builtins
import asyncio
import reddit
from praw.models import Comment
import posts
import json
import html
import reasons
import parser
import shlex
from urllib.parse import unquote
import sqlite3

client = get_client()
reddit = reddit.Reddit()
praw = reddit.praw()
posts = posts.Posts()
reasons = reasons.Reasons()
parser = parser.CommandParser()
conn = sqlite3.connect('kokobot.db')
config = configparser.ConfigParser()
config.read('config.ini')

help_message = \
'''
Command: `/kkb <action> [args]`

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

    e.g. `/kkb remove 7bas4e reasons 1 'r/kpoppers'`

Get help:

    `/kkb help`

'''

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def create_post_em(submission, reports=False):
    color = 0xFFBD24 if submission.is_self else 0x00BCD4
    if reports:
        report_string = ''
        for report in submission.mod_reports:
            report_string += '{}: {}\n'.format(report[1], report[0])
        for report in submission.user_reports:
            report_string += '{}: {}\n'.format(report[1], report[0])
        description = '{}\n Post ID: {}'.format(report_string, submission.id)
    else:
        description = 'Post ID: {}'.format(submission.id)
    if submission.is_self:
        title_string = '{}'.format(submission.title)
    else:
        title_string = '{} ({})'.format(submission.title, submission.domain)
    em = Embed(
        title=title_string,
        description=description,
        url='https://redd.it/{}'.format(submission.id),
        colour=color
    )
    if not submission.is_self and hasattr(submission, 'preview'):
        em.set_thumbnail(
            url=submission.preview['images'][0]['resolutions'][0]['url']
        )
    em.set_author(
        name='u/{}'.format(submission.author),
        icon_url=client.user.default_avatar_url
    )
    return em

def create_comment_em(submission):
    report_string = ''
    for report in submission.mod_reports:
        report_string += '{}: {}\n'.format(report[1], report[0])
    for report in submission.user_reports:
        report_string += '{}: {}\n'.format(report[1], report[0])
    em = Embed(
        title='Comment: {}'.format(submission.id),
        description='{}\n{}'.format(submission.body, report_string),
        url='https://reddit.com{}'.format(submission.permalink),
    )
    em.set_author(
        name='u/{}'.format(submission.author),
        icon_url=client.user.default_avatar_url
    )
    return em

async def stream_sub():
    await client.wait_until_ready()
    server = client.get_server(config['Discord']['ServerID'])
    channel = utils.get(server.channels, name=config['Discord']['PostsChannel'])
    subreddit = praw.subreddit('kpop')

    while not client.is_closed:
        for submission in subreddit.mod.unmoderated():
            if not posts.is_post_added(submission.id):
                em = create_post_em(submission)
                sent_message = await client.send_message(channel, embed=em)
                posts.add_post(submission.id, sent_message.id, channel.id)
        await asyncio.sleep(10)

async def stream_reports():
    await client.wait_until_ready()
    server = client.get_server(config['Discord']['ServerID'])
    channel = utils.get(server.channels, name=config['Discord']['ReportsChannel'])
    subreddit = praw.subreddit('kpop')

    while not client.is_closed:
        for submission in subreddit.mod.modqueue():
            if not posts.is_report_added(submission.id):
                if isinstance(submission, Comment):
                    em = create_comment_em(submission)
                else:
                    em = create_post_em(submission, reports=True)
                sent_message = await client.send_message(channel, embed=em)
                posts.add_report(submission.id, sent_message.id, channel.id)
            if posts.report_was_resolved(submission.id):
                if isinstance(submission, Comment):
                    em = create_comment_em(submission)
                else:
                    em = create_post_em(submission, reports=True)
                sent_message = await client.send_message(channel, embed=em)
                posts.unresolve_report(submission.id, sent_message.id, channel.id)
        await asyncio.sleep(10)

async def purge_channels():
    await client.wait_until_ready()
    subreddit = praw.subreddit('kpop')

    while not client.is_closed:
        c = conn.cursor()

        # Purge resolved reports
        report_ids = []
        for submission in subreddit.mod.modqueue():
            report_ids.append(submission.id)

        c.execute('SELECT submission_id FROM reports WHERE resolved=0')
        unresolved_reports = c.fetchall()

        resolved_reports = []
        for report in unresolved_reports:
            if report[0] not in report_ids:
                resolved_reports.append(report[0])

        for report_id in resolved_reports:
            await posts.mark_report_resolved(report_id)

        # Purge resolved posts
        unmoderated_ids = []
        for post in subreddit.mod.unmoderated():
            unmoderated_ids.append(post.id)

        c.execute('SELECT post_id FROM posts WHERE resolved=0')
        unresolved_posts = c.fetchall()

        resolved_posts = []
        for post in unresolved_posts:
            if post[0] not in unmoderated_ids:
                resolved_posts.append(post[0])

        for post_id in resolved_posts:
            await posts.mark_post_resolved(post_id)
        c.close()
        await asyncio.sleep(300)


async def parse_command(message):
    cmd_args = shlex.split(message.content)

    cmd_args.pop(0)

    if len(cmd_args) == 1 and cmd_args[0] == 'help':
        await client.send_message(message.channel, help_message)
        return True

    try:
        await parser.parse_commands(cmd_args)
        return True
    except ValueError as ve:
        result = ve
        await client.send_message(message.channel, result)
        return False


@client.event
async def on_message(message):
    if message.content.startswith('/kkb'):
        success = await parse_command(message)
        if success:
            await client.delete_message(message)

client.loop.create_task(stream_sub())
client.loop.create_task(stream_reports())
client.loop.create_task(purge_channels())
client.run(config['Discord']['Token'])
