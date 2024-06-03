from dataclasses import dataclass, field

from ..constants import *
from .utils import alias_convert

__all__ = [
    "Achievement"
]

@dataclass
class Achievement:
    _data: dict = field(repr=False)
    achievement_id: int = 0
    name: str = None
    description: str = None
    xp: int = 0

    def __post_init__(self):
        data = alias_convert(self._data, "ACHIEVEMENT")
        for i in data:
            setattr(self, i, data[i])