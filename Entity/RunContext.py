from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from Entity.Player import Player
    from Entity.Team import Team


class RunContext:
    def __init__(self):
        self.players: Dict[str: "Player"] = {}
        self.teams: Dict[str:"Team"] = {}

    def addPlayer(self, player: "Player"):
        if player.key() not in self.players.keys():
            self.players[player.key()] = player

    def addTeam(self, team: "Team"):
        if team.name not in self.teams.keys():
            self.teams[team.name] = team
