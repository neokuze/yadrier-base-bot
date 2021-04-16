
async def run(self, message, args, lcs):
    msg = self.config.get_lang(lcs.lang, "hello").format(message.author)
    await message.channel.send(msg)
