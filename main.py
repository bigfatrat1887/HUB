import pygame
import sys

fps = 60
clock = pygame.time.Clock()


class Board():
    def __init__(self, width, height, cellsize=50):
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.board = [['-'] * width for _ in range(height)]
        self.turn = 'r'
        self.enemy = 'b'

        self.list_move = []
        self.left = 80
        self.top = 80

    def draw(self):
        start_coord = [self.left, self.top]
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), [start_coord[0], start_coord[1], self.cellsize,
                                                                 self.cellsize], 1)
                start_coord[0] += self.cellsize
            start_coord[0] = self.left
            start_coord[1] += self.cellsize

        pygame.draw.circle(screen, 'red', (self.left + self.cellsize * 3 + self.cellsize // 2,
                                                         self.top + self.cellsize * 3 + self.cellsize // 2),
                           self.cellsize // 2 - 2)
        self.board[3][3] = 'r'
        pygame.draw.circle(screen, 'red', (self.left + self.cellsize * 4 + self.cellsize // 2,
                                                         self.top + self.cellsize * 4 + self.cellsize // 2),
                           self.cellsize // 2 - 2)
        self.board[4][4] = 'r'
        pygame.draw.circle(screen, 'blue', (self.left + self.cellsize * 3 + self.cellsize // 2,
                                                         self.top + self.cellsize * 4 + self.cellsize // 2),
                           self.cellsize // 2 - 2)
        self.board[3][4] = 'b'

        pygame.draw.circle(screen, 'blue', (self.left + self.cellsize * 4 + self.cellsize // 2,
                                                         self.top + self.cellsize * 3 + self.cellsize // 2),
                           self.cellsize // 2 - 2)
        self.board[4][3] = 'b'

        pygame.draw.circle(screen, 'red', (self.cellsize // 2 + 5, self.cellsize // 2 + 5),
                           self.cellsize // 2)

    def coord(self, position):
        first = ((position[0] - self.left) // self.cellsize)
        second = ((position[1] - self.top) // self.cellsize)
        if 0 <= first < len(self.board[0]) and 0 <= second < len(self.board):
            return first, second
        else:
            return None

    def move(self, pos):
        if not pos == None:
            x, y = pos
            if [y, x] in self.list_move:
                if self.turn == 'r':
                    color = 'red'
                elif self.turn == 'b':
                    color = 'blue'
                pygame.draw.circle(screen, color, (self.left + self.cellsize * x + self.cellsize // 2,
                                                   self.top + self.cellsize * y + self.cellsize // 2),
                                   self.cellsize // 2 - 2)

                self.board[y][x] = self.turn
                for i in self.check_vertical(x, y):
                    self.board[i[1]][i[0]] = self.turn
                    pygame.draw.circle(screen, color, (self.left + self.cellsize * i[0] + self.cellsize // 2,
                                                       self.top + self.cellsize * i[1] + self.cellsize // 2),
                                       self.cellsize // 2 - 2)

                for j in self.check_horizontal(x, y):
                    self.board[j[1]][j[0]] = self.turn
                    pygame.draw.circle(screen, color, (self.left + self.cellsize * j[0] + self.cellsize // 2,
                                                       self.top + self.cellsize * j[1] + self.cellsize // 2),
                                       self.cellsize // 2 - 2)

                for q in self.check_diagonal(x, y):
                    self.board[q[1]][q[0]] = self.turn
                    pygame.draw.circle(screen, color, (self.left + self.cellsize * q[0] + self.cellsize // 2,
                                                       self.top + self.cellsize * q[1] + self.cellsize // 2),
                                       self.cellsize // 2 - 2)

                if self.turn == 'r':
                    self.turn = 'b'
                    self.enemy = 'r'
                    pygame.draw.circle(screen, 'blue', (self.cellsize // 2 + 5, self.cellsize // 2 + 5),
                                       self.cellsize // 2)
                elif self.turn == 'b':
                    self.turn = 'r'
                    self.enemy = 'b'
                    pygame.draw.circle(screen, 'red', (self.cellsize // 2 + 5, self.cellsize // 2 + 5),
                                       self.cellsize // 2)

    def check_vertical(self, x, y):
        list_point = []

        for i in range(y + 1, self.height):
            if self.board[i][x] == self.enemy:
                list_point.append([x, i])
            else:
                if self.board[i][x] == '-':
                    list_point = []
                break
            if i + 1 == self.height:
                list_point = []
                break
        limit = len(list_point)

        for i in range(y - 1, -1, -1):
            if self.board[i][x] == self.enemy:
                list_point.append([x, i])
            else:
                if self.board[i][x] == '-':
                    list_point = list_point[:limit]
                break
            if i == 0:
                list_point = list_point[:limit]
                break

        return list_point

    def check_horizontal(self, x, y):
        list_point = []
        x_R = x
        if x_R != 7:
            while self.board[y][x_R + 1] == self.enemy:
                x_R += 1
                list_point.append([x_R, y])
                if x_R == self.width - 1:
                    list_point = []
                    break
                if self.board[y][x_R + 1] == '-':
                    list_point = []
                    break
        limit = len(list_point)
        for i in range(x - 1, -1, -1):
            if self.board[y][i] == self.enemy:
                if i != 0:
                    list_point.append([i, y])
                else:
                    list_point = list_point[:limit]
            else:
                if self.board[y][i] == '-':
                    list_point = list_point[:limit]
                break
        return list_point

    def check_diagonal(self, x, y):
        rune_1 = True
        rune_2 = True
        rune_3 = True
        rune_4 = True

        list_point_1 = []
        list_point_2 = []
        list_point_3 = []
        list_point_4 = []

        for i in range(1, 8):
            if rune_1:
                if y + i < self.height and x + i < self.width:
                    if self.board[y + i][x + i] == self.enemy:
                        list_point_1.append([x + i, y + i])
                    else:
                        if self.board[y + i][x + i] == '-':
                            list_point_1 = []
                        rune_1 = False
                else:
                    list_point_1 = []
                    rune_1 = False

            if rune_2:
                if y - i >= 0 and x + i < self.width:
                    if self.board[y - i][x + i] == self.enemy:
                        list_point_2.append([x + i, y - i])
                    else:
                        if self.board[y - i][x + i] == '-':
                            list_point_2 = []
                        rune_2 = False
                else:
                    list_point_2 = []
                    rune_2 = False
            if rune_3:
                if y + i < self.height and x - i >= 0:
                    if self.board[y + i][x - i] == self.enemy:
                        list_point_3.append([x - i, y + i])
                    else:
                        if self.board[y + i][x - i] == '-':
                            list_point_3 = []
                        rune_3 = False
                else:
                    list_point_3 = []
                    rune_3 = False

            if rune_4:
                if y - i >= 0 and x - i >= 0:
                    if self.board[y - i][x - i] == self.enemy:
                        if y - i == 0 or x - i == 0:
                            list_point_4 = []
                            rune_4 = False
                        else:
                            list_point_4.append([x - i, y - i])
                    else:
                        if self.board[y - i][x - i] == '-':
                            list_point_4 = []
                        rune_4 = False
                else:
                    list_point_4 = []
                    rune_4 = False

        list_point = []

        if list_point_1:
            list_point = list_point_1

        if list_point_2:
            for i in list_point_2:
                list_point.append(i)

        if list_point_3:
            for i in list_point_3:
                list_point.append(i)

        if list_point_4:
            for i in list_point_4:
                list_point.append(i)

        return list_point

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if y + i < self.height and x + j < self.width and y + i >= 0 and x + j >= 0:
                    if self.board[y + i][x + j] == self.enemy:
                        if i == 0 and j == 0:
                            pass
                        else:
                            neighbors += 1

        return neighbors

    def show_move(self):
        self.list_move = []
        for i in range(self.height):    # Y
            for j in range(self.width):    # X
                if self.get_neighbors((j, i)) and self.board[i][j] == '-':
                    if self.check_diagonal(j, i) or self.check_vertical(j, i) or self.check_horizontal(j, i):
                        self.list_move.append([i, j])

    def check_win(self):
        screen.fill('black')
        red_points = 0
        blue_points = 0
        for j in self.board:
            for i in j:
                if i == 'r':
                    red_points += 1
                elif i == 'b':
                    blue_points += 1

        font = pygame.font.Font(None, 100)
        if red_points > blue_points:
            text = font.render('RED is winner', True, (255, 0, 0))
        elif red_points < blue_points:
            text = font.render('BLUE is winner', True, (0, 0, 255))
        else:
            text = font.render('НИЧЬЯ', True, (0, 255, 0))

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        font_1 = pygame.font.Font(None, 50)
        text_reset = font_1.render('заново', True, (100, 200, 100))
        screen.blit(text_reset, (215, 366))
        pygame.draw.rect(screen, (100, 200, 100), (210, 366, 131, 35), 1)

    def reset(self):
        self.board = [['-'] * width for _ in range(height)]
        self.turn = 'r'
        self.enemy = 'b'
        self.list_move = []


Board_1 = Board(8, 8)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))
    pygame.display.set_caption('Реверси')
    Board_1.draw()
    Board_1.show_move()
    running = True
    rune_win = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Board_1.move(Board_1.coord(event.pos))
                Board_1.show_move()
                if not Board_1.list_move:
                    Board_1.check_win()
                    rune_win = True
                if rune_win:
                    if event.pos[0] in range(210, 210 + 131) and event.pos[1] in range(366, 366 + 35):
                        Board_1.reset()
                        Board_1.draw()
                        Board_1.show_move()
                        rune_win = False

        clock.tick(fps)
        pygame.display.flip()
    sys.exit()