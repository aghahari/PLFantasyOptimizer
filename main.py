import csv
from Entity.RunContext import RunContext
from Entity.Player import Player
from Entity.Team import Team
from Enum.Position import Position
from Optimizer.MathModel import MathModel
from Entity.Formation import Formation
from Enum.ObjectiveType import ObjectiveType


def createRunContext() -> RunContext:
    runContext = RunContext()
    with open('./Data/PL_Fantasy_Team_Data.csv', newline='') as csvFile:
        playerReader = csv.reader(csvFile)
        for player in playerReader:
            if player[1] == 'Team':
                continue
            team = Team(player[1])
            runContext.addTeam(team)
            position = Position(player[2])
            player = Player(player[0], runContext.teams[player[1]], position, *player[3:])
            runContext.addPlayer(player)
    return runContext


if __name__ == '__main__':
    runContext = createRunContext()
    mathModel = MathModel(Formation(3, 5, 2), ObjectiveType.MOST_POINT, runContext)
    mathModel.run()
