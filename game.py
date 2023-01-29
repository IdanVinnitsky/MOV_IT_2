
from player import Player

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

class Game:
    def __init__(self, id, start, end):
        self.id = id
        self.stat = start
        self.end = end
        self.winner = ""
        self.player0 = Player(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 'yellow')
        self.player1 = Player(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 'red')