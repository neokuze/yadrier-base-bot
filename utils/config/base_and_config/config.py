import os, sys, json
import base_union
import mydb
base = base_union.Union()

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class discord:
    def __init__(self, test=False):
        self.owners = [358273884958490624]
        self.base = base
        self.default_bot = {'prefix': "."}
        self.users = mydb.DataBase("discord_users")
        self.guilds = mydb.DataBase("discord_guilds")
    
    def __repr__(self):
        return "discord"

    def get_lang(self, lang, id):
        return self.base.get_lang(lang, id)

    def get_guild(self, name, ex={}):
        r = self.guilds.create_if_doesnt_exist(name, ex)
        if r:
            return Struct(**r)
        return None

    def get_user(self, name, ex={}):
        r = self.users.create_if_doesnt_exist(name, ex)
        if r:
            return Struct(**r)
        return None

    def save_all(self): # to save something every 6 minutes.
        pass