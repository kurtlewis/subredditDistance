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
        # Check to see if the subreddit exists
        try:
            self.reddit.subreddits.search_by_name(subreddit, exact=True)
        except Exception as e:
            print(e)
            # Subreddit doesn't exist, return a blank list
            return list()
        # Get top posts
        topPosts = self.reddit.subreddit(subreddit).top(limit=self.postLimit)
        results = list()
        for post in topPosts:
            self.extractAllSubreddits(post.selftext, results)
            self.extractAllSubreddits(post.title, results)
            # Only expand comments if requested
            if self.expandComments:
                # Only expand comments when it gives at least 5 more comments
                post.comments.replace_more(threshold=5)
            comments = post.comments.list()
            for comment in comments:
                if isinstance(comment, praw.models.MoreComments):
                    # If expanding comments is not turned on, MoreComments
                    # will create issues
                    continue
                self.extractAllSubreddits(comment.body, results)
        return results

    def extractAllSubreddits(self, text, results):
        sub = self.extractSubreddit(text)
        while sub is not None:
            results.append(sub)
            text = text.replace(sub, '', 1)
            sub = self.extractSubreddit(text)

    def extractSubreddit(self, text):
        result = self.subredditRegex.match(text)
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
