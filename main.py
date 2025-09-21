
import discord
from discord.ext import commands
from database import *
import json
import os
from keep_alive import keep_alive

token = os.environ['TOKEN']

intents = discord.Intents.all()
client = commands.Bot(command_prefix = "-", intents=intents)

#math server id
server_id = 882210341893861386

@client.event
async def on_ready():
  print('Logged in as {}'.format(client.user))
#----------------------------------------------
@client.command(name="reset_scores")
@commands.has_role("qotd creator")
async def reset_scores(ctx):
  reset_all()
#----------------------------------------------
@client.command(name="set_qotd")
@commands.has_role("qotd creator")
async def set_qotd(ctx):
  try:
    image = ctx.message.attachments[0]
  except IndexError:
    await ctx.send("You need to upload an image to set.")
    return

  with open("temp.json", "r+") as file:
    dicti = json.load(file)
    dicti["qotd_link"] = image.url
    file.seek(0)
    json.dump(dicti, file, indent=4)
    file.truncate()
  
  for member in ctx.guild.members:
    update(member.id, new_attempts=0)
  await ctx.send("Set!")
#----------------------------------------------
@client.command(name="announce")
@commands.has_role("qotd creator")
async def announce(ctx, role):
  with open("temp.json", "r") as json_file:
    json_obj = json.load(json_file)
  current_qotd_link = json_obj["qotd_link"]
  await ctx.send(f"{role} New QOTD released! DM your answers to me with the format `-answer <your answer>`. For example `-answer 24`. Thanks!")
  await ctx.send(current_qotd_link)
#----------------------------------------------
@client.command(name="set_ans")
@commands.has_role("qotd creator")
async def set_ans(ctx, ans):
  try:
    ans = int(ans)
  except ValueError:
    await ctx.send("Please set an integer answer only")
    return

  with open("temp.json", "r+") as file:
    dicti = json.load(file)
    dicti["ans"] = ans
    file.seek(0)
    json.dump(dicti, file, indent=4)
    file.truncate()
  await ctx.send("Answer set!")
#----------------------------------------------
@client.command(name="score", help="Gives user's current score. Can be used to find someone else's score by ?score @mention")
async def score(ctx, user:discord.Member = None):
  score = 0
  if(user is None):
    score = search(ctx.message.author.id)["Score"]
  else:
    if(search(user.id) is None):
      post(user.id, 0)
    else:
      score = search(user.id)["Score"]  

  await ctx.send("The score so far is **"+str(score)+" points**")
#----------------------------------------------
@client.command(name="leaderboard", help="Leaderboard of top qotd scorers", aliases=["lb"])
async def leaderboard(ctx):
  leaderboard = collection.find({})
  lb = []

  for i in leaderboard:
    if(not i["Score"] == 0):
      lb.append(
        {'user': discord.utils.get(ctx.guild.members, id=i['UserId']).name,
        'score': i['Score']
         })
  lb = sorted(lb, key= lambda i: i['score'], reverse=True)  
  string = "Top QOTD scorers:\n```\n"
  for i in lb:
    string += i['user']+": "+str(i['score'])+" points\n"
  string += "```"
  await ctx.send(string)
  
#----------------------------------------------
@client.command(name="add_points", help="Add points to a user with ?add_points @mention points (Only for admins)")
@commands.has_role("admin")
async def add_points(ctx, user: discord.User, points):
  try:
    points = int(points)
  except ValueError:
    await ctx.send("Enter an integer number of points")
    return
  result = search(user.id)
  if(not result is None):
    update(user.id, new_score=result["Score"]+points)
  else:
    post(user.id, points)
  await ctx.send("The user's new score is now "+str(search(user.id)["Score"]))
#----------------------------------------------
@client.command(name="answer")
@commands.dm_only()
async def answer(ctx, ans):
  global server_id
  server = client.get_guild(server_id)
  if(not ctx.message.author in server.members):
    return

  member = server.get_member(ctx.message.author.id)

  if(search(member.id) is None):
      post(member.id, 0)

  qotd_solved = discord.utils.get(server.roles, name="qotd-solved")
  if(qotd_solved in member.roles):
    await ctx.send("You have already solved the qotd.")
    return
  result = search(member.id)
  try:
    if(result["attempts"] == 5):
      await ctx.send("Sorry you have taken 5 attempts already.")
      return
  except KeyError:
    update(member.id, new_attempts=0)
    result["attempts"] = 0

  try:
    ans = int(ans)
  except ValueError:
    await ctx.send("Please set an integer answer only")
    return

  with open("temp.json", "r+") as file:
    dicti = json.load(file)
  if(dicti["ans"] == ans):
    result["attempts"] += 1
    update(member.id, new_attempts = result["attempts"])

    update(member.id, new_score = result["Score"]+6-result["attempts"])

    await member.add_roles(qotd_solved)
    await ctx.message.channel.send("Correct! You have earned 5 points")
  else:
    update(member.id, new_attempts=result["attempts"]+1)
    result["attempts"] += 1
    await ctx.send("That is the wrong answer. You have **"+str(5-result["attempts"])+"** attempt(s) left")
#----------------------------------------------  
@client.command(name="remove")
@commands.has_role("tech team")
async def remove(ctx):
  global server_id
  server = client.get_guild(server_id)

  qotd_solved = discord.utils.get(server.roles, name="qotd-solved")
  mem = server.get_member(ctx.message.author.id)
  await mem.remove_roles(qotd_solved)
  await ctx.send("qotd-solved role removed")
#----------------------------------------------
  
keep_alive()
client.run(token)