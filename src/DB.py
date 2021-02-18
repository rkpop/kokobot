import os
import sqlite3


class DB:

    __instance = None
    __instantiation_key = "THIS_IS_TO_STUPIDLY_ENFORCE_SINGLETON_IN_PYTHON"

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = DB(instantiation_key=DB.__instantiation_key)
        return cls.__instance

    def __init__(self, instantiation_key=None):
        assert (
            instantiation_key == DB.__instantiation_key
        ), "Use the DB.get() method to connect to the database"
        self.conn = sqlite3.connect(os.environ.get("DB_PATH"))

    def add_post(self, post_id):
        c = self.conn.cursor()
        if self.is_post_added(post_id, c):
            raise Exception("Post has already been marked as read.")

        c.execute(
            'INSERT INTO "posts" (post_id) VALUES (?)',
            (post_id,),
        )
        self.conn.commit()
        c.close()

    def is_post_added(self, post_id, c=None):
        if c is None:
            c = self.conn.cursor()
        c.execute('SELECT rowid FROM "posts" WHERE "post_id"=?', (post_id,))
        return c.fetchone() is not None

    def is_post_resolved(self, post_id, c=None):
        if c is None:
            c = self.conn.cursor()
        c.execute('SELECT rowid FROM "posts" WHERE "post_id"=? AND resolved=1', (post_id,))
        result = c.fetchone()
        return result is not None

    def is_report_resolved(self, s_id, c=None):
        if c is None:
            c = self.conn.cursor()
        c.execute('SELECT rowid FROM "reports" WHERE "submission_id"=? AND resolved=1', (s_id,))
        result = c.fetchone()
        return result is not None

    def add_report(self, submission_id):
        c = self.conn.cursor()
        if self.is_report_added(submission_id, c):
            raise Exception("Post has already been marked as read.")

        c.execute(
            'INSERT INTO "reports" (submission_id) VALUES (?)',
            (submission_id,),
        )
        self.conn.commit()
        c.close()

    def is_report_added(self, submission_id, c=None):
        if c is None:
            c = self.conn.cursor()
        c.execute("SELECT rowid FROM reports WHERE submission_id=?", (submission_id,))
        return c.fetchone() is not None

    def report_was_resolved(self, submission_id):
        c = self.conn.cursor()

        c.execute(
            "SELECT rowid FROM reports WHERE submission_id=? AND resolved=1",
            (submission_id,),
        )
        result = c.fetchone()
        return result is not None

    def unresolve_report(self, submission_id):
        c = self.conn.cursor()

        c.execute(
            "UPDATE reports SET resolved=0 WHERE submission_id=?",
            (submission_id,),
        )
        self.conn.commit()
        c.close()

    def mark_post_resolved(self, post_id, c=None):
        if c is None:
            c = self.conn.cursor()
        c.execute("UPDATE posts SET resolved=1 WHERE post_id=?", (post_id,))
        self.conn.commit()
        if not self.is_report_resolved(post_id):
            self.mark_report_resolved(post_id, c)

    def mark_report_resolved(self, submission_id, c=None):
        if c is None:
            c = self.conn.cursor()
        c.execute(
            "UPDATE reports SET resolved=1 WHERE submission_id=?", (submission_id,)
        )
        self.conn.commit()
        if not self.is_post_resolved(submission_id):
            self.mark_post_resolved(submission_id, c)

    def get_unresolved_reports(self):
        c = self.conn.cursor()
        c.execute("SELECT submission_id FROM reports WHERE resolved=0")
        return c.fetchall()

    def get_unresolved_posts(self):
        c = self.conn.cursor()
        c.execute("SELECT post_id FROM posts WHERE resolved=0")
        return c.fetchall()
