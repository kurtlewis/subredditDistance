This project isn't complete - it may never be completed.

Incomplete list of features I'd like to add:
* better support for handling praw errors
* logging to a file so that file can be viewed in a web browser
  * This can be accomplished by running the file and piping output to tee - `python3 -u bin/subBFS.py [tableName] [subreddit] [postsPerSub] 2>&1 | tee outfile.txt`. `-u` unbuffers python output so it is immediate. 

# Subreddit relations
For calculating how often reddit pages are linked between each other

# To run
Write your own script using the package, or run a script in bin/ by installing
the project using pip. Use the `-e` flag to update the installation while the
module is edited, which can be useful for development.
`$pip install .`
`$pip3 install .`

# Dependencies
* mysql
* [Mysql Connector](https://dev.mysql.com/downloads/connector/python/)
* [pycodestyle](https://github.com/PyCQA/pycodestyle)
* [PRAW](http://praw.readthedocs.io/en/latest/index.html)

# Configuring Praw
This repo is setup to expect a preconfigured reddit details. Use PRAW's documentation on [praw.ini](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html?highlight=ini) files to set this up, and call it `subredditDistance`

# Configuring Mysql
Because this is a project written to run on a raspberry pi for a long period of time, it is not suitable to hold data in memory (and its good sql practice for me). Copy `config.ini.example` to `config.ini` and fill in the values to connect to an instance of mysql. You'll probably want to create a new database in mysql.

