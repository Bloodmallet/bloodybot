from .character import Character

import logging
import json

import os

logger = logging.getLogger(__name__)


class AdventureBot:
    def create_new_character(self, message, *params):
        """Create a new character. Force character creation by adding a "!" """
        force = "!" in params
        logger.debug(params)
        path = f"characters/{message.author.id}.json"

        if os.path.isfile(path) and not force:
            return "A character already exists."

        logger.debug(f"Generating character for user '{message.author.id}'.")

        c = Character.create_new(message.author.id)

        with open(f"characters/{message.author.id}.json", "w") as f:
            json.dump(c.to_dict(), f, ensure_ascii=False)

        return f"New character created. **{c.full_name}** is ready for adventure.\n{c}"

    def character_overview(self, message, *params):
        """Character overview"""

        try:
            c = Character.load(message.author.id)
        except ValueError:
            return "No character found"
        return str(c)
