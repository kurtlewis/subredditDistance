import praw
from logger import log
import re


class Spider:

    def __init__(self):
        self.reddit = object()
        try:
            self.reddit = praw.Reddit('subredditDistance')
        except Error:
            print('Make sure you have a praw.ini file defined with a bot' +
                  'called "subredditDistance"')
            print(Error)
        self.log = log.Log('./reddit-spider.log', 500)
        self.queue = list()
        self.subredditRegex = re.compile('(/r/\S+)\s')

    def crawl(self, startingPoint):
        """ Crawls from a starting point, adding to the queue any websites it finds """
        topPosts = self.reddit.subreddit(startingPoint).top(limit=10)
        for post in topPosts:
            post.comments.replace_more(threshold=5)
            comments = post.comments.list()
            for comment in comments:
                self.extractSubreddit(comment.body)

    def extractSubreddit(self, commentStr):
        result = self.subredditRegex.match(commentStr)
        if result is not None:
            # Found a link to a subreddit
            sub = result.group(0)
            print(sub)

