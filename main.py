import pygame
import random
import sys


fps = 15
clock = pygame.time.Clock()


class Board:
    def __init__(self, width=8, height=8, cellsize=50):
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.board = [['-'] * width for _ in range(height)]

        self.left = 0
        self.top = 0
        self.tremor = 1
        self.count = 0

        self.color_dict = {'g': 'green', 'p': 'purple', 'o': 'orange', 'r': 'red', 't': 'turquoise'}

    def draw(self):
        start_coord = [self.left, self.top]
        color_list = ['g', 'p', 'o', 'r', 't']
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, 'grey', [start_coord[0], start_coord[1], self.cellsize,
                                                                 self.cellsize], 1)
                color_balls = random.choice(color_list)
                self.board[i][j] = color_balls

                while self.check_neighbors((j, i)):
                    color_balls = random.choice(color_list)
                    self.board[i][j] = color_balls

                pygame.draw.circle(screen, self.color_dict[color_balls], [start_coord[0] + self.cellsize // 2,
                                                                     start_coord[1] + self.cellsize // 2],
                                   self.cellsize // 2 - 5)

                self.board[i][j] = color_balls
                start_coord[0] += self.cellsize
            start_coord[0] = self.left
            start_coord[1] += self.cellsize

    def coord(self, position):
        first = ((position[0] - self.left) // self.cellsize)
        second = ((position[1] - self.top) // self.cellsize)
        if 0 <= first < len(self.board[0]) and 0 <= second < len(self.board):
            return first, second
        else:
            return None

    def check_neighbors(self, pos):
        x, y = pos

        bottom = False
        if y + 2 < self.height:
            if self.board[y][x] == self.board[y + 1][x] == self.board[y + 2][x]:
                bottom = True
        top = False
        if y - 2 >= 0:
            if self.board[y - 2][x] == self.board[y - 1][x] == self.board[y][x]:
                top = True
        center_vertical = False
        if 0 < y < self.height - 1:
            if self.board[y - 1][x] == self.board[y][x] == self.board[y + 1][x]:
                center_vertical = True
        right = False
        if x + 2 < self.width:
            if self.board[y][x] == self.board[y][x + 1] == self.board[y][x + 2]:
                right = True
        left = False
        if x - 2 >= 0:
            if self.board[y][x - 2] == self.board[y][x - 1] == self.board[y][x]:
                left = True
        center_horizontal = False
        if 0 < x < self.width - 1:
            if self.board[y][x - 1] == self.board[y][x] == self.board[y][x + 1]:
                center_horizontal = True
        result = []
        if top:
            result.append('T')
        if bottom:
            result.append('B')
        if center_vertical:
            result.append('C_V')
        if left:
            result.append('L')
        if right:
            result.append('R')
        if center_horizontal:
            result.append('C_H')
        if result:
            return result
        else:
            return False

    def wait_move(self, pos, rune=False):
        x, y = pos
        pygame.draw.rect(screen, 'black', (self.cellsize * x + 2, self.cellsize * y + 2, self.cellsize - 2,
                                           self.cellsize - 2))

        if rune:
            pygame.draw.circle(screen, self.color_dict[self.board[y][x]], [self.cellsize * x + self.cellsize // 2,
                                                                      self.cellsize * y + self.cellsize // 2],
                               self.cellsize // 2 - 5)
            self.tremor = 1
        else:
            if self.tremor == 1:
                self.direction = -1
                self.tremor = 0
                pygame.draw.circle(screen, self.color_dict[self.board[y][x]], [self.cellsize * x + self.cellsize // 2,
                                                                          self.cellsize * y + self.cellsize // 2 - 3],
                                   self.cellsize // 2 - 5)
            elif self.tremor == 0:
                if self.direction == 1:
                    self.tremor = 1
                elif self.direction == -1:
                    self.tremor = -1
                pygame.draw.circle(screen, self.color_dict[self.board[y][x]], [self.cellsize * x + self.cellsize // 2,
                                                                          self.cellsize * y + self.cellsize // 2],
                                   self.cellsize // 2 - 5)
            elif self.tremor == -1:
                self.direction = 1
                self.tremor = 0
                pygame.draw.circle(screen, self.color_dict[self.board[y][x]], [self.cellsize * x + self.cellsize // 2,
                                                                          self.cellsize * y + self.cellsize // 2 + 3],
                                   self.cellsize // 2 - 5)

    def move(self, pos_1, pos_2):
        if pos_1 != pos_2:
            if ((pos_1[0] - pos_2[0] == 1 or pos_1[0] - pos_2[0] == -1) and pos_1[1] == pos_2[1]) or \
                    ((pos_1[1] - pos_2[1] == 1 or pos_1[1] - pos_2[1] == -1) and pos_1[0] == pos_2[0]):
                if pos_1[0] != pos_2[0]:
                    if pos_1[0] > pos_2[0]:
                        step = -5
                    else:
                        step = 5
                    for i in range(1, 11):
                        pygame.draw.rect(screen, 'black',
                                         (self.cellsize * pos_1[0] + 2, self.cellsize * pos_1[1] + 2,
                                          self.cellsize - 2, self.cellsize - 2))
                        pygame.draw.rect(screen, 'black',
                                         (self.cellsize * pos_2[0] + 2, self.cellsize * pos_2[1] + 2,
                                          self.cellsize - 2, self.cellsize - 2))
                        pygame.draw.circle(screen, self.color_dict[self.board[pos_1[1]][pos_1[0]]],
                                           [self.cellsize * pos_1[0] + self.cellsize // 2 + step * i,
                                            self.cellsize * pos_1[1] + self.cellsize // 2],
                                           self.cellsize // 2 - 5)
                        pygame.draw.circle(screen, self.color_dict[self.board[pos_2[1]][pos_2[0]]],
                                           [self.cellsize * pos_2[0] + self.cellsize // 2 - step * i,
                                            self.cellsize * pos_2[1] + self.cellsize // 2],
                                           self.cellsize // 2 - 5)
                        pygame.display.flip()
                    pygame.draw.line(screen, 'grey', (pos_1[0] * self.cellsize, pos_1[1] * self.cellsize),
                                     (pos_1[0] * self.cellsize, (pos_1[1] + 1) * self.cellsize), 2)
                    pygame.draw.line(screen, 'grey', (pos_2[0] * self.cellsize, pos_2[1] * self.cellsize),
                                     (pos_2[0] * self.cellsize, (pos_2[1] + 1) * self.cellsize), 2)
                    self.board[pos_1[1]][pos_1[0]], self.board[pos_2[1]][pos_2[0]], = self.board[pos_2[1]][pos_2[0]], \
                                                                                      self.board[pos_1[1]][pos_1[0]]
                elif pos_1[1] != pos_2[1]:
                    if pos_1[1] > pos_2[1]:
                        step = -5
                    else:
                        step = 5
                    for i in range(1, 11):
                        pygame.draw.rect(screen, 'black',
                                         (self.cellsize * pos_1[0] + 2, self.cellsize * pos_1[1] + 2,
                                          self.cellsize - 2, self.cellsize - 2))
                        pygame.draw.rect(screen, 'black',
                                         (self.cellsize * pos_2[0] + 2, self.cellsize * pos_2[1] + 2,
                                          self.cellsize - 2, self.cellsize - 2))
                        pygame.draw.circle(screen, self.color_dict[self.board[pos_1[1]][pos_1[0]]],
                                           [self.cellsize * pos_1[0] + self.cellsize // 2,
                                            self.cellsize * pos_1[1] + self.cellsize // 2 + step * i],
                                           self.cellsize // 2 - 5)
                        pygame.draw.circle(screen, self.color_dict[self.board[pos_2[1]][pos_2[0]]],
                                           [self.cellsize * pos_2[0] + self.cellsize // 2,
                                            self.cellsize * pos_2[1] + self.cellsize // 2 - step * i],
                                           self.cellsize // 2 - 5)
                        pygame.display.flip()
                    pygame.draw.line(screen, 'grey', (pos_1[0] * self.cellsize, pos_1[1] * self.cellsize),
                                     ((pos_1[0] + 1) * self.cellsize, pos_1[1] * self.cellsize), 2)
                    pygame.draw.line(screen, 'grey', (pos_2[0] * self.cellsize, pos_2[1] * self.cellsize),
                                     ((pos_2[0] + 1) * self.cellsize, pos_2[1] * self.cellsize), 2)
                    self.board[pos_1[1]][pos_1[0]], self.board[pos_2[1]][pos_2[0]] = self.board[pos_2[1]][pos_2[0]], \
                                                                                      self.board[pos_1[1]][pos_1[0]]
                retired_1 = self.calculation_retired(pos_1)
                retired_2 = self.calculation_retired(pos_2)
                if retired_1 or retired_2:
                    if retired_1:
                        retired_1 = self.rebuild(retired_1)
                        for i in retired_1:
                            self.change_row(i)
                    if retired_2:
                        retired_2 = self.rebuild(retired_2)
                        for i in retired_2:
                            self.change_row(i)

                    while self.check():
                        self.check()

                    return True
                else:
                    if pos_1[0] != pos_2[0]:
                        if pos_1[0] > pos_2[0]:
                            step = -5
                        else:
                            step = 5
                        for i in range(1, 11):
                            pygame.draw.rect(screen, 'black',
                                             (self.cellsize * pos_1[0] + 2, self.cellsize * pos_1[1] + 2,
                                              self.cellsize - 2, self.cellsize - 2))
                            pygame.draw.rect(screen, 'black',
                                             (self.cellsize * pos_2[0] + 2, self.cellsize * pos_2[1] + 2,
                                              self.cellsize - 2, self.cellsize - 2))
                            pygame.draw.circle(screen, self.color_dict[self.board[pos_1[1]][pos_1[0]]],
                                               [self.cellsize * pos_1[0] + self.cellsize // 2 + step * i,
                                                self.cellsize * pos_1[1] + self.cellsize // 2],
                                               self.cellsize // 2 - 5)
                            pygame.draw.circle(screen, self.color_dict[self.board[pos_2[1]][pos_2[0]]],
                                               [self.cellsize * pos_2[0] + self.cellsize // 2 - step * i,
                                                self.cellsize * pos_2[1] + self.cellsize // 2],
                                               self.cellsize // 2 - 5)
                            pygame.display.flip()
                        pygame.draw.line(screen, 'grey', (pos_1[0] * self.cellsize, pos_1[1] * self.cellsize),
                                         (pos_1[0] * self.cellsize, (pos_1[1] + 1) * self.cellsize), 2)
                        pygame.draw.line(screen, 'grey', (pos_2[0] * self.cellsize, pos_2[1] * self.cellsize),
                                         (pos_2[0] * self.cellsize, (pos_2[1] + 1) * self.cellsize), 2)
                        self.board[pos_1[1]][pos_1[0]], self.board[pos_2[1]][pos_2[0]] = \
                            self.board[pos_2[1]][pos_2[0]], self.board[pos_1[1]][pos_1[0]]
                    elif pos_1[1] != pos_2[1]:
                        if pos_1[1] > pos_2[1]:
                            step = -5
                        else:
                            step = 5
                        for i in range(1, 11):
                            pygame.draw.rect(screen, 'black',
                                             (self.cellsize * pos_1[0] + 2, self.cellsize * pos_1[1] + 2,
                                              self.cellsize - 2, self.cellsize - 2))
                            pygame.draw.rect(screen, 'black',
                                             (self.cellsize * pos_2[0] + 2, self.cellsize * pos_2[1] + 2,
                                              self.cellsize - 2, self.cellsize - 2))
                            pygame.draw.circle(screen, self.color_dict[self.board[pos_1[1]][pos_1[0]]],
                                               [self.cellsize * pos_1[0] + self.cellsize // 2,
                                                self.cellsize * pos_1[1] + self.cellsize // 2 + step * i],
                                               self.cellsize // 2 - 5)
                            pygame.draw.circle(screen, self.color_dict[self.board[pos_2[1]][pos_2[0]]],
                                               [self.cellsize * pos_2[0] + self.cellsize // 2,
                                                self.cellsize * pos_2[1] + self.cellsize // 2 - step * i],
                                               self.cellsize // 2 - 5)
                            pygame.display.flip()
                        pygame.draw.line(screen, 'grey', (pos_1[0] * self.cellsize, pos_1[1] * self.cellsize),
                                         ((pos_1[0] + 1) * self.cellsize, pos_1[1] * self.cellsize), 2)
                        pygame.draw.line(screen, 'grey', (pos_2[0] * self.cellsize, pos_2[1] * self.cellsize),
                                         ((pos_2[0] + 1) * self.cellsize, pos_2[1] * self.cellsize), 2)
                        self.board[pos_1[1]][pos_1[0]], self.board[pos_2[1]][pos_2[0]] = self.board[pos_2[1]][pos_2[0]], \
                                                                                         self.board[pos_1[1]][pos_1[0]]
                    return False
            else:
                return False
        else:
            return False

    def calculation_retired(self, pos):
        row = self.check_neighbors(pos)
        x, y = pos
        if row:
            list_point = [pos]
            color = self.board[y][x]
            if 'T' in row or 'B' in row or 'C_V' in row:
                for i in range(1, self.height):
                    if y - i >= 0:
                        if self.board[y - i][x] == color:
                            list_point.append((x, y - i))
                        else:
                            break
                    else:
                        break
                for i in range(1, self.height):
                    if y + i < self.height:
                        if self.board[y + i][x] == color:
                            list_point.append((x, y + i))
                        else:
                            break
                    else:
                        break
            if 'L' in row or 'R' in row or 'C_H' in row:
                for i in range(1, self.width):
                    if x - i >= 0:
                        if self.board[y][x - i] == color:
                            list_point.append((x - i, y))
                        else:
                            break
                    else:
                        break
                for i in range(1, self.width):
                    if x + i < self.width:
                        if self.board[y][x + i] == color:
                            list_point.append((x + i, y))
                        else:
                            break
                    else:
                        break
            return list_point
        else:
            return False

    def refresh(self, pos):
        x, y = pos
        pygame.draw.rect(screen, 'black',
                         (self.cellsize * x + 2, self.cellsize * y + 2,
                          self.cellsize - 2, self.cellsize - 2))
        pygame.draw.circle(screen, self.color_dict[self.board[y][x]],
                           [self.cellsize * x + self.cellsize // 2,
                            self.cellsize * y + self.cellsize // 2],
                           self.cellsize // 2 - 5)

    def change_row(self, pos):
        self.count += 1
        color_list = ['g', 'p', 'o', 'r', 't']
        x, y = pos
        for j in range(1, self.height):
            if y - j >= 0:
                for i in range(11):
                    pygame.draw.rect(screen, 'black', [50 * x + 2, 50 * (y - j) + 1, 46, 48])
                    pygame.draw.rect(screen, 'black', [50 * x + 2, 50 * (y - j + 1) + 1, 46, 48])
                    pygame.draw.rect(screen, 'grey', [50 * x, 50 * (y - j), 50, 50], 2)
                    pygame.draw.rect(screen, 'grey', [50 * x, 50 * (y - j + 1), 50, 50], 2)
                    pygame.draw.circle(screen, self.color_dict[self.board[y - j][x]],
                                       [self.cellsize * x + self.cellsize // 2,
                                        self.cellsize * (y - j) + self.cellsize // 2 + i * 5],
                                       self.cellsize // 2 - 5)
                    pygame.display.flip()
                    clock.tick(120)
                self.board[y - j + 1][x] = self.board[y - j][x]
            if y - j == 0 or y == 0:
                color_balls = random.choice(color_list)
                self.board[0][x] = color_balls
                pygame.draw.circle(screen, self.color_dict[color_balls],
                                   [self.cellsize * x + self.cellsize // 2, self.cellsize // 2],
                                   self.cellsize // 2 - 5)
    def rebuild(self, list_point):
        for i in range(len(list_point)):
            for j in range(len(list_point) - i - 1):
                if list_point[j][1] > list_point[j + 1][1]:
                    list_point[j], list_point[j + 1] = list_point[j + 1], list_point[j]
        return list_point

    def check(self):
        for i in range(self.height):
            for j in range(self.width):
                points = self.calculation_retired((j, i))
                if points:
                    for _ in points:
                        self.change_row(_)
                    return True
        return False

    def account(self):
        pygame.draw.rect(screen, 'black', (400, 0, 100, 100))
        font = pygame.font.Font(None, 30)
        text = font.render(str(self.count), True, 'grey')
        text_x = 440
        text_y = 50
        screen.blit(text, (text_x, text_y))

        pygame.draw.rect(screen, 'red', (405, 350, 90, 20), 1)
        font = pygame.font.Font(None, 30)
        text = font.render('сдаться', True, 'red')
        text_x = 410
        text_y = 350
        screen.blit(text, (text_x, text_y))

    def goodbye(self):
        screen.fill('black')
        if self.count >= 100:
            font = pygame.font.Font(None, 40)
            text = font.render('УХ ты, {} очков'.format(self.count), True, (255, 215, 0))
            text_x = 30
            text_y = 150
            screen.blit(text, (text_x, text_y))

            font = pygame.font.Font(None, 40)
            text = font.render('Весьма неплохо'.format(self.count), True, (245, 245, 220))
            text_x = 80
            text_y = 200
            screen.blit(text, (text_x, text_y))

            font = pygame.font.Font(None, 40)
            text = font.render('Надеюсь, ещё увидимся'.format(self.count), True, (255, 215, 0))
            text_x = 130
            text_y = 260
            screen.blit(text, (text_x, text_y))
        else:
            font = pygame.font.Font(None, 40)
            text = font.render('хм, аж {} очков'.format(self.count), True, 'red')
            text_x = 130
            text_y = 150
            screen.blit(text, (text_x, text_y))

            font = pygame.font.Font(None, 70)
            text = font.render('пока'.format(self.count), True, 'red')
            text_x = 200
            text_y = 220
            screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        clock.tick(0.5)


Board_1 = Board()

if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 400
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    pygame.display.set_caption('Три в ряд')
    Board_1.draw()
    running = True
    click = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(405, 495) and event.pos[1] in range(350, 370):
                    Board_1.goodbye()
                    running = False
                    break
                if click:
                    if click == Board_1.coord(event.pos):
                        Board_1.refresh(click)
                        click = 0

                    else:
                        if Board_1.move(Board_1.coord(event.pos), click):
                            Board_1.account()
                            click = 0

                else:
                    click = Board_1.coord(event.pos)

        if click:
            Board_1.wait_move(click)

        clock.tick(fps)
        pygame.display.flip()
    sys.exit()