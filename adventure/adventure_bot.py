from .character import Character
from .quests import get_quests

import logging
import json
import os
import random

logger = logging.getLogger(__name__)


class AdventureBot:
    def create_new_character(self, message, *params):
        """Create a new character. Force character creation by adding a "!" """
        force = "!" in params
        logger.debug(params)
        path = f"characters/{message.author.id}.json"

        first_name = None
        last_name = None
        if len(params) >= 2:
            first_name = params[0]
            last_name = params[1]

        if os.path.isfile(path) and not force:
            return "A character already exists."

        logger.debug(f"Generating character for user '{message.author.id}'.")

        c = Character.create_new(
            message.author.id, first_name=first_name, last_name=last_name
        )

        with open(f"characters/{message.author.id}.json", "w") as f:
            json.dump(c.to_dict(), f, ensure_ascii=False)

        return f"New character created. **{c.full_name}** is ready for adventure.\n{c}"

    def character_overview(self, message, *params):
        """Character overview"""

        try:
            c = Character.load(message.author.id)
        except ValueError:
            logger.exception("Character load failed.")
            return "No character found"
        return str(c)

    def start_quest(self, message, *params):

        try:
            c = Character.load(message.author.id)
        except ValueError:
            return "No character found"

        if not hasattr(self, "_quests"):
            self._quests = get_quests()

        quest = random.choice(self._quests)
        c.go_on_quest(quest)

        return str(quest)

    def questlog(self, message, *params):
        try:
            c = Character.load(message.author.id)
        except ValueError:
            return "No character found"

        if c.quest_name is None:
            return f"{c.full_name} is currently on no quest."

        if not hasattr(self, "_quests"):
            self._quests = get_quests()

        for quest in self._quests:
            if quest.name == c.quest_name:
                return f"{c.full_name} Questlog:\n{quest}"

        return f"{c.full_name} fell into the abyss of a non-existing quest?"
