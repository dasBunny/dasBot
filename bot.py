#!/usr/bin/python3

import discord
from logins import bot_token

class Bot(discord.Client):
    def get_chat(self, channel):
        return {
            701916157149446245: 701916194135081070,
            701916494300315669: 701933243485782067,
            701921846228025387: 701921872924770354,
        }[channel.id]
    
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if before.channel is not None:
                chat = self.get_channel(self.get_chat(before.channel))
                await chat.send("{} left the channel".format(member.display_name))
                await chat.set_permissions(member, overwrite=None)
            if after.channel is not None:
                chat = self.get_channel(self.get_chat(after.channel))
                await chat.set_permissions(member, read_messages=True)
                await chat.send("{} joined the channel".format(member.display_name))

Bot().run(bot_token)
