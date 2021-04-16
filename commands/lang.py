
async def run(self, message, args, lcs):
    lang = args[0] if args else ""
    msg = self.config.get_lang(lcs.lang, "lang.listall").format(", ".join(list(self.config.base.langs)))
    if lang in self.config.base.langs:
        self.config.users.update_row(lcs.cuser.id, "lang", lang)
        msg = self.config.get_lang(lang, "lang.success").format(repr(lang))
    await message.channel.send(msg)
