import praw
from logger import log
import re


class Spider:

    def __init__(self, postLimit=100, expandComments=True):
        self.postLimit = postLimit
        self.expandComments = expandComments
        self.reddit = object()
        try:
            self.reddit = praw.Reddit('subredditDistance')
        except Error:
            print('Make sure you have a praw.ini file defined with a bot' +
                  'called "subredditDistance"')
            print(Error)
        self.log = log.Log('./reddit-spider.log', 500)
        self.subredditRegex = re.compile('/r/([a-zA-Z0-9_]+)[\s|/]')
        self.visitedSubreddits = set()

    def crawlForSubredditLinks(self, subreddit):
        """ Crawls from a starting point, adding to the queue any websites it finds """
        topPosts = self.reddit.subreddit(subreddit).top(limit=self.postLimit)
        results = list()
        for post in topPosts:
            if self.expandComments:
                post.comments.replace_more(threshold=5)
            comments = post.comments.list()
            for comment in comments:
                if isinstance(comment, praw.models.MoreComments):
                    # If expanding comments is not turned on, MoreComments 
                    # will create issues
                    continue
                sub = self.extractSubreddit(comment.body)
                if sub is not None:
                    results.append(sub)
        return results

    def extractSubreddit(self, commentStr):
        result = self.subredditRegex.match(commentStr)
        if result is not None:
            # Found a link to a subreddit
            return result.group(1)
        else:
            return None

    def breadthFirstSubredditScan(self, startingSubreddit, queue=list()):
        print('Search started with ' + startingSubreddit)
        results = self.crawlForSubredditLinks(startingSubreddit)
        for link in results:
            if link not in self.visitedSubreddits:
                queue.append(link)
                self.visitedSubreddits.add(link)
            print(startingSubreddit + ' links to ' + link)
        # Pop off top of queue and recursively call
        if len(queue) != 0:
            self.breadthFirstSubredditScan(queue.pop(0), queue=queue)
        
