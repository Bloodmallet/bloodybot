"""A discord bot that reflets the adventure hungry TürstopperPinguin
(short: TP).

TODO:
    - load adventures from json file
    - let users propose new adventures
    - save proposed new adventures to additional json file
    - check other guild.members for being bots -> leave guild if more than X
        bots are present

"""

import discord
import json
import os
import random

from tp_bot import secrets

token = secrets.token


class TPClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('tp_bot/adventures.json', 'r') as f:
            self._adventures = json.load(f)['adventures']

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Connected to {len(self.guilds)} guilds.')
        for guild in self.guilds:
            print(
                f'  - {guild.name} (id: {guild.id}, member: {len(guild.members)})'
            )

    def get_adventure(self, *args, **kwargs):

        try:
            actor = args[0][0]
        except IndexError:
            actor = 'TP'

        if actor is None:
            actor = 'TP'

        story = random.choice(self._adventures)

        story = story.replace('<ACTOR>', actor)

        return story

    async def on_message(self, message: str):
        if message.author == self.user:
            return

        if message.author.bot:
            return

        PREFIX = '| "|>'

        if not message.content.startswith(PREFIX):
            return

        content = message.content.strip()

        command = content[5:].split()[0]
        try:
            params = content[5:].split()[1:] or [None]
        except IndexError:
            params = [None]

        commands = {
            '!':
            self.get_adventure,
            '?':
            'Greetings, let me explain your options real quick:\nFor me to notice your message you need to start it with a penguin | "|> and add a command afterwards. Commands:\n! - receive one of many adventures\n! <name> - let <name> receive one of many adventures\n? - receive this help text\n\nSoon: propose an adventure.',
        }

        if command in commands:
            if type(commands[command]) == str:
                await message.channel.send(commands[command])
            else:
                await message.channel.send(commands[command](params))


client = TPClient()

client.run(token)
