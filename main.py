import utils
import os
import sys
import asyncio
import json

class Main:
    def __init__(self, settings=None):
        self._settings = settings
        self._modules = utils.All_Modules()
        self._loader = None
        self._close_db_on_close = None
        self._config = None
        self._accs = None
        self._clients = None

    @property
    def settings(self):
        return self._settings

    @property
    def modules(self):
        return self._modules

    @property
    def loader(self):
        return self._loader

    @property
    def close_db_on_close(self):
        return self._close_db_on_close

    @property
    def config(self):
        return self._config
    
    @property
    def accs(self):
        return self._accs

    @property
    def clients(self):
        return self._clients

    def start(self, loop):
        try:
            print("Loading bots... ", [x for x in dir(self.modules) if x[0] != '_'])
            if self.settings['debug']:
                Tasks = [self._client.discord.start(self._accs["discord"]['debug_bot'])]
            else:
                Tasks = [self._client.discord.start(self._accs["discord"]['bot'])]
            task = asyncio.gather(*Tasks, return_exceptions=True)
            loop.run_until_complete(task)
            loop.run_forever()
        except KeyboardInterrupt:
            print("[b0t] was killed.")
        except:
            _, d, n3 = sys.exc_info()
            n = n3.tb_lineno
            a = n3.tb_frame.f_code.co_filename
            msg = 'Error in ({}), Line #{} :{}'.format(
                a, n, d)
            print(msg)
        finally:
            if main.close_db_on_close:
                _ = [getattr(main, str(x)).closing_db()
                    for x in main if str(x)[:1] != "_" and hasattr(main, f"{x}", "closing_db")]

    def set_properties_before(self, loader, accounts):
        self._loader = loader
        self._accs = accounts
        self._loader(self._modules, [os.getcwd()+"/utils/clients"])
        self._client = utils.clients(self._modules)
        

if __name__ == "__main__":
    settings = utils.open_json('settings.json')
    main = Main(settings)
    utils.import_to_sys(
        [os.getcwd()+x for x in list(settings['paths'].values())]) # carga modulos localmente
    main.set_properties_before( #crea nuevas propiedades
        utils.load_modules, #prepara el cargar modulo
        utils.open_json(os.getcwd()+settings['auth'])) #credenciales del bot a usar.
    loop = asyncio.get_event_loop()
    main.start(loop)
    
 