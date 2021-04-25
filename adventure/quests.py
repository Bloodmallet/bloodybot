import datetime
import json
import typing


class Quest:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        description_short: str,
        duration: int = 3 * 60,
        reward_exp: int = 5,
        reward_loot: typing.Optional[int] = None,
        optional_loot: typing.Optional[int] = None,
        optional_chance: float = 0.0,
    ) -> None:
        self.name = name
        self.description = description
        self.description_short = description_short
        self.duration = int(duration)
        self.reward_exp = int(reward_exp)
        self.reward_loot = reward_loot
        self.optional_loot = optional_loot
        self.optional_chance = optional_chance

    def __str__(self) -> str:
        duration = str(datetime.timedelta(seconds=self.duration))
        strings = [
            f"{self.name} ({duration:0>8})",
            "",
            f"*{self.description_short}*",
            "",
            self.description,
            "",
            "**Rewards**",
            f"Experience: {self.reward_exp}",
            f"Loot: {self.reward_loot if self.reward_loot else 'None'}",
            f"Rare-Loot: {self.optional_loot if self.optional_loot else 'None'}",
        ]
        return "\n".join(strings)

    def effective_duration(self, speed: int):
        return max(self.duration / (1.0 + speed / 100.0), 60)


def get_quests() -> typing.List[Quest]:
    with open("adventure/quests.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return list([Quest(**quest) for quest in data])
