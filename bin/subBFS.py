#!/usr/bin/env python3

import argparse
import subredditDistance

parser = argparse.ArgumentParser(
    description='Will BFS through reddit with starting subreddit, storing data'
                ' in supplied tablename',
    epilog='It can take a while to run this operation, there is a request'
           ' limit of .5/s and it takes multiple requests to parse'
           ' a single submission')
parser.add_argument('tableName', type=str, help='The name of the table to use')
parser.add_argument('startingSubreddit', type=str, help='The subreddit to'
                    ' start BFS on.')
parser.add_argument('postsPerSubreddit', type=int,
                    help='Number of posts per subreddit to be scanned')
parser.add_argument('-p', '--pickle', type=str,
                    help='Enables writing of progress files to disk. Takes'
                    ' path as argument.')
parser.add_argument('-t', '--tableReuse', action='store_true',
                    help='Allows the named table to be reused, even if it'
                    ' already exists')
# parser.add_argument('-x', '--dontexpand', action='store_true',
#                     help='Dont expand comments. Can greatly improve speed')

args = parser.parse_args()

dbx = subredditDistance.DatabaseConnection(args.tableName, 
                                           not(args.tableReuse))

spid = subredditDistance.Spider(dbx, postLimit=args.postsPerSubreddit)

if (args.pickle):
    spid.addPicklingUtil(subredditDistance.PicklingUtil(args.tableName,
                                                        args.pickle))


spid.breadthFirstSubredditScan(args.startingSubreddit)

dbx.close()
