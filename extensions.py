from config import MARK_OF_SHIP

class IndexException(Exception):
    pass
class UserException(Exception):
    pass
class CheckIndeces:
    @staticmethod
    def create_ship(row, column, route, length):
        list_of_indeces = [[], [], [], [], [], [], [],]
        counter = 0
        if route:
            for i in range(length):
                tpl = (row + i, column)
                list_of_indeces[counter].append(tpl)
            counter += 1
        else:
            for i in range(length):
                tpl = (row, column + i)
                list_of_indeces[counter].append(tpl)
            counter += 1
        return list_of_indeces
    @staticmethod
    def is_available_indeces(matrix, row, col, route, length):
        if not(0 <= route <= 1):
            raise UserException('1 - вертикальное направление \n0 - горизонтальное направление')
        if length > 3 or length < 0:
            raise UserException(f'Корабль не может иметь длину {length}')
        if (0 < row < len(matrix)) and (0 < col < len(matrix)):
            if (row > 4 and route == 1 and length == 3) or (row == 6 and route == 1 and length > 1):
                raise IndexException(f'Вертикальный корабль, длиной {length} по координатам ({row};{col}), не вмещается в поле.\nПопробуйте сменить направление, либо координаты.')
            if (col > 4 and route == 0 and length == 3) or (col == 6 and route == 0 and length > 1):
                raise IndexException(f'Горизонтальный корабль, длиной {length} по координатам ({row};{col}), не вмещается в поле.\nПопробуйте сменить направление, либо координаты.')
        else:
            raise IndexException(f'Введены неверные координаты: ({row};{col})')
        s = CheckIndeces().create_ship(row, col, route, length)
        if route:
            for i in s:
                for j in i:
                    if matrix[j[0] - 1][j[1]] == MARK_OF_SHIP or matrix[j[0] - 1][j[1] - 1] == MARK_OF_SHIP:
                        raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    try:
                        if matrix[j[0] - 1][j[1] + 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    except IndexError:
                        pass
                    try:
                        if matrix[j[0]][j[1] - 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        if matrix[j[0]][j[1] + 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    except IndexError:
                        pass
                    try:
                        if matrix[j[0] + 1][j[1]] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        if matrix[j[0] + 1][j[1] - 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        if matrix[j[0] + 1][j[1] + 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    except IndexError:
                        pass
        else:
            for i in s:
                for j in i:
                    if matrix[j[0]][j[1] - 1] == MARK_OF_SHIP or matrix[j[0] - 1][j[1] - 1] == MARK_OF_SHIP:
                        raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    try:
                        if matrix[j[0] + 1][j[1] - 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    except IndexError:
                        pass
                    try:
                        if matrix[j[0] - 1][j[1]] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        if matrix[j[0] + 1][j[1]] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    except IndexError:
                        pass
                    try:
                        if matrix[j[0]][j[1] + 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        if matrix[j[0] - 1][j[1] + 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                        if matrix[j[0] + 1][j[1] + 1] == MARK_OF_SHIP:
                            raise IndexException(f'Расстояние от одного корабля до другого должно быть минимум в одну клетку')
                    except IndexError:
                        pass