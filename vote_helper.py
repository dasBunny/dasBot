import pickle
from strings import *
import time

def refreshMessages():
    pass

def checkForRole(target,rolename):
    all_roles = target.roles
    for role in all_roles:
        if role.name == rolename:
            return True
    return False

def checkIfExisting(votes,votetype,target):
    for _,value in votes.items():
        if value["type"]==votetype:
            if value["target"]==target.id:
                return True
    return False

def getEligibleCount(ctx):
    quota = 0
    for member in ctx.guild.members:
        if checkForRole(member,'Trusted'):
            quota=quota+1
    return quota

async def promoteStart(ctx,target):
    if checkForRole(target,"Trusted"):
        print("Role already assigned.")
        await ctx.message.author.send(vote_already_trusted)
        return False
    votes = pickle.load(open("votes.pickle","rb"))
    print(votes)
    if checkIfExisting(votes,'promote',target):
        await ctx.message.author.send(vote_already_running)
        return False        
    quota = 0
    for member in ctx.guild.members:
        if(checkForRole(member,'Trusted') and member.id!=target.id):
            quota=quota+1
    quota = round(quota*2/3)
    print(quota)
    message=await ctx.channel.send("Processing vote")
    await message.edit(content=vote_promote_message.format(target.mention,ctx.author.mention,quota,message.id))
    votes[message.id]={"type":'promote',"message":message.id,"target":target.id,"starttime":time.time(),"author":ctx.author.id,"voted":[ctx.author.id],"ayy":1,"nay":0}
    await message.add_reaction('\N{THUMBS UP SIGN}')
    await message.add_reaction('\N{THUMBS DOWN SIGN}')
    pickle.dump(votes, open("votes.pickle","wb"))

async def voteCasted(message,user,pro):
    votes = pickle.load(open("votes.pickle","rb"))
    if message.id in votes:
        if checkForRole(user,'Trusted'):
            vote = votes[message.id]
            for userid in vote['voted']:
                if userid == user.id:
                    await user.send(vote_already_voted.format(message.id))
                    return False
            if pro:
                vote['ayy']=vote['ayy']+1
            else:
                vote['ayy']=vote['ayy']+1
        else:
            await user.send(vote_no_permission)
            return False
    else:
        await user.send(vote_doesnt_exist.format(message.id))
        return False

        