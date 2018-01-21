"""
Because there's a problem that lets subreddits be entered multiple times, it's
necessary to dedup some subs in the database
The first step is going to be determining the scope of the problem.
################################################################################
        Commit 5c5de91 makes the issue this script aims to fix a non-issue
        It is not necessary to use this script for any runs after updating to
        that commit
################################################################################
"""

import re
import sys
import subredditDistance

# The first step is using the log file to determine how many times each sub
# was duplicated
if (len(sys.argv) < 3):
    raise Exception("Please input the name of the log file and table name in that order")
# create regex pattern
regex = re.compile(r'Searching ([a-zA-Z0-9_]+)')
# create dict for tracking appearances of each subreddit
subs = dict()
# open the file and parse it
logFile = open(sys.argv[1], 'r')
for line in logFile:
    match = re.search(regex, line)
    if match is not None:
        sub = match.group(1).lower()
        if sub in subs:
            subs[sub] = subs[sub] + 1
        else:
            subs[sub] = 1

# close logfile
logFile.close()

# Create database connection
dbx = subredditDistance.DatabaseConnection(sys.argv[2], False)
# dbx.allRowsToLowerCase()

# For each duplication, set the value of each link in the database to
# itself divided by the total number of times that sub was duplicated
total = 0
for sub in subs.keys():
    if subs[sub] > 1:
        print(sub + ':' + str(subs[sub]))
        total = total + subs[sub]
        # only run dedup action when this is explicitly uncommented
        #dbx.deDupSubredditLink(sub, subs[sub])
print(total)


