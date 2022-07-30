from Enum.Position import Position


class Formation:
    def __init__(self, defenders: int, midfielders: int, attackers: int):
        self.goalkeeper: int = 1
        self.defenders: int = defenders
        self.midfielders: int = midfielders
        self.attackers: int = attackers
        self.bench: int = 3
        self.formation = {position: [] for position in Position}
        self.mainKeeper = None
        self.benchKeeper = None
        self.benchList = []
        if self.defenders + self.midfielders + self.attackers != 10:
            raise ValueError('The summation of the formation is not correct')

    def addPlayer(self, player, bench = False):
        if bench:
            if player.position == Position.GOALKEEPER:
                self.benchKeeper = player
                return
            self.benchList.append(player)
        else:
            self.formation[player.position].append(player)

    def print(self):
        for position in Position:
            print(f'{position}:\t {"--".join([player.key(False) for player in self.formation[position]])}')
        print(f'BENCH KEEPER:\t {self.benchKeeper.key(False) if self.benchKeeper else "NONE SELECTED"}')
        print(f'BENCH:\t{"--".join([player.key(False) for player in self.benchList])}')
