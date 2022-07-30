from typing import TYPE_CHECKING, Optional
from ortools.linear_solver import pywraplp
if TYPE_CHECKING:
    from Entity import Team
    from Enum import Position
    from Optimizer.MathModel import MathModel


class Player:
    def __init__(self, name: str, team: "Team", position: "Position", price: float, pick: float = 0.0, minutes: int = 0,
                 points: int = 0, goals: int = 0, assists: int = 0, bonus: int = 0, bps: float = 0.0):
        self.name: str = name
        self.team: "Team" = team
        self.position: "Position" = position
        self.price: float = float(str(price).replace('Â£', '').replace('M', ''))
        self.pick: float = float(str(pick).replace('%', ''))
        self.minutes: int = int(minutes)
        self.points: int = int(points)
        self.goals: int = int(goals)
        self.assists: int = int(assists)
        self.bonus: int = int(bonus)
        self.bps: float = float(bps)
        self.selectionVariable: Optional[pywraplp.Variable] = None
        self.benchVariable: Optional[pywraplp.Variable] = None

    def initializeVariable(self, model: "MathModel") -> None:
        self.selectionVariable = model.solver.IntVar(0, 1, f'main_select_{self.key()}')
        self.benchVariable = model.solver.IntVar(0, 1, f'bench_select_{self.key()}')

    def key(self, price:bool = True) -> str:
        firstP = f"{self.name}({self.team.name})({self.position.name})"
        secondP = f"({self.price})" if price else ''
        return firstP + secondP

    def secondaryValue(self) -> float:
        return 0.01 * (self.points + self.goals + self.assists + self.pick + self.minutes)
