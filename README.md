# pycord-cog-template-class

## Requirements
- colorama (pip install colorama)
- pycord (pip install py-cord)

## Example
```py
import discord

# Import the Bot class
from BotClass import Bot

# Create a bot variable
bot = Bot(
    token="abc123",
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
