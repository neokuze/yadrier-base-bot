import sys

for_owners = True

async def run(self, message, args, lcs):
    locs = {}
    print("weeee")
    if not args:
        ret = self.config.get_lang(lcs.cuser.lang, 'no_args')
    else:
        try:
            glibs =  globals() | locals() # python3.9
            string = 'async def execute(): return ' + " ".join(args)
            exec(string, glibs, locs)
            ret = await locs["execute"]()
        except:
            ret = sys.exc_info()[1].args[0]
    if ret == None:
        ret = self.config.get_lang(lcs.cuser.lang, 'done')
    await message.channel.send(ret)
