from extensions import *
from config import *
import random

class Board:
    def __init__(self):
        self.matrix = self.create_board()
        self.limit = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]  # Если список окажется пуст, вызовем ошибку
        self.list_of_indeces = []  # Будем сюда добавлять индексы расположения кораблей во время их создания
        self.list_of_indeces_shots = [[]] # Индексы выстрелов
        self.counter_of_ships = 0
        self.enemy_matrix = self.create_board()
    def get_my_board(self):
        for i in range(len(self.matrix)):
            print(*self.matrix[i], end='')
            print()
    def get_enemy_board(self):
        for i in range(len(self.enemy_matrix)):
            print(*self.enemy_matrix[i], end='')
            print()
    @staticmethod
    def create_board():
        matrix = []
        for _ in range(7):
            temp = [i for i in range(7)]
            matrix.append(temp)
        for row in range(1, 7):
            for col in range(7):
                if col == 0:
                    matrix[row][col] = row
                else:
                    matrix[row][col] = FREE_CELL
        matrix[0][0] = ' '
        return matrix
    def add_ship(self, row, col, route, length):
        try:
            @staticmethod
            def check_used_ships(los, length):  # Если корабль доступен в списке, возвращает список, вычеркивая из него этот корабль
                flag = False
                for i in los:
                    if len(i) == length:
                        flag = True
                        los.remove(i)
                        break
                if not flag:
                    raise UserException('Корабли этого типа закончились.')
                return los

            @staticmethod
            def is_available_indeces_of_ship(matrix, row, col, route, length):
                if matrix[row][col] == MARK_OF_SHIP:
                    raise UserException('В этой точке уже стоит корабль')
                if route != 0 and route != 1:
                    raise UserException('1 - вертикальное направление \n0 - горизонтальное направление')
                if length > 3 or length < 0:
                    raise UserException(f'Корабль не может иметь длину {length}')
                if (0 < row < len(matrix)) and (0 < col < len(matrix)):
                    if (row > 4 and route == 1 and length == 3) or (row == 6 and route == 1 and length > 1):
                        raise IndexException(
                            f'Вертикальный корабль, длиной {length} по координатам ({row};{col}), не вмещается в поле.\nПопробуйте сменить направление, либо координаты.')
                    if (col > 4 and route == 0 and length == 3) or (col == 6 and route == 0 and length > 1):
                        raise IndexException(
                            f'Горизонтальный корабль, длиной {length} по координатам ({row};{col}), не вмещается в поле.\nПопробуйте сменить направление, либо координаты.')
                else:
                    raise IndexException(f'Введены неверные координаты: ({row};{col})')
                s = Ship(length, (row, col), route).dots()
                if route:
                    for i in s:
                        dot = Dot(*i)
                        if matrix[dot.x - 1][dot.y] == MARK_OF_SHIP or matrix[dot.x - 1][dot.y - 1] == MARK_OF_SHIP:
                            raise IndexException(
                                f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        try:
                            if matrix[dot.x - 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x][dot.y - 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                            if matrix[dot.x][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x + 1][dot.y] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                            if matrix[dot.x + 1][dot.y - 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                            if matrix[dot.x + 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        except IndexError:
                            pass
                else:
                    for i in s:
                        dot = Dot(*i)
                        if matrix[dot.x][dot.y - 1] == MARK_OF_SHIP or matrix[dot.x - 1][dot.y - 1] == MARK_OF_SHIP:
                            raise IndexException(
                                f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        try:
                            if matrix[dot.x + 1][dot.y - 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x - 1][dot.y] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                            if matrix[dot.x + 1][dot.y] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                            if matrix[dot.x - 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                            if matrix[dot.x + 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException(
                                    f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        except IndexError:
                            pass

            is_available_indeces_of_ship(self.matrix, row, col, route, length)
            los = check_used_ships(self.limit, length)
        except (IndexException, UserException) as e:
            print(f'Ошибка пользователя.\n{e}')
        else:
            self.list_of_indeces.append(Ship(length, (row, col), route).dots())

            for i in self.list_of_indeces[self.counter_of_ships]:
                dot = Dot(*i)
                self.matrix[dot.x][dot.y] = MARK_OF_SHIP
            self.matrix = self.countour(route, self.matrix, self.counter_of_ships, self.list_of_indeces)
            self.limit = los.copy()
            self.counter_of_ships += 1

    def countour(self, route, matrix, counter, indeces):
        COUNTOUR_RAISE = MARK_OF_SHIP + '-123456' + HIT_MISS + HIT_IN_SHIP
        if route:
            for i in indeces[counter]:
                dot = Dot(*i)
                try:
                    if str(matrix[dot.x - 1][dot.y]) not in COUNTOUR_RAISE:
                        matrix[dot.x - 1][dot.y] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x - 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x - 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x - 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x - 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

                if str(matrix[dot.x][dot.y - 1]) not in COUNTOUR_RAISE:
                    matrix[dot.x][dot.y - 1] = TERRYTORY_OF_SHIP
                try:
                    if matrix[dot.x][dot.y + 1] not in COUNTOUR_RAISE:
                        matrix[dot.x][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
                try:
                    if str(matrix[dot.x + 1][dot.y]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x + 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x + 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x + 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
            return matrix
        else:
            for i in indeces[counter]:
                dot = Dot(*i)
                try:
                    if str(matrix[dot.x][dot.y - 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x][dot.y - 1] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x - 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x - 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x + 1][dot.y - 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y - 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

                if str(matrix[dot.x - 1][dot.y]) not in COUNTOUR_RAISE:
                    matrix[dot.x - 1][dot.y] = TERRYTORY_OF_SHIP
                try:
                    if matrix[dot.x + 1][dot.y] not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
                try:
                    if str(matrix[dot.x][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x][dot.y + 1] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x - 1][dot.y + 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x - 1][dot.y + 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x + 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
            return matrix

    def shot(self, x, y):
        dot = Dot(x, y)
        try:
            if (0 < x < len(self.matrix)) and (0 < y < len(self.matrix)):
                if HIT_IN_SHIP in self.matrix[dot.x][dot.y] or HIT_MISS in self.matrix[dot.x][dot.y]:
                    raise UserException('Нельзя стрелять в одно и то же место')
            else:
                raise IndexException('Введены неверные координаты')
        except (UserException, IndexException) as e:
            print(f'Ошибка пользователя\n{e}')
        else:
            if MARK_OF_SHIP in self.matrix[dot.x][dot.y]:
                self.matrix[dot.x][dot.y] = HIT_IN_SHIP
                self.enemy_matrix[dot.x][dot.y] = HIT_IN_SHIP
                self.list_of_indeces_shots[0].append((dot.x, dot.y))
                for index in range(len(self.list_of_indeces)):
                    if (dot.x, dot.y) in self.list_of_indeces[index]:
                        los1 = len(self.list_of_indeces[index]) - self.list_of_indeces[index].count(HIT_IN_SHIP)
                        self.list_of_indeces[index].append(HIT_IN_SHIP)
                        self.is_ship_killed(los1, self.list_of_indeces[index])
                        return True
            else:
                self.matrix[dot.x][dot.y] = HIT_MISS
                self.enemy_matrix[dot.x][dot.y] = HIT_MISS
                return False
    def is_ship_killed(self, los1, los2):
        if Ship(los1, los2[0]).check_hp(len(los2)) == 0:
            print('Корабль убит')
            if los1 != 1:
                route = Ship(los2, los2[0]).get_route()
            else:
                route = 1
            self.enemy_matrix = self.countour(route, self.enemy_matrix, 0, self.list_of_indeces_shots)

            

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dots(self):
        return self.x, self.y


class Ship:
    def __init__(self, length, dot, route=None):
        self.length = length
        self.dot = Dot(*dot)
        self.route = route
        self.hp = None

    def dots(self):
        list_of_indeces = []
        if self.route:
            for i in range(self.length):
                tpl = (self.dot.x + i, self.dot.y)
                list_of_indeces.append(tpl)
        else:
            for i in range(self.length):
                tpl = (self.dot.x, self.dot.y + i)
                list_of_indeces.append(tpl)
        return list_of_indeces
    def check_hp(self, los2):
        self.hp = self.length - los2 + self.length
        return self.hp
    def get_route(self):
        if self.length[0][0] != self.length[1][0]:
            return 1
        else:
            return 0
class Player:
    def __init__(self):
        self.matrix = Board().matrix
        self.enemy_matrix = Board().enemy_matrix
        self.moves = Board()

    def ask(self):
        pass
    def move(self):
        self.moves.shot(*self.ask())

class User(Player):
    def ask(self):
        print('Введите координаты точки, куда хотите выстрелить')
        s = [int(i) for i in input().split()]
        x, y = s
        return x, y

class AI(Player):
    pass


class Game: # не доделан
    def __init__(self):
        self.user = User()
        self.ai = AI()
    def start(self):
        print(f'Хотите, чтобы корабли расставились автоматически?\nY - Да\nN - Нет')
        ans = input().lower()
        if ans == 'y':
            self.random_board()
        while True:
            self.user.moves.get_enemy_board()
            print('-------------')
            self.user.moves.get_my_board()
            n = input()
            if n == 'y':
                s = [int(i) for i in input().split()]
                row, col, route, length = s
                self.user.moves.add_ship(row, col, route, length)
                print(self.user.moves.list_of_indeces)
            if n == 's':
                self.user.move()
    def random_board(self):
        counter = 0
        while counter < 100:
            length = len(self.user.moves.limit[0])
            row = random.randint(1, 6)
            col = random.randint(1, 6)
            route = random.randint(0, 1)
            self.user.moves.add_ship(row, col, route, length)
            if len(self.user.moves.limit) == 0:
                break
            counter += 1
        if len(self.user.moves.limit) != 0:
            print()
            print('ПЕРЕСОБИРАЕМ')
            print()
            self.user.moves.matrix = self.user.moves.create_board()
            self.user.moves.limit = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]  # Если список окажется пуст, вызовем ошибку
            self.user.moves.list_of_indeces = []  # Будем сюда добавлять индексы расположения кораблей во время их создания
            self.user.moves.counter_of_ships = 0
            self.random_board()


Game().start()
