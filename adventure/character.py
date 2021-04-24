from datetime import datetime
from .stats import Stat, Stats
import csv
import random
import datetime

import logging

logger = logging.getLogger(__name__)


class Character:
    first_name: str
    last_name: str
    title: str
    created_at: datetime.datetime

    stats: Stats

    inventory = []

    equipment = []

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        lines = [
            "```Markdown",
            f"{self.full_name} ({self.age})",
            "",
            f"{self.stats}",
            "```",
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.full_name

    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "created_at": str(self.created_at),
            "stats": self.stats.to_dict(),
            "inventory": self.inventory,
            "equipment": self.equipment,
        }

    @property
    def full_name(self) -> str:
        title = "" if not self.title else f"{self.title} "
        return f"{title}{self.first_name} {self.last_name}"

    @property
    def short_name(self) -> str:
        return f"{self.first_name}"

    @property
    def age(self) -> str:
        now = datetime.datetime.utcnow()

        diff = now - self.created_at
        hours = diff.seconds // (60 * 60)
        d_hours = datetime.timedelta(hours=hours)
        minutes = (diff - d_hours).seconds // 60

        return f"{diff.days}d {hours}h {minutes}min"

    @classmethod
    def create_new(cls):
        with open("adventure/first_names.csv", "r") as f:
            content = f.readlines()

        first_name_data = csv.reader(content, delimiter="\t")

        names = []
        for row in first_name_data:
            names.append(row[1])
            names.append(row[3])

        logger.info(names)

        cls.first_name = random.choice(names)

        with open("adventure/last_names.csv", "r") as f:
            last_names = f.readlines()

        cls.last_name = random.choice(last_names).strip()

        cls.title = ""

        cls.stats = Stats()

        cls.created_at = datetime.datetime.utcnow()

        return cls()

    @classmethod
    def load_from_dict(cls, d: dict):
        cls.first_name = d["first_name"]
        cls.last_name = d["last_name"]
        cls.title = d["title"]
        cls.created_at = datetime.datetime.fromisoformat(d["created_at"])
        cls.stats = Stats(**d["stats"])
        cls.inventory = d["inventory"]
        cls.equipment = d["equipment"]
        return cls()
