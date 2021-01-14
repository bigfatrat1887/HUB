import pygame
import sys


fps = 60
clock = pygame.time.Clock()


class Board():
    def __init__(self, width, height, cellsize=50):
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.board = [['-'] * self.width for _ in range(self.height)]
        self.left = 150
        self.top = 150

        self.rune = 'cross'
        self.player = 0

        self.win = False
        self.winner = None
        self.move = 0

    def draw(self):
        start_coord = [self.left, self.top]
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), [start_coord[0], start_coord[1], self.cellsize,
                                                                 self.cellsize], 1)
                start_coord[0] += self.cellsize
            start_coord[0] = self.left
            start_coord[1] += self.cellsize
        pygame.draw.line(screen, 'blue', (5, 5), (self.cellsize - 5, self.cellsize - 5), 2)
        pygame.draw.line(screen, 'blue', (5, self.cellsize - 5), (self.cellsize - 5, 5), 2)

    def coord(self, position):
        first = ((position[0] - self.left) // self.cellsize)
        second = ((position[1] - self.top) // self.cellsize)
        if 0 <= first < len(self.board[0]) and 0 <= second < len(self.board):
            return first, second
        else:
            return None

    def cross_zero(self, pos):
        if self.win:
            return False
        if not pos == None:
            x, y = pos
            start_coord = [self.left + self.cellsize * x, self.top + self.cellsize * y]
            if self.board[y][x] == '-':
                if self.rune == 'cross':
                    pygame.draw.line(screen, pygame.Color('blue'), (start_coord[0] + 2, start_coord[1] + 2),
                                     (start_coord[0] - 2 + self.cellsize, start_coord[1] - 2 + self.cellsize), 2)
                    pygame.draw.line(screen, pygame.Color('blue'), (start_coord[0] + 2,
                                                                    start_coord[1] + self.cellsize - 2),
                                     (start_coord[0] - 2 + self.cellsize, start_coord[1] + 2), 2)
                    self.board[y][x] = 'x'
                    self.rune = 'zero'
                    pygame.draw.rect(screen, 'black', (0, 0, self.cellsize + 5, self.cellsize + 5))
                    pygame.draw.circle(screen, pygame.Color('red'), (self.cellsize // 2, self.cellsize // 2),
                                       self.cellsize // 2 - 2, 2)
                elif self.rune == 'zero':
                    pygame.draw.circle(screen, pygame.Color('red'), (start_coord[0] + self.cellsize // 2,
                                                                     start_coord[1] + self.cellsize // 2),
                                       self.cellsize // 2 - 2, 2)
                    self.board[y][x] = 'o'
                    self.rune = 'cross'
                    pygame.draw.rect(screen, 'black', (0, 0, self.cellsize + 5, self.cellsize + 5))
                    pygame.draw.line(screen, 'blue', (5, 5), (self.cellsize - 5, self.cellsize - 5), 2)
                    pygame.draw.line(screen, 'blue', (5, self.cellsize - 5), (self.cellsize - 5, 5), 2)
                if self.chech_win():
                    pygame.display.flip()
                    self.game_over()
                return True
        return False


    def chech_win(self):
        if self.win:
            return True

        if self.board[0].count('x') == 3 or self.board[1].count('x') == 3 or self.board[2].count('x') == 3:
            self.winner = 'x'
        elif self.board[0].count('o') == 3 or self.board[1].count('o') == 3 or self.board[2].count('o') == 3:
            self.winner = 'o'
        elif self.board[0][0] == self.board[0][1] == self.board[0][2]:
            if self.board[0][0] == 'x':
                self.winner = 'x'
            elif self.board[0][0] == 'o':
                self.winner = 'o'
        elif self.board[1][0] == self.board[1][1] == self.board[1][2]:
            if self.board[1][0] == 'x':
                self.winner = 'x'
            elif self.board[1][0] == 'o':
                self.winner = 'o'
        elif self.board[2][0] == self.board[2][1] == self.board[2][2]:
            if self.board[2][0] == 'x':
                self.winner = 'x'
            elif self.board[2][0] == 'o':
                self.winner = 'o'
        elif self.board[0][0] == self.board[1][0] == self.board[2][0]:
            if self.board[0][0] == 'x':
                self.winner = 'x'
            elif self.board[0][0] == 'o':
                self.winner = 'o'
        elif self.board[0][1] == self.board[1][1] == self.board[2][1]:
            if self.board[0][1] == 'x':
                self.winner = 'x'
            elif self.board[0][1] == 'o':
                self.winner = 'o'
        elif self.board[0][2] == self.board[1][2] == self.board[2][2]:
            if self.board[0][2] == 'x':
                self.winner = 'x'
            elif self.board[0][2] == 'o':
                self.winner = 'o'
        elif self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == 'x':
                self.winner = 'x'
            elif self.board[0][0] == 'o':
                self.winner = 'o'
        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 'x':
                self.winner = 'x'
            elif self.board[0][2] == 'o':
                self.winner = 'o'
        elif self.board[0].count('-') == 0 and self.board[1].count('-') == 0 and self.board[2].count('-') == 0:
            self.winner = '-'

        if not (self.winner is None):
            self.win = True
            return True

    def game_over(self):
        clock.tick(3)
        screen.fill('black')
        font = pygame.font.Font(None, 100)

        if self.winner == 'x':
            text = font.render('"X" is winner', True, (0, 0, 255))

        elif self.winner == 'o':
            text = font.render('"O" is winner', True, (225, 0, 0))

        elif self.winner == '-':
            text = font.render('ничья', True, (0, 255, 0))

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        font_1 = pygame.font.Font(None, 50)
        text_reset = font_1.render('заново', True, (100, 200, 100))
        screen.blit(text_reset, (190, 335))
        pygame.draw.rect(screen, (100, 200, 100), (185, 337, 131, 35), 1)

    def reset(self):
        self.board = [['-'] * self.width for _ in range(self.height)]
        self.move = 0
        self.rune = 'cross'
        self.player = 0
        self.win = False
        self.winner = None

    def move_selection(self):
        pygame.draw.line(screen, 'green', (240, 100), (240, 380), 2)
        font = pygame.font.Font(None, 300)
        text = font.render('2', True, (0, 0, 255))
        text_x = 110
        text_y = 160
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 300)
        text = font.render('1', True, (255, 0, 0))
        text_x = 270
        text_y = 160
        screen.blit(text, (text_x, text_y))

    def opponent(self):
        if self.player == 'o':
            self.opozition = 'x'
            self.move += 1
            if self.move == 1:
                if self.player in self.board[1][0] or self.player in self.board[2][0] or\
                        self.player in self.board[2][1]:
                    self.cross_zero((2, 0))
                elif self.player in self.board[0][1] or self.player in self.board[0][2] or\
                        self.player in self.board[1][2]:
                    self.cross_zero((0, 2))
                elif self.player in self.board[2][2]:
                    self.cross_zero((2, 0))
                elif self.player in self.board[1][1]:
                    self.cross_zero((2, 2))
            elif self.move == 2:
                if self.board[2][0] == self.opozition and self.board[1][0] == '-':
                    self.cross_zero((0, 1))
                if self.board[0][2] == self.opozition and self.board[0][1] == '-':
                    self.cross_zero((1, 0))
                elif self.board[1].count(self.player) == 2 and self.board[1].count(self.opozition) == 0:
                    if self.board[1][0] == '-':
                        self.cross_zero((0, 1))
                    elif self.board[1][1] == '-':
                        self.cross_zero((1, 1))
                    else:
                        self.cross_zero((2, 1))
                elif self.board[0][1] == self.board[1][1] == self.player:
                    self.cross_zero((1, 2))
                elif self.board[1][1] == self.board[2][1] == self.player:
                    self.cross_zero((1, 0))
                elif self.board[0][1] == self.board[2][1] == self.player:
                    self.cross_zero((1, 1))
                elif self.player == self.board[0][1] and self.player == self.board[1][0]:
                    self.cross_zero((1, 1))
                elif self.board[2][2] == '-':
                    self.cross_zero((2, 2))
                elif self.board[2][0] == '-':
                    self.cross_zero((0, 2))
                elif self.board[0][2] == '-':
                    self.cross_zero((2, 0))
            elif self.move == 3:
                if self.board[1][0] == self.opozition and self.board[2][0] == '-':
                    self.cross_zero((0, 2))
                elif self.board[1][0] == '-' and self.board[2][0] == self.opozition:
                    self.cross_zero((0, 1))
                elif self.board[0][2] == self.board[2][2] == self.opozition and self.board[1][2] == '-':
                    self.cross_zero((2, 1))
                elif self.board[0][2] == self.board[1][2] == self.opozition and self.board[2][2] == '-':
                    self.cross_zero((2, 2))
                elif self.board[1][2] == self.board[2][2] == self.opozition and self.board[0][2] == '-':
                    self.cross_zero((2, 0))
                elif self.board[2].count(self.opozition) == 2 and self.board[2].count(self.player) == 0:
                    if self.board[2][0] == '-':
                        self.cross_zero((0, 2))
                    elif self.board[2][1] == '-':
                        self.cross_zero((1, 2))
                    else:
                        self.cross_zero((2, 2))
                elif self.board[2][0] == self.opozition and self.board[1][0] == '-':
                    self.cross_zero((0, 1))
                elif self.board[0][2] == self.opozition and self.board[0][1] == '-':
                    self.cross_zero((1, 0))
                elif self.board[1].count(self.player) == 2 and self.board[1].count(self.opozition) == 0:
                    if self.board[1][0] == '-':
                        self.cross_zero((0, 1))
                    elif self.board[1][1] == '-':
                        self.cross_zero((1, 1))
                    else:
                        self.cross_zero((2, 1))
                elif self.board[0][0] == self.board[1][1] == self.opozition and self.board[2][2] == '-':
                    self.cross_zero((2, 2))
                elif self.board[0][0] == self.board[2][2] == self.opozition and self.board[1][1] == '-':
                    self.cross_zero((1, 1))
                elif self.board[0][1] == self.board[1][1] == self.opozition and self.board[2][1] == '-':
                    self.cross_zero((1, 2))
                elif self.board[0][1] == self.board[2][1] == self.opozition and self.board[1][1] == '-':
                    self.cross_zero((1, 1))
                elif self.board[2][1] == self.board[1][1] == self.opozition and self.board[0][1] == '-':
                    self.cross_zero((1, 0))
                elif (self.board[2][0] == self.board[1][1] == self.opozition or
                      self.board[2][0] == self.board[1][1] == self.player) and self.board[0][2] == '-':
                    self.cross_zero((2, 0))
                elif (self.board[0][2] == self.board[2][0] == self.opozition or
                      self.board[0][2] == self.board[2][0] == self.player) and self.board[1][1] == '-':
                    self.cross_zero((1, 1))
                elif (self.board[0][2] == self.board[1][1] == self.opozition or
                      self.board[0][2] == self.board[1][1] == self.player) and self.board[2][0] == '-':
                    self.cross_zero((0, 2))
                elif self.board[2][0] == '-':
                    self.cross_zero((0, 2))
                else:
                    rune_guard = False
                    for i in range(3):
                        for j in range(3):
                            if self.board[i][j] == '-':
                                self.cross_zero((j, i))
                                rune_guard = True
                                break
                        if rune_guard:
                            break
            else:
                rune_guard = False
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == '-':
                            self.cross_zero((j, i))
                            rune_guard = True
                            break
                    if rune_guard:
                        break
        elif self.player == 'x':
            pass

Board_1 = Board(3, 3)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))
    pygame.display.set_caption('Крестики-нолики')
    Board_1.move_selection()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not Board_1.player:
                    if event.pos[1] in range(110, 380):
                        if event.pos[0] in range(70, 240):
                            Board_1.player = 'x'
                            screen.fill('black')
                            Board_1.draw()
                        elif event.pos[0] in range(240, 410):
                            Board_1.player = 'o'
                            screen.fill('black')
                            Board_1.draw()
                            Board_1.cross_zero((0, 0))

                else:
                    if Board_1.cross_zero(Board_1.coord(event.pos)):
                        Board_1.opponent()
                    if Board_1.chech_win():
                        if event.pos[0] in range(185, 185 + 131) and event.pos[1] in range(337, 337 + 35):
                            screen.fill('black')
                            Board_1.reset()
                            Board_1.move_selection()
        clock.tick(fps)
        pygame.display.flip()
    sys.exit()
