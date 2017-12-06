import praw
import re
import time


class Spider:

    def __init__(self, databaseCnx, postLimit=100, expandComments=True):
        self.dbCnx = databaseCnx
        self.postLimit = postLimit
        self.expandComments = expandComments
        self.reddit = object()
        try:
            self.reddit = praw.Reddit('subredditDistance')
        except Error:
            print('Make sure you have a praw.ini file defined with a bot' +
                  'called "subredditDistance"')
            print(Error)
        self.subredditRegex = re.compile('/r/([a-zA-Z0-9_]+)[\s|/]')
        self.visitedSubreddits = set()

    def crawlForSubredditLinks(self, subreddit):
        """ Crawls from a starting point, adding to the queue
         any websites it finds """
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

    def breadthFirstSubredditScan(self, startingSubreddit):
        queue = list()
        queue.append(startingSubreddit)
        self.visitedSubreddits.add(startingSubreddit)
        while len(queue) > 0:
            subreddit = queue.pop(0)
            print('[Queue:' + str(len(queue)) + ']Searching ' + subreddit)
            try:
                results = self.crawlForSubredditLinks(subreddit)
                for link in results:
                    if link not in self.visitedSubreddits:
                        queue.append(link)
                        self.visitedSubreddits.add(link)
                    self.dbCnx.addSubredditLink(subreddit, link)
            except Exception as err:
                # Error, this subreddit won't be hit
                print("Error: " + str(err))
                # Temporary fix - sleep in case it was an internet issue
                # hopefully the issue will resolve itself
                # raise err
                time.sleep(60)
