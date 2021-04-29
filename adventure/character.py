from datetime import datetime
from .stats import Stat, Stats
from .quests import Quest, get_quests
import csv
import random
import datetime
import json
import logging
import os
import enum

logger = logging.getLogger(__name__)


class Status(enum.Enum):
    IDLE = "idle"
    ADVENTURE = "adventure"
    QUEST = "quest"


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

    quest_name: str = None
    quest_start_time: datetime.datetime = None

    adventure_start_time: datetime.datetime = None

    def __init__(self) -> None:
        self.messages = []

    def __str__(self) -> str:
        lines = [
            "```Markdown",
            f"{self.full_name} [{self.race}]",
            f"Level: {self.level} ({self.exp} / {self.next_level_exp_requirement})",
            self.status,
            "",
            f"{self.stats}",
            "```",
        ]
        if self.messages:
            lines = self.messages + lines
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
            "quest_name": self.quest_name,
            "quest_start_time": str(self.quest_start_time)
            if self.quest_start_time
            else None,
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
        return self.level * 10

    @property
    def status(self):
        if self.quest_name:
            text = ""
            quest = self.get_quest(self.quest_name)
            remaining_duration = datetime.timedelta(
                seconds=quest.effective_duration(self.stats.speed)
            ) - (datetime.datetime.utcnow() - self.quest_start_time)
            if remaining_duration > datetime.timedelta(seconds=0):
                stringyfied = str(remaining_duration).split(".")[0]
                text = f"remaining: {stringyfied:0>8}"
            else:
                text = f"done"

            return f"Quest: {quest.name} ({text})"
        elif self.adventure_start_time:
            return "Adventuring"
        else:
            return "Idle"

    def load_quests(self):
        if not hasattr(self, "_quests"):
            self._quests = get_quests()
        return self._quests

    def get_quest(self, name: str) -> Quest:
        self.load_quests()
        for quest in self._quests:
            if quest.name == name:
                return quest
        return None

    def roll(self, chance: float) -> bool:
        return random.random() * 10000.0 <= chance * 100.0

    def turn_in_quest(self):
        if not self.quest_name:
            return
        if "done" in self.status:
            quest = self.get_quest(self.quest_name)
            self.exp += quest.reward_exp
            self.quest_name = None
            self.quest_start_time = None
            self.messages.append(f"Quest '{quest.name}' completed.")
            self.messages.append(f"Received {quest.reward_exp} experience points.")
            if quest.reward_loot:
                self.inventory.append(quest.reward_loot)
            if quest.optional_loot:
                if self.roll(quest.optional_chance):
                    self.inventory.append(quest.optional_loot)

    def go_on_quest(self, quest: Quest):
        self.quest_name = quest.name
        self.quest_start_time = datetime.datetime.utcnow()
        self.save()

    def update_level(self):
        if self.exp >= self.next_level_exp_requirement:
            self.exp = self.exp - self.next_level_exp_requirement
            self.level += 1

            self.messages.append('Level up! :tada: TP is so proud of you. !<"')

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
        self.turn_in_quest()
        self.update_exp()
        self.update_level()

        self.save()

    def save(self):
        path = f"characters/{self.user_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)

    @classmethod
    def create_new(cls, user_id: str, *, first_name: str = None, last_name: str = None):

        cls.user_id = user_id

        with open("adventure/first_names.csv", "r", encoding="utf-8") as f:
            content = f.readlines()

        first_name_data = csv.reader(content, delimiter="\t")

        names = []
        for row in first_name_data:
            names.append(row[1])
            names.append(row[3])

        with open("adventure/last_names.csv", "r", encoding="utf-8") as f:
            last_names = f.readlines()

        with open("adventure/races.csv", "r", encoding="utf-8") as f:
            races = f.readlines()

        cls.first_name = random.choice(names) if first_name is None else first_name
        cls.last_name = (
            random.choice(last_names).strip() if last_name is None else last_name
        )
        cls.title = ""
        cls.created_at = datetime.datetime.utcnow()
        cls.race = random.choice(races).strip()

        cls.level = 1
        cls.exp = 0

        cls.stats = Stats()

        cls.quest_name = None
        cls.quest_start_time = None
        cls.last_time_based_exp = None

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

        with open(path, "r", encoding="utf-8") as f:
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

        cls.quest_name = d.get("quest_name", None)

        quest_start_time = d.get("quest_start_time", None)
        if quest_start_time:
            cls.quest_start_time = datetime.datetime.fromisoformat(quest_start_time)
        else:
            cls.quest_start_time = None

        character = cls()

        character.self_update()
        return character
