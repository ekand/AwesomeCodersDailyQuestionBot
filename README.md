# QDJ - The Question du jour (Daily Question) bot

QDJ is a discord bot that can ask users a question every day. It will ping the users who have the role for it and ask them a question which the users can answer. I originally wrote this bot for a server for learning French but this can certainly be used for other reasons too.

# Prerequisites

Before you can begin setting up your bot, you will need the following:

* A Discord account
* An application created through Discord's developer portal
* A MongoDB database
* A place to host your bot
* discord.py
* dnspython
* pymongo

You can easily create a Discord account on their website and then you can access their developer portal where you can create an application afterwards. The application is for genreating a token which you'll need to run the bot. The bot uses MongoDB as its database to store the questions and you would want a place where you can host your bot so that it can run 24/7 and continuously ask questions daily. 

`discord.py`, `dnspython` and `pymongo` can be installed using the `pip install` command.


