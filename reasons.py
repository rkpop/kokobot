class Reasons:

    reasons = {
        1: {
            "text": "* This submission is better suited for: {}.",
            "formatted": True,
        },
        2: {
            "text": "* I.A.1 - All submissions must be directly relevant to Korean pop music, artists, companies, or fans. General Korean culture, language, or entertainment industry posts are considered off-topic for this subreddit.",
            "formatted": False,
        },
        3: {
            "text": "* I.A.2 - The title of your submission does not comply with [our formatting rules](/r/kpop/wiki/rules). Feel free to resubmit using the following formatting: {}. Flairs should not be included in the title of submissions. Be sure to flair your post after submitting.",
            "formatted": True,
        },
        4: {
            "text": "* I.A.3 - Submission titles should be detailed and direct. Do not editorialize titles or use vague titles. All types of performance links should always include the artist and song name. When linking to an article, it is best-practice to use the exact title of the article when possible. Titles should be in English. Titles entirely in Korean will be removed.",
            "formatted": False,
        },
        5: {
            "text": "* I.A.4 - Submitted articles that are entirely in Korean must include a full English translation or detailed summary in the comments. Headline or Twitter translations are not sufficient. Machine translations (Google, Bing, Naver, etc.) are not permitted. Please complete the translation before posting and add it immediately to avoid the submission being removed.",
            "formatted": False,
        },
        6: {
            "text": "* I.A.5 - When submitting clips from variety appearances, concerts, or showcases, choose the best clip and submit it as a direct link. All other clips should be added to the comment section for that link. Do not submit multiple clips of the same artist from the same show.",
            "formatted": False,
        },
        7: {
            "text": "* I.A.6 - Images and gifs/gyfs of idols that are not teasers or announcements should be posted to r/kpics or r/kpopgyfs.",
            "formatted": False,
        },
        8: {
            "text": "* I.A.7 - Official teaser images and announcements must be rehosted on imgur or reddit image host. Multiple images should be collected into an album. Teaser image posts from Twitter/Facebook/Instagram/etc are forbidden.",
            "formatted": False,
        },
        9: {
            "text": "* I.A.8 - It is a [repost]({}). Reposts are forbidden unless the previous post has been deleted. Articles and blogs which restate the same news item as a previously posted article without adding significant new information will be considered reposts.",
            "formatted": True,
        },
        10: {
            "text": '* I.A.9 - Memes, jokes, "shitposts", and other items intended primarily for humor are forbidden. These are more appropriate for /r/kpoppers or the "Friday Free-For-All" discussion thread.',
            "formatted": False,
        },
        11: {
            "text": '* I.A.10 - "Blind" articles are forbidden. "Blind" articles are generally gossip articles like "Person A arrested for drugs" or "Top star caught in sex scandal" where the identity of the subject is not revealed.',
            "formatted": False,
        },
        12: {
            "text": "* I.A.11 - Piracy is forbidden. This includes links to sites which promote or facilitate piracy as well as direct links to pirated materials such as torrents. Link to officially licensed sources when available. Unofficial audio uploads should be limited to YouTube only. Unofficial video uploads should be linked only when an officially licensed video is not available in the same format (subbed or raw).",
            "formatted": False,
        },
        13: {
            "text": "* I.A.12 - Solicitation is forbidden. Submissions offering to buy/sell/trade merch, concert tickets, or albums are better suited for r/kpopforsale. r/kpop is not affiliated with r/kpopforsale so use it at your own risk.",
            "formatted": False,
        },
        14: {
            "text": '* I.A.13 - URL shorteners and "click-thru" sites such as adfly are forbidden. Use only direct original links to submitted content.',
            "formatted": False,
        },
        15: {
            "text": '* I.A.14 - "Throwback" posts are forbidden. Please only post current releases, performances, and variety appearances.',
            "formatted": False,
        },
        16: {
            "text": "* I.A.15 - Music show performances and winner announcements should be limited to the music show wiki post for that episode with the exception of the very first Comeback/Debut stage by an artist, the very first music show win ever for an artist, or if there is no broadcast that week but a winner is still announced. A guide to posting and editing the music show wiki posts can be found [here](/r/kpop/comments/5qvxf3/the_complete_guide_to_creating_and_editing_music/).",
            "formatted": False,
        },
        17: {
            "text": "* I.A.16 - Submitting content from your own channel or blog is considered self-promotion. Self-promotion submissions must follow reddit%u2019s 9:1 site-wide rules regarding self-promotion which can be found [here](/wiki/selfpromotion).",
            "formatted": False,
        },
        18: {
            "text": "* I.A.17 - Music streaming site links such as Spotify or Apple Music should be kept in the [Upcoming Releases](/r/kpop/wiki/upcoming-releases/archive) wiki. Album and non-MV song links should be kept in the relevant Album Discussion thread, except for single album releases when there are only two songs. No album discussion should be posted for single releases.",
            "formatted": False,
        },
        19: {
            "text": "* I.B.1 - Submissions that are only relevant to one group, one idol, or their fans and are not newsworthy or substantial should be posted to the [group-specific subreddit](https://www.reddit.com/r/kpop/wiki/relatedsubs#wiki_group.2Fartist_subreddits.3A): /r/{}.  An extensive list of which types of content are allowed and forbidden can be found [here.](https://www.reddit.com/r/kpop/wiki/rules#wiki_b.__group-specific_content)",
            "formatted": True,
        },
        20: {
            "text": '* I.C.1 - Discussion thread submissions should be open-ended conversation starters. Simple questions with a single answer, recommendations, and song/idol identifications should be posted in /r/kpophelp or the "Monday Q&A" discussion thread.',
            "formatted": False,
        },
        21: {
            "text": "* I.C.2 - Discussion submissions should include significant content in the original post beyond just asking a question. Expand upon your topic idea to help generate meaningful discussion. You should start the initial discussion by contributing an answer to your submission. Simply restating the title of the submission in the body does not constitute initial discussion.",
            "formatted": False,
        },
        22: {
            "text": "* I.C.3 - Discussion topics which are overly familiar to kpop fans, worn out, similar to other recent topics, or lacking substance will be removed at moderator discretion.  More information on these topics can be found [here.](https://www.reddit.com/r/kpop/wiki/stale-topics)  These and similar topics are more appropriate for /r/kpoppers.",
            "formatted": False,
        },
        23: {
            "text": '* II.B.3 - Personal Conduct - No personal attacks.  No racism or hate speech.  Do not post hateful comments about groups, idols, or songs.  Do not post "gross" or overtly sexual comments about idols. Be respectful at all times.',
            "formatted": False,
        },
    }

    def get_header(self, username, kind):
        return "Hey /u/{}, thank you for submitting to /r/kpop! Unfortunately, your {} has been removed for the following reason(s):\n\n".format(
            username, kind
        )

    def get_footer(self):
        return "*I am a bot. Please do not reply to my messages as they will not be seen by the modteam.*\n\nIf you have any questions regarding the ruleset of /r/kpop, please refer to the [rules](/r/kpop/wiki/rules) or [message the moderators](/message/compose?to=%2Fr%2Fkpop). Thank you!"

    def needs_text(self, reason):
        if reason == "custom":
            return True

        reason = int(reason)
        if len(self.reasons) <= reason:
            raise ValueError("Reason does not exist")

        reason_obj = self.reasons[reason]
        return reason_obj["formatted"]

    def add_reason(self, reason, text=None):
        if reason == "custom":
            if text is None:
                raise ValueError("No text given for custom reason.")
            return "* {}".format(text)

        reason = int(reason)
        reason_obj = self.reasons[reason]
        if reason_obj["formatted"]:
            if text is None:
                raise ValueError("No text given for reason ".format(reason))
            return reason_obj["text"].format(text)
        else:
            return reason_obj["text"]
