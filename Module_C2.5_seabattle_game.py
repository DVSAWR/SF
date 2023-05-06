from random import randint


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    empty_tile = 'O'
    ship_tile = '■'
    destroyed_ship_tile = '\033[1;93mX\033[0m'
    miss_tile = '\033[35mT\033[0m'



class GameFieldException(Exception):
    ...
class OutGameFieldException(GameFieldException):
    def __str__(self):
        return 'Error: You are trying to shoot out of game field!'
class UsedGameFieldTileException(GameFieldException):
    def __str__(self):
        return 'Error: You have already fired at this game field tile'
class WrongShipPositionException(GameFieldException):
    ...

class Ship:
    def __init__(self, position, length, orintation):
        self.position = position
        self.length = length
        self.orintation = orintation

        self.hp = length

    @property
    def ship_position(self):
        ship_position_tile = []
        for i in range(self.length):
            cur_x = self.position.x
            cur_y = self.position.y
            if self.orintation == 0:
                cur_x += i
            elif self.orintation == 1:
                cur_y += i

            ship_position_tile.append(Tile(cur_x, cur_y))
        return ship_position_tile

    def damaged(self, shot):
        return shot in self.ship_position

class GameField:
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide
        self.count = 0
        self.field = [['O']*size for _ in range(size)]

        self.used_tile = []
        self.ships = []

    def add_ship(self, ship):
        for p in ship.ship_position:
            if self.out(p) or p in self.used_tile:
                raise WrongShipPositionException()
        for p in ship.ship_position:
            self.field[p.x][p.y] = Tile.ship_tile
            self.used_tile.append(p)

        self.ships.append(ship)
        self.ship_outline(ship)

    def ship_outline(self, ship, v=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for p in ship.ship_position:
            for dx, dy in near:
                cur = Tile(p.x + dx, p.y + dy)
                if not(self.out(cur)) and cur not in self.used_tile:
                    if v:
                        self.field[cur.x][cur.y] = Tile.miss_tile
                    self.used_tile.append(cur)

    def __str__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hide:
            res = res.replace(Tile.ship_tile, Tile.empty_tile)
        return res

    def out(self, p):
        return not((0 <= p.x < self.size) and (0 <= p.y < self.size))

    def shot(self, p):
        if self.out(p):
            raise OutGameFieldException()
        if p in self.used_tile:
            raise UsedGameFieldTileException()

        self.used_tile.append(p)

        for ship in self.ships:
            if p in ship.ship_position:
                ship.hp -= 1
                self.field[p.x][p.y] = Tile.destroyed_ship_tile
                if ship.hp == 0:
                    self.count += 1
                    self.ship_outline(ship, v=True)
                    print('* Enemy SHIP was destroyed! *\n')
                    return False
                else:
                    print('* HIT! *\n')
                    return True

        self.field[p.x][p.y] = Tile.miss_tile
        print('* MISS! *\n')
        return False

    def begin(self):
        self.used_tile = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except GameFieldException as e:
                print(e)

class Bot(Player):
    def ask(self):
        p = Tile(randint(0,5), randint(0, 5))
        print(f'Complucter turn: {p.x+1} {p.y+1}')
        return p

class User(Player):
    def ask(self):
        while True:
            cords = input('Your turn: ').split()

            if len(cords) != 2:
                print(' Enter 2 nums! ')
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print(' Enter nums! ')
                continue

            x, y = int(x), int(y)

            return Tile(x-1, y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = True

        self.bot = Bot(co, pl)
        self.user = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = GameField(size=self.size)
        attempts = 0
        for length in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Tile(randint(0, self.size), randint(0, self.size)), length, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipPositionException:
                    ...
        board.begin()
        return board

    def start_information(self):
        print('\t-----------------')
        print('\t \033[1mSEA-BATTLE GAME\033[0m')
        print('\t-----------------')
        print(' \033[1mInput format: x y\033[0m\n'
              ' x - line number\n'
              ' y - column number\n')

        print(' \033[1mTile format:\033[0m\n'
              f' empty tile = {Tile.empty_tile}\n'
              f' ship tile = {Tile.ship_tile}\n'
              f' destroyed ship tile = {Tile.destroyed_ship_tile}\n'
              f' miss tile = {Tile.miss_tile}\n')


    def loop(self):
        num = 0
        while True:
            print('User game field:')
            print(self.user.board)
            print('\n')
            print('Complucter game field:')
            print(self.bot.board)
            if num % 2 == 0:
                print('\n\033[1mUser turn!\033[0m')
                repeat = self.user.move()
            else:
                print('\n\033[1mComplucter turn!\033[0m')
                repeat = self.bot.move()
            if repeat:
                num -= 1

            if self.bot.board.count == 7:
                print('\n* USER WIN! *')
                break

            if self.user.board.count == 7:
                print('\n* COMPLUCTER WIN! *')
                break
            num += 1

    def start(self):
        self.start_information()
        self.loop()




glhf = Game()
glhf.start()
