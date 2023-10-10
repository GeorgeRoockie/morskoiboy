from extensions import *
from config import *
class Board:
    def __init__(self):
        self.matrix = self.create_board()
        self.ship = Ship()

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
            CheckIndeces.is_available_indeces(self.matrix, row, column, route, length)
        except (IndexException, UserException) as e:
            print(f'Ошибка пользователя \n{e}')
        else:
            self.indeces = self.ship.create_ship(row, column, route, length)
            for i in self.indeces:
                if len(i) != 0:
                    for j in i:
                        self.matrix[j[0]][j[1]] = MARK_OF_SHIP
            self.countour(route)

    def countour(self, route):
        COUNTOUR_RAISE = MARK_OF_SHIP + '-123456'
        for i in self.indeces:
            for j in i:
                if route:
                    try:
                        if str(self.matrix[j[0] - 1][j[1]]) not in COUNTOUR_RAISE:
                            self.matrix[j[0] - 1][j[1]] = TERRYTORY_OF_SHIP
                            if str(self.matrix[j[0] - 1][j[1] - 1]) not in COUNTOUR_RAISE:
                                self.matrix[j[0] - 1][j[1] - 1] = TERRYTORY_OF_SHIP
                        if str(self.matrix[j[0] - 1][j[1] + 1]) not in COUNTOUR_RAISE:
                            self.matrix[j[0] - 1][j[1] + 1] = TERRYTORY_OF_SHIP
                    except IndexError:
                        pass

                    if str(self.matrix[j[0]][j[1] - 1]) not in COUNTOUR_RAISE:
                        self.matrix[j[0]][j[1] - 1] = TERRYTORY_OF_SHIP
                    try:
                        if self.matrix[j[0]][j[1] + 1] not in COUNTOUR_RAISE:
                            self.matrix[j[0]][j[1] + 1] = TERRYTORY_OF_SHIP
                    except IndexError:
                        pass
                    try:
                        if str(self.matrix[j[0] + 1][j[1]]) not in COUNTOUR_RAISE:
                            self.matrix[j[0] + 1][j[1]] = TERRYTORY_OF_SHIP
                            if str(self.matrix[j[0] + 1][j[1] - 1]) not in COUNTOUR_RAISE:
                                self.matrix[j[0] + 1][j[1] - 1] = TERRYTORY_OF_SHIP
                        if str(self.matrix[j[0] + 1][j[1] + 1]) not in COUNTOUR_RAISE:
                            self.matrix[j[0] + 1][j[1] + 1] = TERRYTORY_OF_SHIP
                    except IndexError:
                        pass
                else:
                    try:
                        if str(self.matrix[j[0]][j[1] - 1]) not in COUNTOUR_RAISE:
                            self.matrix[j[0]][j[1] - 1] = TERRYTORY_OF_SHIP
                            if str(self.matrix[j[0] - 1][j[1] - 1]) not in COUNTOUR_RAISE:
                                self.matrix[j[0] - 1][j[1] - 1] = TERRYTORY_OF_SHIP
                        if str(self.matrix[j[0] + 1][j[1] - 1]) not in COUNTOUR_RAISE:
                            self.matrix[j[0] + 1][j[1] - 1] = TERRYTORY_OF_SHIP
                    except IndexError:
                        pass

                    if str(self.matrix[j[0] - 1][j[1]]) not in COUNTOUR_RAISE:
                        self.matrix[j[0] - 1][j[1]] = TERRYTORY_OF_SHIP
                    try:
                        if self.matrix[j[0] + 1][j[1]] not in TERRYTORY_OF_SHIP:
                            self.matrix[j[0] + 1][j[1]] = TERRYTORY_OF_SHIP
                    except IndexError:
                        pass
                    try:
                        if str(self.matrix[j[0]][j[1] + 1]) not in COUNTOUR_RAISE:
                            self.matrix[j[0]][j[1] + 1] = TERRYTORY_OF_SHIP
                            if str(self.matrix[j[0] - 1][j[1] + 1]) not in COUNTOUR_RAISE:
                                self.matrix[j[0] - 1][j[1] + 1] = TERRYTORY_OF_SHIP
                        if str(self.matrix[j[0] + 1][j[1] + 1]) not in COUNTOUR_RAISE:
                            self.matrix[j[0] + 1][j[1] + 1] = TERRYTORY_OF_SHIP
                    except IndexError:
                        pass




class Ship:
    def __init__(self):
        self.list_of_ships = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')] # Если список окажется пуст, вызовем ошибку
        self.list_of_indeces = [[], [], [], [], [], [], [],] # Будем сюда добавлять индексы расположения кораблей во время их создания
        self.counter = 0 # Счетчик для смены индекса в списке индексов
    def create_ship(self, row, column, route, length):
        if route:
            for i in range(length):
                tpl = (row + i, column)
                self.list_of_indeces[self.counter].append(tpl)
            self.counter += 1
        else:
            for i in range(length):
                tpl = (row, column + i)
                self.list_of_indeces[self.counter].append(tpl)
            self.counter += 1
        check_deleted_ship = len(self.list_of_ships)
        for j in range(len(self.list_of_ships)): #Удаляем поставленный корабль из списка доступных
            if len(self.list_of_ships[j]) == length:
                del self.list_of_ships[j]
                break
        try:
            if len(self.list_of_ships) == check_deleted_ship: #Смысл в том, что если список не изменился, значит корабль был уже взять, тем самым, вызвав ошибку, не дадим взять новый
                raise UserException('Этот корабль недоступен!')#Это будет доделываться, когда напишу класс пользователя
        except UserException:
            print('Корабли такой длины закончились')

        print(self.list_of_ships)
        print(self.list_of_indeces)
        return self.list_of_indeces

b = Board()

while True:
    b.get_board()
    n = input()
    if n == 'y':
        s = [int(i) for i in input().split()]
        row, col, route, length = s
        b.add_ship(row, col, route, length)
        b.get_board()
'''
b.add_ship(4, 3, 1, 3)
b.get_board()
b.add_ship(1, 1, 1, 2)
b.get_board()
'''
