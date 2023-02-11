# pycord-bot-class

## Requirements

- [colorama](https://pypi.org/project/colorama/) (pip install colorama)
- [pycord](https://pypi.org/project/py-cord/) (pip install py-cord)
- [aiosqlite](https://pypi.org/project/aiosqlite/) (pip install aiosqlite)

## Features

- Load cogs from a directory
- Load cogs from subdirectorys
- Add static cogs
- Async database functions
- Built-in on_ready event
- (Coming soon) Built-in error handler

## Bot parameters

- token (String)
- ready_event (Boolean)
- debug_logs (Boolean, optional, default False)

## Example

```py
import discord

# Import the Bot class
from BotClass import Bot

# Create a bot variable
bot = Bot(
    token="abc123",
    ready_event=True,
    intents=discord.Intents.default()
)

if __name__ == '__main__':
    # Loads cogs from a directory, for example: events.onready
    bot.load_dir('events')

    # Loads cogs from subdirectorys, for example: cogs.slashcommands.ban
    bot.load_subdir('cogs')

    # Add static cogs
    bot.add_static_cogs(["commands.help", "commands.kick"])

    # bot.exec() starts the bot
    bot.exec()
```
