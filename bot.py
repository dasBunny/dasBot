import discord

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
                await chat.set_permissions(member, overwrite=None)
            if after.channel is not None:
                chat = self.get_channel(self.get_chat(after.channel))
                await chat.set_permissions(member, read_messages=True)

Bot().run('NzAyMDQ0ODA3MDgxNzU0NjQx.XqC7yg.lIlozDtNRlf7PFp9DzseE2FmIM8')
