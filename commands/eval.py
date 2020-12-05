import sys

async def run(self, message, args, lcs):
    locs = {}
    if not args:
        self.config.get_lang(lcs.cuser.lang, 'eval.noargs')
    else:
        try:
            glibs =  globals() | locals() # python3.9
            string = 'async def execute(): return ' + " ".join(args)
            exec(string, glibs, locs)
            ret = await locs["execute"]()
        except:
            ret = sys.exc_info()[1].args[0]
    return dict(text=ret)
