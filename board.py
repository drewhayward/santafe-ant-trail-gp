_sf_init = """.###............................
...#............................
...#.....................###....
...#....................#....#..
...#....................#....#..
...####.#####........##.........
............#................#..
............#...................
............#.......#...........
............#.......#........#..
............#.......#...........
....................#...........
............#................#..
............#...................
............#.......#.....###...
............#.......#..#........
.................#..............
................#...............
............#...#.......#.......
............#...#..........#....
............#...................
............#...#...............
............#.............#.....
............#..........#........
...##..#####....#...............
.#..............#...............
.#..............#...............
.#......#######.................
.#.....#........................
.......#........................
..####..........................
................................"""


class State:
    def __init__(self) -> None:
        self._board = [[c == '#' for c in line] for line in _sf_init.split('\n')]
        self._height = len(self._board)
        self._width = len(self._board[0])
        self._ant = (0,0)
        self._dir = 1
        self._dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self._dir_str = ['v', '>', '^', '<']
        self.collected = 0
        self.steps = 0

    def action_move(self):
        self.steps += 1
        self._ant = (self._ant[0] + self._dirs[self._dir][0]) % self._width, \
            (self._ant[1] + self._dirs[self._dir][1]) % self._height

        if self[self._ant]:
            self[self._ant] = False
            self.collected += 1

    def action_left(self):
        self.steps += 1
        self._dir = (self._dir - 1) % 4

    def action_right(self):
        self.steps += 1
        self._dir = (self._dir + 1) % 4

    def sense_food(self):
        pos = (self._ant[0] + self._dirs[self._dir][0]) % self._width,\
                 (self._ant[1] + self._dirs[self._dir][1]) % self._height

        return self[pos]

    def __getitem__(self, key):
        if not isinstance(key, tuple) or len(key) != 2 or not all(isinstance(k, int) for k in key):
            raise TypeError('Key must be a size 2 tuple of positive integers.')
        return self._board[key[1]][key[0]]

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or len(key) != 2 or not all(isinstance(k, int) for k in key):
            raise TypeError('Key must be a size 2 tuple of positive integers.')
        if not isinstance(value, bool):
            raise TypeError('Board values should be booleans.')

        self._board[key[1]][key[0]] = value

    def __str__(self) -> str:
        board = ''
        for y, row in enumerate(self._board):
            for x, c in enumerate(row):
                if (x,y) == self._ant:
                    board += self._dir_str[self._dir]
                elif self[x,y]:
                    board += 'X'
                else:
                    board += ' '
                
                board += ' '
            board += '\n'

        return board



if __name__ == "__main__":
    b = State()
    print(b)
    print(b[0,2])