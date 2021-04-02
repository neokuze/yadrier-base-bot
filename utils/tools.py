import sys, os, json
import importlib
from importlib import util

class All_Modules:
    def __init__(self): pass

class clients:
    def __init__(self, modules):
        self.discord = modules.discord.Bot()

def open_json(f):
    r = {}
    with open(f) as file:
        r.update(json.load(file))
    return r

def import_to_sys(paths):
    for path in paths:
        if path not in sys.path:
            sys.path.append(path)
        for module in os.listdir(path):
            ismodule = True if module[-3:] == "py" else False 
            if ismodule and module not in sys.modules:
                sys.modules[module] = __import__(module)

def load_modules(where, paths, debug = 0):
    result = {}
    for path in paths:
        div = "/"
        for _module in os.listdir(path):
            name = _module
            if name[0] != "_":
                fpath = f"{path}{div}{name}"
                try:
                    with open(fpath, encoding='utf-8') as _: 
                        pass
                    isdir = False
                except IsADirectoryError:
                    isdir = True
                except Exception as e:
                    _, detalle, n2 = sys.exc_info()
                    numlinea = n2.tb_lineno
                    archivo = n2.tb_frame.f_code.co_filename
                    msg = 'Error in ({}), Line #{} :{}'.format(
                        archivo, numlinea, detalle)
                    if debug > 0:
                        print(msg)
                if not isdir:
                    spec = util.spec_from_file_location(name, fpath)    
                    module = util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                isset = False
                if not hasattr(where, name.split(".")[0]):
                    setattr(where, name.split(".")[0], module)
                    isset = True
                u = path.split("/")[-1:][0]
                if u not in result:
                    i = [name] if isset else []
                    result[u] = dict(modules=[name], count=0, already=i)
                else:
                    result[u]['count'] += 1
                    result[u]['modules'].append(name)
                    if isset:
                        result[u]['already'].append(name)
    return result
