import discord
import vote_helper
import json
import  asyncio
import voteClass
import _pickle as pickle
from datetime import datetime, timedelta
from logins import bot_token
from discord.ext import commands
from strings import *
from config import *

bot = commands.Bot(command_prefix='!', description='''Ich stinke hart nach hurensohn''')
vote_list = []

def get_chat(channel):
    return {
        701916157149446245: 701916194135081070,
        701916494300315669: 701933243485782067,
        701921846228025387: 701921872924770354,
    }[channel.id]

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.get_channel(voting_channel_id).purge()
    await loadVotes()
    await timedCheck()

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if before.channel is not None:
            print("removing permission")
            chat = bot.get_channel(get_chat(before.channel))
            await chat.set_permissions(member, overwrite=None)
        if after.channel is not None:
            chat = bot.get_channel(get_chat(after.channel))
            await chat.set_permissions(member, read_messages=True)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel.id == voting_channel_id:
        if message.author != bot.user:
            print(message.author.name)
            print(bot.user.name)
            print("deleting")
            await message.delete()

@bot.event
async def on_reaction_add(reaction,user):
    print("reaction event")
    if reaction.message.channel.id == voting_channel_id:
        if user != bot.user:
            await reaction.remove(user)
            for v in vote_list:
                if v.message_id == reaction.message.id:
                    if reaction.emoji == "\N{THUMBS UP SIGN}":
                        if await v.castVote(user,True):
                            vote_list.remove(v)
                    elif reaction.emoji == "\N{THUMBS DOWN SIGN}":
                        if await v.castVote(user,False):
                            vote_list.remove(v)
                    save()
                    break
  #          pickle.dump(vote_list, open("votes.pickle","wb"))


@bot.command()
async def contest(ctx,message_id,*text):
    if ctx.channel.id == voting_channel_id:
        for word in text:
            print(word)
    
@bot.command()
async def purge_votes(ctx):
    if vote_helper.checkForRole(ctx.author,'Admin'):
        x = [None]
        pickle.dump(x, open("votes.pickle","wb"))
        await bot.get_channel(voting_channel_id).purge()

@bot.command()
async def vote(ctx,*topic):
    if vote_helper.checkForRole(ctx.author,'Trusted'):
        topic_string = " ".join(topic)
        eligible = vote_helper.getEligibleCount(ctx)
        v = voteClass.Vote(ctx.message.author.id,round((eligible*0.35)),round((eligible/2)+0.5),datetime.now()+timedelta(days=2),bot,topic_string)
        await v.sendMessage()
        vote_list.append(v)
        print(v.json_dict())
        save()
        #pickle.dump(vote_list, open("votes.pickle","wb"))
    else:
        await ctx.author.send(vote_no_permission_start)

def save():
    json_list = []
    for v in vote_list:
        json_list.append(v.json_dict())
    print(json.dumps(json_list))
    json.dump(json_list,open('votes.json','w'))

async def loadVotes():
    votes = json.load(open('votes.json'))
    for vote in votes:
        obj = voteClass.Vote(vote['author_id'],vote['quota'],vote['cutoff'],datetime.fromtimestamp(vote['end']),bot,vote['topic'])
        print(vote['ayy'])
        obj.setVars(vote['ayy'],vote['nay'],vote['voted'])
        await obj.sendMessage()
        vote_list.append(obj)

async def timedCheck():
    while True:
        await asyncio.sleep(60)
        print('checking')
        for v in vote_list:
            if await v.checkFinish():
                vote_list.remove(v)
                save()
            
bot.run(bot_token)
