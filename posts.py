import sqlite3
import asyncio
from client import get_client

conn = sqlite3.connect('kokobot.db')
client = get_client()

class Posts:

    def add_post(self, post_id, message_id, channel_id):
        c = conn.cursor()
        if self.is_post_added(post_id, c):
            raise Exception('Post has already been marked as read.')

        c.execute('INSERT INTO "posts" (message_id, post_id, channel_id) VALUES (?, ?, ?)', (message_id, post_id, channel_id,))
        conn.commit()
        c.close()

    def is_post_added(self, post_id, c=None):
        if c is None:
            c = conn.cursor()
        c.execute('SELECT "message_id" FROM "posts" WHERE "post_id"=?', (post_id,))
        if c.fetchone() is None:
            return False
        return True

    def is_post_resolved(self, post_id, c=None):
        if c is None:
            c = conn.cursor()
        c.execute('SELECT "resolved" FROM "posts" WHERE "post_id"=?', (post_id,))
        result = c.fetchone()
        if result is None:
            return False
        return result[0]

    def is_report_resolved(self, s_id, c=None):
        if c is None:
            c = conn.cursor()
        c.execute('SELECT "resolved" FROM "reports" WHERE "submission_id"=?', (s_id,))
        result = c.fetchone()
        if result is None:
            return False
        return result[0]

    def add_report(self, s_id, message_id, channel_id):
        c = conn.cursor()
        if self.is_report_added(s_id, c):
            raise Exception('Post has already been marked as read.')

        c.execute('INSERT INTO "reports" (message_id, submission_id, channel_id) VALUES (?, ?, ?)', (message_id, s_id, channel_id))
        conn.commit()
        c.close()

    def is_report_added(self, s_id, c=None):
        if c is None:
            c = conn.cursor()
        c.execute('SELECT message_id FROM reports WHERE submission_id=?', (s_id,))
        if c.fetchone() is None:
            return False
        return True

    def report_was_resolved(self, s_id):
        c = conn.cursor()

        c.execute('SELECT submission_id FROM reports WHERE submission_id=? AND resolved=1', (s_id,))
        result = c.fetchone()
        if result is None:
            return False
        return True

    def unresolve_report(self, s_id, message_id, channel_id):
        c = conn.cursor()

        c.execute('UPDATE reports SET resolved=0, message_id=?, channel_id=? WHERE submission_id=?', (message_id, channel_id, s_id,))
        conn.commit()
        c.close()

    async def mark_post_resolved(self, post_id, c=None):
        if c is None:
            c = conn.cursor()
        c.execute('UPDATE posts SET resolved=1 WHERE post_id=?', (post_id,))
        conn.commit()
        c.execute('SELECT message_id, channel_id FROM posts WHERE post_id=?', (post_id,))
        result = c.fetchone()
        if result is None:
            return True
        channel = client.get_channel(str(result[1]))
        if channel is None:
            print('ERROR: could not find channel from result: {}'.format(result))
            return True
        msg = await client.get_message(channel, str(result[0]))
        await client.delete_message(msg)
        if not self.is_report_resolved(post_id):
            await self.mark_report_resolved(post_id, c)

    async def mark_report_resolved(self, s_id, c=None):
        if c is None:
            c = conn.cursor()
        c.execute('UPDATE reports SET resolved=1 WHERE submission_id=?', (s_id,))
        conn.commit()
        c.execute('SELECT message_id, channel_id FROM reports WHERE submission_id=?', (s_id,))
        result = c.fetchone()
        if result is None:
            return True
        channel = client.get_channel(str(result[1]))
        if channel is None:
            print('ERROR: could not find channel from result: {}'.format(result))
            return True
        msg = await client.get_message(channel, str(result[0]))
        await client.delete_message(msg)
        if not self.is_post_resolved(s_id):
            await self.mark_post_resolved(s_id, c)
