from random import choice, randint
import time, os, curses, copy

class Board:

    PIECES = [
        [(0, 3, 1), (0, 4, 5), (0, 5, 1), (0, 6, 1)],
        [(0, 3, 1), (0, 4, 5), (0, 5, 1), (1, 4, 1)],
        [(0, 4, 1), (0, 5, 5), (0, 6, 1), (1, 4, 1)],
        [(0, 3, 1), (0, 4, 5), (0, 5, 1), (1, 5, 1)],
        [(0, 4, 1), (0, 5, 1), (1, 4, 1), (1, 5, 1)],
        [(0, 3, 1), (0, 4, 1), (1, 4, 5), (1, 5, 1)],
        [(0, 5, 1), (0, 6, 1), (1, 4, 1), (1, 5, 5)],
    ]

    def __init__(self, window):
        self.grid = [[0 for j in range(10)] for i in range(20)]
        self.window = window
        self.turns = 0
        self.lost = False
        self.lineClears = 0
        self.next = randint(1, 7)
        self.autoChoice = True
        self.generateNewPiece()

    def getBoard(self):
        return copy.deepcopy(self.grid)
        
    def display(self):
        self.window.clear()
        self.window.addstr("\n |--------------------|\n")
        for row in self.grid:
            self.window.addstr(" |")
            for i in row:
                #self.window.addstr("{} ".format(i))
                self.window.addstr("{}".format("  " if i == 0 else "[]"))
            self.window.addstr("|\n")
        self.window.addstr(" |--------------------|\n")
        self.window.addstr("\n  " + "".join([("[]" if (-1, i, 1) in self.PIECES[self.next-1] or (-1, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " turns: " + str(self.turns))
        self.window.addstr("\n  " + "".join([("[]" if (0, i, 1) in self.PIECES[self.next-1] or (0, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " lost: " + str(self.lost))
        self.window.addstr("\n  " + "".join([("[]" if (1, i, 1) in self.PIECES[self.next-1] or (1, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " clears: " + str(self.lineClears))
        self.window.addstr("\n  " + "".join([("[]" if (2, i, 1) in self.PIECES[self.next-1] or (2, i, 5) in self.PIECES[self.next-1] else "  ") for i in range(3, 7)]) + " next: " + str(self.next))
        self.window.addstr("\n")

    def generateNewPiece(self):
        for loc in self.PIECES[self.next - 1]:
            self.grid[loc[0]][loc[1]] = loc[2]
        if self.autoChoice:
            self.next = randint(1, 7)

    def rotateActive(self):
        pivot = (-1, -1)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 5:
                    pivot = (i, j) #break
        if pivot[0] != -1:
            error = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 4:
                        if pivot[0] + j - pivot[1] > 19 or pivot[1] + pivot[0] - i > 9 or pivot[0] + j - pivot[1] < 0 or pivot[1] + pivot[0] - i < 0 or self.grid[pivot[0] + j - pivot[1]][pivot[1] + pivot[0] - i] == 2:
                            error = True #break
            if not error:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j] == 1 or self.grid[i][j] == 4:
                            self.grid[pivot[0] + j - pivot[1]][pivot[1] + pivot[0] - i] += 3
                            self.grid[i][j] -= 1
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        if self.grid[i][j] == 3 or self.grid[i][j] == 4:
                            self.grid[i][j] -= 2

    def translateActiveLeft(self):
        onLeft = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                    if j == 0 or self.grid[i][j-1] == 2:
                        onLeft = True #break
        if not onLeft:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                        self.grid[i][j-1] = self.grid[i][j]
                        self.grid[i][j] = 0

    def translateActiveRight(self):
        onRight = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                    if j == 9 or self.grid[i][j+1] == 2:
                        onRight = True #break
        if not onRight:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])-1, -1, -1):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                        self.grid[i][j+1] = self.grid[i][j]
                        self.grid[i][j] = 0

    def incrementTime(self):
        onBottom = False
        noneActive = True
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                    noneActive = False
                    if i == 19 or self.grid[i+1][j] == 2:
                        onBottom = True
        if noneActive:
            self.generateNewPiece()
        elif onBottom:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                        self.grid[i][j] = 2
            self.lineClear()
            if 2 in self.grid[0]: self.lost = True
        else:
            for i in range(len(self.grid)-1, -1, -1):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == 1 or self.grid[i][j] == 5:
                        self.grid[i+1][j] = self.grid[i][j]
                        self.grid[i][j] = 0
        self.turns += 1

    def lineClear(self):
        for i in range(len(self.grid)):
            if not (0 in self.grid[i]):
                for j in range(i, 0, -1):
                    self.grid[j] = self.grid[j-1]
                self.grid[0] = [0 for j in range(10)]
                self.lineClears += 1

class AI():

    def __init__(self):
        pass
    
    def move(self, state):
        choice = randint(1, 3)
        if choice == 1:
            state.translateActiveLeft()
        elif choice == 2:
            state.translateActiveRight()
        else:
            state.rotateActive()


def main(win):
    curses.noecho() #stop keys echoing to screen
    win.nodelay(True)
    
    board = Board(win)
    board.display()

    counter = int(time.time())
    while 1:
        try:
            key = win.getkey()
            if key == os.linesep or key == 'q':
                break
            if key == 's' or key == 'KEY_DOWN':
                board.incrementTime()
                board.display()
            if key == 'a' or key == 'KEY_LEFT':
                board.translateActiveLeft()
                board.display()
            if key == 'd' or key == 'KEY_RIGHT':
                board.translateActiveRight()
                board.display()
            if key == 'w' or key == 'KEY_UP':
                board.rotateActive()
                board.display()
            if key in ['{}'.format(i) for i in range(8)]:
                if key == '0':
                    board.autoChoice = True
                    board.next = randint(1, 7)
                else:
                    board.autoChoice = False
                    board.next = int(key)
                board.display()
        except Exception as e:
            # No input
            current = int(time.time())
            if counter < current:
                board.incrementTime()
                board.display()
                counter = current

if __name__ == '__main__':
    curses.wrapper(main)