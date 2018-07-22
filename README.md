# KoKoBot

## Overview

KoKoBot is a Discord/Reddit bot that's used by the moderators of r/kpop, r/kpophelp, and r/kpoppers.

The primary purpose is to get realtime updates of the unmoderated and reports queue delivered directly to Discord.
From there mods can take actions such as (re)approve or remove (with reasons).

KoKoBot uses a very simple command syntax.


## Installation

There are two files that must be created.

`config.ini` and `kokobot.db`

### config.ini

Use the provided `config.ini.dist` as an example.
Fill in the appropriate values for the config options.
These will be used by KoKoBot for connecting to Discord and Reddit

### kokobot.db

Use the provided `kokobot.db.schema` file to provision a SQLite3 database.
This is the database that will be the main backing store for KoKoBot's internal state.
It will keep track of posts it's seen and decisions that have been made by moderators regarding those posts.

## Running

KoKoBot requires Python3 (Note that Python 3.7.0 will require patching of some packages due to `async` becoming a reserved word).

To run,

```
python3 bot.py
```
