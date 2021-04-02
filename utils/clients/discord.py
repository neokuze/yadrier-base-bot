import asyncio 
import discord
import config

class Bot(discord.Client):
    async def on_ready(self):
        if not hasattr(self, "config"):
            self.config = config.discord()
        self.config.base.load_all()
        print("Loading discord bot...")
        self.loop.create_task(self.auto_save())

    async def on_member_join(self, member):
        _ = self.config.get_guild(member.guild.id, ex=dict(lang='en', suffix='.'))

    async def on_member_leave(self, member):
        _ = self.config.get_guild(member.guild.id, ex=dict(lang='en', suffix='.'))

    async def auto_save(self):
        while True:
            self.config.save_all()
            await asyncio.sleep(60*6)

    async def on_message(self, message):
        cprefix = self.config.default_bot["prefix"]
        try:
            if message.author.bot == True or message.author == self.user:
                return
            message_content = message.content.split(" ")
            if message.guild != None:
                cguild = self.config.get_guild(str(message.guild.id), ex=dict(lang='en', prefix=cprefix))
                if not cguild:
                    cguild = self.config.get_guild(str(message.guild.id), ex=dict(lang='en', prefix=cprefix))
                cuser = self.config.get_user(message.author.id, ex=dict(lang=cguild.lang or 'en', prefix=cprefix or '.'))
                if not cuser:
                    cuser = self.config.get_user(message.author.id, ex=dict(lang=cguild.lang or 'en', prefix=cprefix or '.'))
            else:
                cuser = self.config.get_user(message.author.id, ex=dict(lang='en', prefix=cprefix))
                if not cuser:
                    cuser = self.config.get_user(message.author.id, ex=dict(lang='en', prefix=cprefix))
                cguild = None
            
            if len(message.content.split()) > 1:
                cmd, args = message.content.split(" ", 1)
                args = args.split()
            else:
                cmd, args = message.content.lower(), []
            cmd = cmd.lower()
            _lcs = {'cuser': cuser, 'cguild': cguild, 'cmd': cmd, 'lang': cuser.lang}
            lcs = config.Struct(**_lcs)
            if cmd and cmd[0] in [cprefix]:
                prfx = True
                cmd = cmd[1:].lower()
            else:
                prfx = False
            if prfx:
                if cmd in self.config.base.cmds and self.config.base.cmds[cmd]:
                    modulo = self.config.base.cmds[cmd]
                    if modulo.for_owners and not message.author.id in self.config.owners:
                        await message.channel.trigger_typing()
                        await message.channel.send(self.config.get_lang(cuser.lang, "notowner"))
                    else:
                        msg = await modulo.run(self, message, args, lcs)
        except Exception as e:
            print(e)
    def closing_db(self):
        self.config.users.close()
        self.config.guild.close()
