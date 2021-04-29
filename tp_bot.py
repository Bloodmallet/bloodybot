"""A discord bot that reflets the adventure hungry TürstopperPinguin
(short: TP).

TODO:
    - check other guild.members for being bots -> leave guild if more than X
        bots are present
"""

import discord
import json
import logging
import os
import random
from typing import List, Tuple

from tp_bot import secrets
from adventure.adventure_bot import AdventureBot

token = secrets.token
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class TPClient(discord.Client, AdventureBot):
    """Bot reacts to chat commands."""

    def __init__(self, *args, **kwargs):
        """Load the content of 'tp_bot/adventures.json' and 'tp_bot/suggestions.json'."""
        super().__init__(*args, **kwargs)

        with open("tp_bot/adventures.json", "r") as f:
            self._adventures: List[str] = json.load(f)["adventures"]

        try:
            with open("tp_bot/suggestions.json", "r") as f:
                self._suggestions: List[str] = json.load(f)
        except FileNotFoundError:
            self._suggestions = []

    def add_suggestion(self, *args, **kwargs) -> str:
        """Add user provided strings as an adventure suggestion. Resultstring
        is saved to disk.

        Returns:
            [str]: Bot thanks the user for the suggestion.
        """
        self._suggestions.append(" ".join(*args))
        self.save_suggestions()

        return f"Thank you for your suggestion: {self._suggestions[-1]}"

    def get_adventure(self, *args, **kwargs) -> str:
        """An adventure is retrieved from the approved adventure list. If an
        actor name was provided, this name is used. Else 'TP' is used.

        Returns:
            str: personalized adventure text
        """

        try:
            actor: str = args[0]
        except IndexError:
            actor = "TP"

        if actor is None:
            actor = "TP"

        story: str = random.choice(self._adventures)

        story = story.replace("<ACTOR>", actor)

        return story

    def list_suggestions(self, *args, **kwargs) -> str:
        """Show all user-provided suggestions. This function might need to
        leave...

        Returns:
            [str]: [description]
        """
        return "\n".join(self._suggestions)

    def save_suggestions(self) -> None:
        """Save suggestions to file/disk."""
        with open("tp_bot/suggestions.json", "w") as f:
            json.dump(self._suggestions, f)

    async def on_message(self, message: str) -> None:
        """React to user input (message).

        Args:
            message (str): [description]
        """
        if message.author == self.user:
            return

        if message.author.bot:
            return

        PENGUIN_LONG = '| "|>'
        PENGUIN_SHORT = '">'

        PREFIXES = [
            PENGUIN_LONG,
            PENGUIN_SHORT,
        ]

        active_prefix = None
        for prefix in PREFIXES:
            if message.content.startswith(prefix):
                active_prefix = prefix
                logger.info(
                    f"Message with content prefix '{active_prefix}' in server {message.guild.name} detected."
                )

        if active_prefix is None:
            return

        content: str = message.content.strip()

        try:
            command = content[len(active_prefix) :].split()[0]
        except IndexError:
            print(f"IndexError on {content}")
            return

        try:
            params = content[len(active_prefix) :].split()[1:] or [None]
        except IndexError:
            params = [None]

        if active_prefix == PENGUIN_SHORT:
            params = [message] + params

        if active_prefix == PENGUIN_LONG:
            commands = {
                "!": self.get_adventure,
                "+": self.add_suggestion,
                # '+?': self.list_suggestions,
                "?": "Greetings, let me explain your options real quick:\nFor me to notice your message you need to start it with a penguin | \"|> and add a command afterwards. Commands:\n`!` - receive one of many adventures\n`! <name>` - let <name> receive one of many adventures\n`+ <adventure>` - suggest a new adventure (After a review your adventure might be added. Use '<ACTOR>' as the <name> placeholder in your adventure)\n`Invite` - return the invite-link to get this bot\n`?` - receive this help text",
                "Invite": "https://discordapp.com/api/oauth2/authorize?client_id=639876959350030338&permissions=2048&scope=bot",
            }
        elif active_prefix == PENGUIN_SHORT:
            commands = {
                "new": self.create_new_character,
                "new-character": self.create_new_character,
                "c": self.character_overview,
                "overview": self.character_overview,
                "start-quest": self.start_quest,
                "q": self.questlog,
                "questlog": self.questlog,
                "?": "Prefix your commands using `\">`\nCommands:\n- `?` show help text\n- `new-character [FIRST_NAME LAST_NAME:optional] [!:optional]`, create a new character. [FIRST_NAME LAST_NAME] set the character name, need to be provided as a pair. [!] deletes your existing character to create a new one.\n- `c` or `overview`, view your character overview\n- `start-quest` receive a random quest (if you're already on a quest, that one will be aborted)\n- `q` or `questlog`, view your active questlog\n\n Invite this bot to your own discord using this link: <https://discordapp.com/api/oauth2/authorize?client_id=639876959350030338&permissions=2048&scope=bot>",
            }

        if command in commands:
            if isinstance(commands[command], str):
                await message.channel.send(commands[command])
            else:
                await message.channel.send(commands[command](*params))

    async def on_ready(self):
        """Start-up message. Let's the user know about active connections and
        how many users are in each discord.
        """
        print(f"{self.user} has connected to Discord!")
        print(f"Connected to {len(self.guilds)} guilds.")
        for guild in self.guilds:
            print(f"  - {guild.name} (id: {guild.id}, {len(guild.members)} members)")


client = TPClient()

client.run(token)
