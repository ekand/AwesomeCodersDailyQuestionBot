import discord
import pymongo
from pymongo import MongoClient
import asyncio
from discord.ext import commands, tasks

client = commands.Bot(command_prefix="qdj ")
client.remove_command('help')

TOKEN = "BOT TOKEN GOES HERE"

CHANNEL = "CHANNEL TO SEND MESSAGE HERE AS AN INT"

cluster = MongoClient(
    "LINK TO YOUR MONGODB CLUSTER")

db = cluster["NAME OF DATABASE HERE"]

collection = db["NAME OF COLLECTION HERE"]

numRows = collection.estimated_document_count()

if collection.estimated_document_count() < 1:
  collection.insert_one({"id": 1,"question": "No questions at the moment. Please notify a moderator to add more."})
  MESSAGE = collection.find_one({"id": 1})["question"]
else:
  MESSAGE = collection.find_one({"id": 1})["question"]

#Function that sends the daily question
@tasks.loop(hours = 24)
async def send_interval_message():
  await client.wait_until_ready()
  channel = client.get_channel(CHANNEL)
  messageSent = collection.find_one({"id": 1})["question"]
  role = "<@&[REPLACE THIS WITH THE ROLE ID OF THE ROLE THE BOT WILL PING]>"
  await channel.send(role + " " + messageSent)
  collection.delete_one({"id": 1})

  reorder(1,collection.estimated_document_count())

@send_interval_message.before_loop
async def wait_interval():
    await client.wait_until_ready()

@client.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
  embed = discord.Embed(
    title = "List of commands",
    color = discord.Color.blue()
  )
  embed.add_field(name = "instructions", value = "Use the prefix 'qdj' and then type in one of the following commands and its required arguments. For adding questions, be sure to surround your question with quotation marks for the bot to accept the entire question.", inline = False)
  embed.add_field(name = "getstatus", value = "Sends a message if the bot is online as well as the number of questions in its database.", inline = False)
  embed.add_field(name = "get [id]", value = "Given an id number, it will return the question assigned that id number.", inline = False)
  embed.add_field(name = "add [question]", value = "Adds the question to the database.", inline = False)
  embed.add_field(name = "remove [id]", value = "Given an id number, it will remove the question assigned that id number.", inline = False)
  embed.add_field(name = "replace [id] [newquestion]", value = "Given an id number and new question, it will replace the question assigned that number with the new question.", inline = False)

  await ctx.send(embed=embed)

#Checks if the bot is working. Sends an embedded message if it's online and nothing if it is not.
@client.command()
@commands.has_permissions(administrator=True)
async def getstatus(ctx):
  embed = discord.Embed(
                title="Bot Status",
                color=discord.Color.blue()
            )
  embed.add_field(name="Status", value="Online", inline=False)
  embed.add_field(name="Number of questions", value=collection.estimated_document_count())

  await ctx.send(embed=embed)

#Returns the question given an id. 
@client.command()
@commands.has_permissions(administrator=True)
async def get(ctx,id):
  if int(id) > collection.estimated_document_count():
    await ctx.channel.send("Question not found. Check to see if your number is greater than the number of questions that exist and try again.")
  else:
    id = int(id)
    question = collection.find_one({"id": id})["question"]
  
    # create embed
    embed = discord.Embed(
      title="Question info",
      color=discord.Color.blue()
      )
    embed.add_field(name="id", value=id, inline=False)
    embed.add_field(name="Question", value=question)
    await ctx.send(embed=embed)

#Adds a question to the database
@client.command()
@commands.has_permissions(administrator=True)
async def add(ctx,question):
  question = {"id": collection.estimated_document_count() + 1, "question": question}
  collection.insert_one(question)

  embed = discord.Embed(
  title="Your question has been added. Use 'qdj get [id]' to view your question.",
  color=discord.Color.blue()
  )
  embed.add_field(name="id", value=question.get("id"), inline=False)
  embed.add_field(name="Question", value=question.get("question"))

  await ctx.send(embed=embed)

#Removes the question given an id. 
@client.command()
@commands.has_permissions(administrator=True)
async def remove(ctx,id):
  if int(id) > collection.estimated_document_count():
    await ctx.channel.send("Question does not exist. Check to see if your number is greater than the number of questions that exist and try again.")
  else:
    id = int(id)
    question = collection.find_one({"id": id})["question"]
    print(question)
    collection.delete_one({"id": id})

    # create embed
    embed = discord.Embed(
      title="Your question has been removed.",
      color=discord.Color.blue()
  )
    embed.add_field(name="id", value=id, inline=False)
    embed.add_field(name="Question", value=question)

    await ctx.channel.send(embed=embed)

  reorder(id, collection.estimated_document_count())

#Edits a question given its id and the new question it will replace it with
@client.command()
@commands.has_permissions(administrator=True)
async def replace(ctx,id,newQuestion):
  if int(id) > collection.estimated_document_count():
    await ctx.channel.send("Question not found. Check to see if your number is greater than the number of questions that exist and try again.")
  else:
    id = int(id)
    question = collection.find_one({"id": id})["question"]
    collection.find_one_and_replace({"id":id,"question":question},{"id":id,"question": newQuestion})

    embed = discord.Embed(
      title="Your question has been replaced",
      color=discord.Color.blue()
  )
    embed.add_field(name="id", value=id, inline=False)
    embed.add_field(name="Previous Question", value=question, inline=False)
    embed.add_field(name="New Question", value=newQuestion)

    await ctx.channel.send(embed=embed)

#Function that gets called to reorder the ids to ensure that ids for each question incremenet by 1
def reorder(id, numRows):
  if id <= numRows:
    id += 1
    collection.update_one(
    {"id": id},
    {"$set": {"id": id - 1}}
    )
    return reorder(id, numRows)
  else:
    return

#Error handling for missing arguments, non-existent commands, or missing administrator permissions
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    await ctx.send("Error: You need to be administrator to use this command.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Error: Missing an arugment.")
  elif isinstance(error, commands.CommandNotFound):
    await ctx.send("Error: Command not found.")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    if collection.estimated_document_count() < 1:
      collection.insert_one({"id": 1,"question": "No questions at the moment. Please notify a moderator to add more."})
    send_interval_message.start()
    

client.run(TOKEN)
