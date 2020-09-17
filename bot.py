#!/usr/bin/python3

import discord
from logins import bot_token


class Bot(discord.Client):
    chat = {}

    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            # leave channel
            if before.channel is not None:
                chat = self.get_channel(self.chat[before.channel.id])
                # remove permission from member
                await chat.set_permissions(member, overwrite=None)
                # delete text channel if empty
                if not before.channel.members:
                    self.chat.pop(before.channel.id, None)
                    await chat.delete()
            # join channel
            if after.channel is not None:
                # create new text channel if none exist
                if after.channel.id not in self.chat or \
                   self.get_channel(self.chat[after.channel.id]) is None:
                    chat = await after.channel.guild .create_text_channel(
                               'chat',
                               topic=after.channel.name,
                               category=self.get_channel(701908552163262508),
                               position=2
                           )
                    self.chat[after.channel.id] = chat.id
                # get associated text channel
                else:
                    chat = self.get_channel(self.chat[after.channel.id])
                # give permission to member
                await chat.set_permissions(member, read_messages=True)


Bot().run(bot_token)
