DiscordGuild = """
    CREATE TABLE IF NOT EXISTS DiscordGuild (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        lang TEXT,
        prefix TEXT,
        created_at TEXT,
        venable INTEGER DEFAULT 0,
        vrole TEXT,
        vchannel TEXT
    )
"""

DiscordUser = """
    CREATE TABLE IF NOT EXISTS DiscordUser (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        lang TEXT,
        prefix TEXT,
        nick TEXT,
        birthday TEXT,
        created_at TEXT
    )
"""
