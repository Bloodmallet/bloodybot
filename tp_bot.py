import discord
import os
import random

from tp_bot import secrets

token = secrets.token


class TPClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Connected to {len(self.guilds)} guilds.')
        for guild in self.guilds:
            print(f'  - {guild.name} (id: {guild.id})')
            if guild.members:
                print('    Members:')
            for member in guild.members:
                print(f'      {member.name}')

    def adventure(self, *args, **kwargs):

        try:
            actor = args[0][0]
        except IndexError:
            actor = 'TP'

        adventures = [
            f'Winter is coming for {actor}.',
            f'{actor} is at the Hell\'s Gate.',
            f'A Danger Noodle is attacking {actor}.',
            f'{actor} the spy. So sneaky!',
            f'Prison Break for {actor}!',
            f'What is love? {actor} don\'t hurt me!',
        ]

        return random.choice(adventures)

    async def on_message(self, message: str):
        if message.author == self.user:
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
            '!': self.adventure,
            '?': 'You\'re part of a wild experiment. Stay tuned!'
        }

        if command in commands:
            await message.channel.send(commands[command](params))


client = TPClient()

client.run(token)
