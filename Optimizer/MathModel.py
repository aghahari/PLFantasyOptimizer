from ortools.linear_solver import pywraplp
from typing import TYPE_CHECKING, List
from Enum.ObjectiveType import ObjectiveType
from Enum.Position import Position


if TYPE_CHECKING:
    from Entity.Formation import Formation
    from Entity.RunContext import RunContext
    from Entity.Team import Team


class MathModel:
    def __init__(self, formation: "Formation", objectiveType: ObjectiveType, runContext: "RunContext"):
        self.solver: pywraplp.Solver = pywraplp.Solver('PFL Solver', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.formation: "Formation" = formation
        self.objectiveType: ObjectiveType = objectiveType
        self.runContext: "RunContext" = runContext

    def run(self):
        self.__initialize()
        self.__createObjective()
        self.__createConstraints()
        self.__solve()
        self.__showResult()

    def __initialize(self):
        for player in self.runContext.players.values():
            player.initializeVariable(self)

    def __createObjective(self):
        coefficient = {}
        if self.objectiveType == ObjectiveType.MOST_POINT:
            coefficient = {player: player.points for player in self.runContext.players.values()}
        self.__mainObjective(coefficient)

    def __mainObjective(self, coefficient):
        objective = self.solver.Objective()
        for player in coefficient.keys():
            coeff = coefficient[player] + player.secondaryValue()
            objective.SetCoefficient(player.selectionVariable, coeff)
            objective.SetCoefficient(player.benchVariable, 0.5 * coeff)
        objective.SetMaximization()

    def __createConstraints(self):
        self.__formationConstraints()
        self.__teamConstraints()
        self.__budgetConstraint()
        self.__playerConstraints()

    def __playerConstraints(self):
        for player in self.runContext.players.values():
            ct = self.solver.Constraint(0, 1, f'ct_player_{player.key()}')
            ct.SetCoefficient(player.selectionVariable, 1.0)
            ct.SetCoefficient(player.benchVariable, 1.0)

    def __formationConstraints(self):
        self.__formationConstraint([Position.GOALKEEPER], self.formation.goalkeeper)
        self.__formationConstraint([Position.DEFENDER], self.formation.defenders)
        self.__formationConstraint([Position.MIDFIELDER], self.formation.midfielders)
        self.__formationConstraint([Position.ATTACKER], self.formation.attackers)
        self.__formationConstraint([Position.DEFENDER], 5 - self.formation.defenders, mainTeam=False)
        self.__formationConstraint([Position.MIDFIELDER], 5 - self.formation.midfielders, mainTeam=False)
        self.__formationConstraint([Position.ATTACKER], 3 - self.formation.attackers, mainTeam=False)
        self.__formationConstraint([Position.GOALKEEPER], 1, mainTeam=False)

    def __formationConstraint(self, positionList: List["Position"], limit: int, mainTeam: bool = True):
        allPlayers = [player for player in self.runContext.players.values() if player.position in positionList]
        ct = self.solver.Constraint(limit, limit)
        for player in allPlayers:
            ct.SetCoefficient(player.selectionVariable if mainTeam else player.benchVariable, 1.0)

    def __teamConstraints(self):
        for team in self.runContext.teams.values():
            self.__teamConstraint(team)

    def __teamConstraint(self, team: "Team", limit: int = 3):
        allPlayers = [player for player in self.runContext.players.values() if player.team == team]
        ct = self.solver.Constraint(0, limit)
        for player in allPlayers:
            ct.SetCoefficient(player.selectionVariable, 1.0)
            ct.SetCoefficient(player.benchVariable, 1.0)

    def __budgetConstraint(self, budget: float = 100.0):
        ct = self.solver.Constraint(0, budget, 'ct_budget')
        for player in self.runContext.players.values():
            ct.SetCoefficient(player.selectionVariable, player.price)
            ct.SetCoefficient(player.benchVariable, player.price)

    def __solve(self):
        self.solver.Solve()

    def __showResult(self):
        for player in self.runContext.players.values():
            if player.selectionVariable.solution_value() > 0.8:
                self.formation.addPlayer(player)
            if player.benchVariable.solution_value() > 0.8:
                self.formation.addPlayer(player, bench=True)
        self.formation.print()
