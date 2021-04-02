import json, os, sys
import importlib

class Union:
    def __init__(self):
        self.langs = {}
        self.cmds = {}
        self.default_bot = {"prefix": "."}

    def load_all(self):
        self.load_cmds()
        self.load_langs()

    def get_lang(self, lang, id):
        if lang in self.langs and id in self.langs[lang]:
            return self.langs[lang][id]
        return "langs[{}][{}]".format(repr(lang), repr(id))

    def load_langs(self):
        print("GLOBAL-> ", "Loading languages...")
        self.langs.clear()
        for path in os.scandir("langs/"):
            lang = os.path.splitext(os.path.split(path.path)[1])[0]
            with open(path.path, encoding="utf-8") as file:
                self.langs[lang] = json.load(file)

    def load_cmds(self):
        print("GLOBAL-> ", "Loading cmds...")
        self.cmds.clear()
        for path in os.listdir("commands"):
            try:
                path = os.path.join("commands", path)
                cmd = os.path.splitext(os.path.split(path)[1])[0]
                with open(path, encoding="utf8") as _:
                    try:
                        spec = importlib.util.spec_from_file_location(cmd, path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        module._name = str(cmd)
                        module.for_owners = bool(
                            hasattr(module, "for_owners") and module.for_owners)
                        module.for_pm = bool(
                            hasattr(module, "for_pm") and module.for_pm)
                        if hasattr(module, "category") and module.category:
                            module.category = str(getattr(module, "category"))
                        else: module.category = False
                        self.cmds[cmd] = module
                    except BaseException as e:
                        ename = e.__class__.__name__
                        eargs = str(e)
                        msg = "Error loading cmd {}.\n\t{}: {}"
                        msg = msg.format(cmd, ename, eargs)
                        print(msg, file=sys.stderr)
            except IsADirectoryError:
                pass
                