import enum
import typing
from .stats import Stats

import random


class Slot(enum.Enum):
    HEAD = "head"
    SHOULDERS = "shoulders"
    CHEST = "chest"
    HANDS = "hands"
    LEGS = "legs"
    FEET = "feet"
    RING = "ring"
    TRINKET = "trinket"
    WEAPON = "weapon"
    OFFHAND = "offhand"


class Rarity(enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

    def generate_rarity(self):
        stages = [self.COMMON, self.UNCOMMON, self.RARE, self.EPIC, self.LEGENDARY]

        success_rolls = 0
        for _ in range(len(stages) - 1):
            if random.randint(1, 10) == 10:
                success_rolls += 1
            else:
                break

        return stages[success_rolls]


class Item:
    def __init__(self) -> None:
        self.slot: typing.Optional[Slot] = None
        self.stats: Stats = None
        self.value: float = 0.0
        self.rarity: Rarity = None
