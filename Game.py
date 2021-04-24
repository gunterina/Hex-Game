import sys
import pygame.mouse
from Grid import Grid


class Game:
    JMIN = None
    JMAX = None
    EMPTY = '.'

    def __init__(self):
        self.backgroundColor = (0, 0, 0)
        self.screenSize = (1280, 720)
        self.boardPosition = (250, 80)

        self.tileSize = 30
        self.NUM_ROWS = 11
        self.NUM_COLS = 11
        self.grid = Grid(
            self.NUM_ROWS,
            self.NUM_COLS,
            self.tileSize
        )

        # colours
        self.emptyColour = (70, 70, 70)
        self.playerColours = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255)
        }

        for tile in self.hexTiles():
            tile.colour = self.emptyColour

        self.matrix = [[self.__class__.EMPTY for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        self.currentPlayer = 'red'
        self.text = 'Red\'s turn'

    @classmethod
    def initialiseGame(cls, display, game):
        cls.display = display
        cls.tileSize = game.tileSize

    def hexTiles(self):
        return self.grid.tiles.values()

    def showMatrix(self):
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if j == 0:
                    print(' ' * i, end='')
                print(str(row[j]), end=' ')
            print()

    @classmethod
    def otherPlayer(cls, player):
        if player == cls.JMIN:
            return cls.JMAX
        return cls.JMIN

    def showText(self):
        fontObj = pygame.font.SysFont('arial', 40)
        renderedText = fontObj.render(self.text, True, (255, 255, 255))
        width = 400
        height = 100
        left = self.screenSize[0] / 2 - width / 2
        top = self.screenSize[1] - 1.3*height
        rectangle = pygame.Rect(left, top, width, height)
        rectangleText = renderedText.get_rect(center=rectangle.center)
        pygame.draw.rect(self.display, (0, 0, 0), rectangle)
        self.display.blit(renderedText, rectangleText)

    def makeMove(self):
        tile = self.getNearestTile(pygame.mouse.get_pos())
        tile.colour = self.playerColours[self.currentPlayer]
        x, y = tile.gridPosition
        self.matrix[y][x] = self.currentPlayer[0].upper()
        self.grid.visitedTiles[tile.gridPosition] = 1
        otherPlayer = self.otherPlayer(self.currentPlayer)
        self.text = otherPlayer.capitalize() + '\'s turn'
        return x, y

    def getNearestTile(self, pos):
        nearestTile = None
        minDist = sys.maxsize

        for tile in self.hexTiles():
            distance = tile.distanceSq(pos, self.boardPosition)
            if distance < minDist:
                minDist = distance
                nearestTile = tile
        return nearestTile

    def isValidMove(self):
        tile = self.getNearestTile(pygame.mouse.get_pos())
        return self.grid.visitedTiles[tile.gridPosition] == 0
