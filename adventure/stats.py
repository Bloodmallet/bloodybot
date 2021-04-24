import enum

import random


class Stat(enum.Enum):
    POWER = "power"
    SPEED = "speed"
    LUCK = "luck"


class Stats:
    def __init__(
        self,
        *,
        power=None,
        speed=None,
        luck=None,
    ) -> None:
        if not all([power, speed, luck]):
            power = random.randint(1, 5)
            speed = random.randint(1, 5)
            luck = random.randint(1, 5)

        self._power = power
        self._speed = speed
        self._luck = luck
        self._tmp_power = None
        self._tmp_speed = None
        self._tmp_luck = None

    def __str__(self) -> str:
        lines = ["Stats"]
        if self._tmp_power:
            prefix = "+"
            if self._tmp_power < 0:
                prefix = ""
            lines.append(f"Power {self.power:>3d} ({prefix}{self._tmp_power})")
        else:
            lines.append(f"Power {self.power:>3d}")
        if self._tmp_speed:
            prefix = "+"
            if self._tmp_speed < 0:
                prefix = ""
            lines.append(f"Speed {self.speed:>3d} ({prefix}{self._tmp_speed})")
        else:
            lines.append(f"Speed {self.speed:>3d}")
        if self._tmp_luck:
            prefix = "+"
            if self._tmp_luck < 0:
                prefix = ""
            lines.append(f"Luck  {self.luck:>3d} ({prefix}{self._tmp_luck})")
        else:
            lines.append(f"Luck  {self.luck:>3d}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Stats {self.power} {self.speed} {self.luck}"

    def to_dict(self) -> dict:
        return {
            "power": self._power,
            "speed": self._speed,
            "luck": self._luck,
        }

    @property
    def power(self) -> int:
        """Determines your success chance."""

        return self._power

    @property
    def speed(self) -> int:
        """Determines your speed."""

        return self._speed

    @property
    def luck(self) -> int:
        """Determines your success chance."""

        return self._luck
