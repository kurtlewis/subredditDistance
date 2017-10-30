# Subreddit relations
For calculating how often reddit pages are linked between each other

# Dependencies
* mysql
* [Mysql Connector](https://dev.mysql.com/downloads/connector/python/)
* [pycodestyle](https://github.com/PyCQA/pycodestyle)
* PRAW


# Configuring Praw
This repo is setup to expect a preconfigured reddit details. Use PRAW's documentation on [praw.ini](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html?highlight=ini) files to set this up, and call it `subredditDistance`

# Configuring Mysql
Because this is a project written to run on a raspberry pi for a long period of time, it is not suitable to hold data in memory (and its good sql practice for me). Copy `config.ini.example` to `config.ini` and fill in the values to connect to an instance of mysql