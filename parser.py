import reddit
import asyncio
import reasons
import posts

reddit = reddit.Reddit()
praw = reddit.praw()
reasons = reasons.Reasons()
posts = posts.Posts()

class CommandParser:

    async def parse_commands(self, raw_input):
        # <approve|remove> [<post/comment id>] reasons? [reasons]

        if len(raw_input) < 2:
            raise ValueError('Missing post/comment ids')

        if raw_input[0] == 'approve':
            post_ids = raw_input[1].split(',')
            for post_id in post_ids:
                is_report = False
                if posts.is_post_resolved(post_id):
                    is_report = True
                await reddit.approve_post(post_id, is_report=is_report)
            return

        if raw_input[0] == 'approvec':
            comment_ids = raw_input[1].split(',')
            for comment_id in comment_ids:
                await reddit.approve_comment(comment_id)
            return

        if raw_input[0] == 'removec':
            comment_ids = raw_input[1].split(',')
            for comment_id in comment_ids:
                await reddit.remove_comment(comment_id)
            return

        if raw_input[0] == 'remove':
            post_ids = raw_input[1].split(',')
            if len(post_ids) > 1:
                if len(raw_input) > 3:
                    raise ValueError('Reasons are not supported when removing multiple posts')
                for post in post_ids:
                    is_report = False
                    if posts.is_post_resolved(post_id):
                        is_report = True
                    await reddit.remove_post(post, is_report=is_report)
                return

            if len(raw_input) < 3:
                is_report = False
                if posts.is_post_resolved(post_ids[0]):
                    is_report = True
                await reddit.remove_post(post_ids[0], is_report=is_report)
                return

            if raw_input[2] != 'reasons':
                raise ValueError('Invalid command format. Expected "reasons".')

            try:
                reason_string = self.parse_reasons(raw_input[3:])
            except ValueError as ve:
                return ve

            if len(reason_string) == 0:
                raise ValueError('No reasons given for removal')

            username = praw.submission(id=post_ids[0]).author
            header = reasons.get_header(username, 'post')
            footer = reasons.get_footer()

            reason_string = '{}{}{}'.format(header, reason_string, footer)

            is_report = False
            if posts.is_post_resolved(post_ids[0]):
                is_report = True
            await reddit.remove_post(post_ids[0], reason_string, is_report=is_report)
            return

        raise ValueError('Invalid command format')

    def parse_reasons(self, reason_input):
        # 1 'r/kpoppers' 2 3 6 9 'https://redd.it/7fb1r5' custom 'Custom reason!'

        reason_string = ''

        user_input = False
        for index,reason in enumerate(reason_input):
            if user_input:
                user_input = False
                continue

            if reasons.needs_text(reason):
                if len(reason_input) <= index+1:
                    raise ValueError('Reason {} required text.'.format(reason))

                if reason_input[index+1] == 'custom':
                    raise ValueError('Reason {} required text.'.format(reason))

                reason_string += (reasons.add_reason(reason, reason_input[index+1]) + "\n\n")
                user_input = True

            else:
                reason_string += (reasons.add_reason(reason) + "\n\n")

        return reason_string
