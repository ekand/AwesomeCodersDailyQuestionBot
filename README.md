# QDJ - The Question du jour (Daily Question) bot

QDJ is a discord bot that can ask users a question every day. It will ping the users who have the role for it and ask them a question which the users can answer. If you're wondering why I named the bot, "QDJ", it stands for "question du jour" and I originally wrote this bot for a server for learning French. Of course, it can be used for other purposes too. 

# Prerequisites

Before you can begin setting up your bot, you will need the following:

* A Discord account
* An application created through Discord's developer portal
* A MongoDB database
* A place to host your bot
* discord.py
* dnspython
* pymongo

You can create a Discord account on their website and then you can access their developer portal where you can create an application. The application is for genreating a token which you'll need to run the bot. The bot uses MongoDB as its database to store the questions and you would want a place where you can host your bot so that it can run 24/7 and continuously ask questions daily. 

`discord.py`, `dnspython` and `pymongo` can be installed using the `pip install` command.

# Setting up the database

Create your mongoDB cluster and create your database and collection. When your bot is activated, each entry you create will have an `_id`, which identifies the document and is immutable, an `id`, which identifies the question and is mutable, and a `question` which is the question content itself.

# Setting up the bot itself

In the code found in `qdj.py`, you'll find fields where you will need to fill in yourself. Follow the code and replace the values with your data as necessary. 

# Hosting the Bot

Please see your server host for instructions on how to upload the bot onto their server and have it run 24/7.

# Testing the Bot

You can test the bot locally by running `python qdj.py` or have your server start the bot. To learn more on how to use the bot, type in `qdj help` for the list of commands.
