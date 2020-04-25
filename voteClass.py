from config import voting_channel_id,announcement_channel_id
from strings import *
from datetime import datetime,timedelta
import vote_helper
import json

class Vote:
    def __init__(self,author,quota,cutoff,end,bot,topic):
        self.type = 'undef'
        self.author_id = author
        self.quota = quota
        self.cutoff = cutoff
        self.end = end
        self.bot = bot
        self.ayy = 0
        self.nay = 0
        self.voted = []
        self.message_id = 0
        self.topic = topic

    async def sendMessage(self):
        message=await self.bot.get_channel(voting_channel_id).send("Processing vote")
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.add_reaction('\N{THUMBS DOWN SIGN}')
        self.message_id = message.id
        await message.edit(content=vote_general_message.format(self.topic,self.bot.get_user(self.author_id).mention,self.quota,self.end.strftime("%d/%m/%Y, %H:%M")))

    def print(self):
        print("Type: "+self.type)
        print("Author: "+self.bot.get_user(self.author_id).name)
        print("Quota: "+str(self.quota))
        print("End: "+str(self.end))
        print("Ayy: "+str(self.ayy))
        print("Nay: "+str(self.nay))

    def json_dict(self):
        return {'type':self.type,'author_id':self.author_id,'quota':self.quota, 'cutoff':self.cutoff,'end':datetime.timestamp(self.end),'ayy':self.ayy,'nay':self.nay,'voted':self.voted,'topic':self.topic}

    def setVars(self,ayy,nay,voted):
        self.ayy = ayy
        self.nay = nay
        self.voted = voted

    def getMessage(self):
        return self.message_id

    async def castVote(self,user,pro):
        for uid in self.voted:
            if uid == user.id:
                await user.send(vote_already_voted.format(self.topic))
                return False
        self.voted.append(user.id)
        if pro:
            self.ayy = self.ayy+1
            txt = "AYY"
        else:
            self.nay = self.nay+1
            txt = "NAY"
        await user.send(vote_counted.format(self.topic,txt))
        if self.ayy > self.cutoff:
            await self.success()
            return True
        if self.nay > self.cutoff:
            await self.failure(True)
            return True
        return False

    async def checkFinish(self):
        if self.end < datetime.now():
            await self.finish()
            return True
        return False

    async def finish(self):
        if len(self.voted)>=self.quota:
            if self.ayy>self.nay:
                await self.success()
            else:
                await self.failure(True)
        else:
            await self.failure(False)

    async def success(self):
        message = await self.bot.get_channel(voting_channel_id).fetch_message(self.message_id)
        await message.delete()
        await self.bot.get_channel(announcement_channel_id).send(vote_passed.format(self.topic,self.ayy,self.nay))
        return
    async def failure(self,quota_met):
        message = await self.bot.get_channel(voting_channel_id).fetch_message(self.message_id)
        await message.delete()
        if quota_met:
            await self.bot.get_channel(announcement_channel_id).send(vote_failed.format(self.topic,self.nay,self.ayy))
        else:
            await self.bot.get_channel(announcement_channel_id).send(vote_failed_quota.format(self.topic,self.ayy,self.nay,len(self.voted),self.quota))
        return

class Promote(Vote):
    def __init__(self,author,quota,end,target):
        self.target_id = target.id
        super().__init__(author,quota,end)

    async def castVote(self,user,pro):
        if user.id == self.target_id:
            return 
        for uid in self.voted:
            if uid == user.id:
                return
        self.voted.append(user.id)
        if pro:
            self.ayy = self.ayy+1
        else:
            self.nay = self.nay+1
        if self.ayy > self.quota:
            await self.voteSucess()
        return

    def voteSucess(self):
        pass

class General(Vote):
    def __init__(self,author,quota,end,desc):
        self.description = desc
        super().__init__(author,quota,end)