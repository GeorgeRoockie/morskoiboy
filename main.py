from extensions import *
from config import *

class Board:
    def __init__(self):
        self.matrix = self.create_board()
        self.limit = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]  # Если список окажется пуст, вызовем ошибку
        self.list_of_indeces = []  # Будем сюда добавлять индексы расположения кораблей во время их создания
        self.counter = 0
        self.list_of_shots = []
    def create_board(self):
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

    def get_board(self):
        for i in range(len(self.matrix)):
            print(*self.matrix[i], end='')
            print()

    def add_ship(self, row, column, route, length):
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
            def create_ship(row, column, route, length):
                list_of_indeces = []
                if route:
                    for i in range(length):
                        tpl = (row + i, column)
                        list_of_indeces.append(tpl)
                else:
                    for i in range(length):
                        tpl = (row, column + i)
                        list_of_indeces.append(tpl)
                return list_of_indeces

            @staticmethod
            def is_available_indeces_of_ship(matrix, row, col, route, length):
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
                s = create_ship(row, col, route, length)
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

            los = check_used_ships(self.limit, length)
            is_available_indeces_of_ship(self.matrix, row, col, route, length)
        except (IndexException, UserException) as e:
            print(f'Ошибка пользователя.\n{e}')
        else:
            self.list_of_indeces.append(create_ship(row, column, route, length))
            Ship(self.list_of_indeces[self.counter]).get_ship()
            self.limit = los.copy()
            for i in self.list_of_indeces[self.counter]:
                dot = Dot(*i)
                self.matrix[dot.x][dot.y] = MARK_OF_SHIP
            self.countour(route)
            self.counter += 1

    def countour(self, route):
        COUNTOUR_RAISE = MARK_OF_SHIP + '-123456'
        if route:
            for i in self.list_of_indeces[self.counter]:
                dot = Dot(*i)
                try:
                    if str(self.matrix[dot.x - 1][dot.y]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x - 1][dot.y] = TERRYTORY_OF_SHIP
                        if str(self.matrix[dot.x - 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            self.matrix[dot.x - 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(self.matrix[dot.x - 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x - 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

                if str(self.matrix[dot.x][dot.y - 1]) not in COUNTOUR_RAISE:
                    self.matrix[dot.x][dot.y - 1] = TERRYTORY_OF_SHIP
                try:
                    if self.matrix[dot.x][dot.y + 1] not in COUNTOUR_RAISE:
                        self.matrix[dot.x][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
                try:
                    if str(self.matrix[dot.x + 1][dot.y]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x + 1][dot.y] = TERRYTORY_OF_SHIP
                        if str(self.matrix[dot.x + 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            self.matrix[dot.x + 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(self.matrix[dot.x + 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x + 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
        else:
            for i in self.list_of_indeces[self.counter]:
                dot = Dot(*i)
                try:
                    if str(self.matrix[dot.x][dot.y - 1]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x][dot.y - 1] = TERRYTORY_OF_SHIP
                        if str(self.matrix[dot.x - 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            self.matrix[dot.x - 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(self.matrix[dot.x + 1][dot.y - 1]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x + 1][dot.y - 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

                if str(self.matrix[dot.x - 1][dot.y]) not in COUNTOUR_RAISE:
                    self.matrix[dot.x - 1][dot.y] = TERRYTORY_OF_SHIP
                try:
                    if self.matrix[dot.x + 1][dot.y] not in TERRYTORY_OF_SHIP:
                        self.matrix[dot.x + 1][dot.y] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
                try:
                    if str(self.matrix[dot.x][dot.y + 1]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x][dot.y + 1] = TERRYTORY_OF_SHIP
                        if str(self.matrix[dot.x - 1][dot.y + 1]) not in COUNTOUR_RAISE:
                            self.matrix[dot.x - 1][dot.y + 1] = TERRYTORY_OF_SHIP
                    if str(self.matrix[dot.x + 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        self.matrix[dot.x + 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

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
                for index in range(len(self.list_of_indeces)):
                    if (dot.x, dot.y) in self.list_of_indeces[index]:
                        self.list_of_indeces[index].append(HIT_IN_SHIP)
                        Ship(self.list_of_indeces[index]).get_ship()
                        return True
            else:
                self.matrix[dot.x][dot.y] = HIT_MISS
                return False


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dots(self):
        return self.x, self.y


class Ship:
    def __init__(self, ship):
        self.length = len(ship) - ship.count(HIT_IN_SHIP)
        self.dot = ship[0]
        if HIT_IN_SHIP in ship:
            self.hp = f'{self.length - ship.count(HIT_IN_SHIP)}\{self.length}'
        else:
            self.hp = f'{self.length}\{self.length}'

    def get_ship(self):
        print(f'Корабль длиной: {self.length}\nТочка носа коробля: {self.dot}\nЗдоровье: {self.hp}')





b = Board()

while True:
    b.get_board()
    n = input()
    if n == 'y':
        s = [int(i) for i in input().split()]
        row, col, route, length = s
        b.add_ship(row, col, route, length)
        print(b.list_of_indeces)
    if n == 's':
        b.shot(int(input()), int(input()))
