from dataclasses import dataclass, field
from typing import List

from ..constants import *
from .player import StatsLeaderboardPlayer, TechniqueLeaderboardPlayer, PeriodicLeaderboardPlayer
from .guild import LeaderboardGuild

from .utils import GAME_NAMES

__all__ = [
    "StatsLeaderboard",
    "LevelLeaderboard",
    "WeightedWinsLeaderboard",
    "TechniqueLeaderboard",
    "PeriodicLeaderboard",
    "GuildLeaderboard"
]

@dataclass
class StatsLeaderboard:
    _data: dict = field(repr=False)
    players: List[StatsLeaderboardPlayer] = field(default_factory=list)

    def __post_init__(self):
        for i in self._data:
            self.players.append(StatsLeaderboardPlayer(i))

@dataclass
class LevelLeaderboard(StatsLeaderboard):
    leaderboard: str = "level"

@dataclass
class WeightedWinsLeaderboard(StatsLeaderboard):
    leaderboard: str = "weightedwins"

@dataclass
class TechniqueLeaderboard:
    _data: dict = field(repr=False)
    players: List[StatsLeaderboardPlayer] = field(default_factory=list)

    def __post_init__(self):
        for i in self._data:
            self.players.append(TechniqueLeaderboardPlayer(i))

@dataclass
class PeriodicLeaderboard:
    _data: dict = field(repr=False)
    game: str = None
    type: str = None
    period: str = None
    players: List[PeriodicLeaderboardPlayer] = field(default_factory=list)

    def __post_init__(self):
        self.game = GAME_NAMES[self.game.lower()]

        for i in range(len(self._data)):
            self.players.append(PeriodicLeaderboardPlayer(self._data[i], position=i+1))

@dataclass
class GuildLeaderboard:
    _data: dict = field(repr=False)
    guilds: List[LeaderboardGuild] = field(default_factory=list)

    def __post_init__(self):
        for i in self._data:
            self.guilds.append(LeaderboardGuild(i))