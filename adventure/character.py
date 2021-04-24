from datetime import datetime
from .stats import Stat, Stats
import csv
import random
import datetime
import json
import logging
import os


logger = logging.getLogger(__name__)


class Character:
    user_id: str

    first_name: str
    last_name: str
    title: str
    created_at: datetime.datetime
    last_time_based_exp: datetime.datetime

    race: str

    level: int
    exp: int

    stats: Stats

    inventory = []

    equipment = []

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        lines = [
            "```Markdown",
            f"[{self.race}] {self.full_name} ({self.age})",
            f"Level: {self.level} ({self.exp} / {self.next_level_exp_requirement})",
            "",
            f"{self.stats}",
            "```",
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.full_name

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "created_at": str(self.created_at),
            "race": self.race,
            "stats": self.stats.to_dict(),
            "inventory": self.inventory,
            "equipment": self.equipment,
            "level": self.level,
            "exp": self.exp,
            "last_time_based_exp": str(self.last_time_based_exp),
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

        return f"{diff.days}d {hours:0>2d}:{minutes:0>2d}h"

    @property
    def next_level_exp_requirement(self) -> int:
        return self.level ** 2 * 10

    def update_level(self):
        if self.exp >= self.next_level_exp_requirement:
            self.exp = self.exp - self.next_level_exp_requirement
            self.level += 1

            power = random.randint(0, 2)
            # luck effect
            if random.randint(1, 100) <= self.stats.luck ** (1 / 2):
                power += 1
            self.stats._power += power
            self.stats._tmp_power = power

            speed = random.randint(0, 2)
            # luck effect
            if random.randint(1, 100) <= self.stats.luck ** (1 / 2):
                speed += 1
            self.stats._speed += speed
            self.stats._tmp_speed = speed

            luck = random.randint(0, 2)
            # luck effect
            if random.randint(1, 100) <= self.stats.luck ** (1 / 2):
                luck += 1
            self.stats._luck += luck
            self.stats._tmp_luck = luck

    def update_exp(self):
        now = datetime.datetime.utcnow()
        passed_minutes = (now - self.last_time_based_exp).seconds // 60

        if passed_minutes > 0:
            self.exp += passed_minutes
            self.last_time_based_exp = now

    def self_update(self):
        self.update_exp()
        self.update_level()

        self.save()

    def save(self):
        path = f"characters/{self.user_id}.json"
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)

    @classmethod
    def create_new(cls, user_id: str):

        cls.user_id = user_id

        with open("adventure/first_names.csv", "r") as f:
            content = f.readlines()

        first_name_data = csv.reader(content, delimiter="\t")

        names = []
        for row in first_name_data:
            names.append(row[1])
            names.append(row[3])

        with open("adventure/last_names.csv", "r") as f:
            last_names = f.readlines()

        with open("adventure/races.csv", "r") as f:
            races = f.readlines()

        cls.first_name = random.choice(names)
        cls.last_name = random.choice(last_names).strip()
        cls.title = ""
        cls.created_at = datetime.datetime.utcnow()
        cls.race = random.choice(races).strip()

        cls.level = 1
        cls.exp = 0

        cls.stats = Stats()

        return cls()

    @classmethod
    def load(cls, user_id: str):
        """Load character of the the user.

        Args:
            user_id (str): [description]

        Returns:
            str: Character information
        """
        path = f"characters/{user_id}.json"
        if not os.path.isfile(path):
            raise ValueError("No character found. Create one!")

        with open(path, "r") as f:
            d = json.load(f)

        cls.user_id = d["user_id"]
        cls.first_name = d["first_name"]
        cls.last_name = d["last_name"]
        cls.title = d["title"]
        cls.created_at = datetime.datetime.fromisoformat(d["created_at"])
        cls.race = d["race"]
        cls.stats = Stats(**d["stats"])
        cls.inventory = d["inventory"]
        cls.equipment = d["equipment"]
        cls.level = d.get("level", 1)
        cls.exp = d.get("exp", 0)
        cls.last_time_based_exp = datetime.datetime.fromisoformat(
            d.get("last_time_based_exp", d["created_at"])
        )

        character = cls()

        character.self_update()
        return character
