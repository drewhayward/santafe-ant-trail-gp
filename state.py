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



TERMINALS = {'MOVE', 'LEFT', 'RIGHT'}
NONTERMINALS = {'IF_SENSE', 'PROG2', 'PROG3'}
NONTERMINAL_ARGS = {'IF_SENSE':2, 'PROG2':2, 'PROG3':3}

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

    def take_action(self, action: str):
        fns = {
            'MOVE': self.action_move,
            'LEFT': self.action_left,
            'RIGHT': self.action_right,
        }
        fns[action]()

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


def smartsplit(s):
    output = []
    start = 0
    count = 0
    for i, c in enumerate(s):
        assert(count >= 0)
        if c == '(':
            count += 1
        elif c == ')':
            count -= 1
        elif c == ' ' and count == 0 and start < i - 1:
            output.append(s[start:i])
            start = i + 1
    assert(count == 0)
    if count == 0 and start < len(s):
        output.append(s[start:])
    return output

def smartstrip(s):
    if s.startswith('(') and s.endswith(')'):
        return s[1:-1]
    else:
        return s

class Node:
    def __init__(self, s = None) -> None:
        if s is not None:
            pass # Recursively init program
            self.cmd, *self.children = smartsplit(smartstrip(s))
            self.children = [Node(c) for c in self.children]
        else:
            self.cmd = None
            self.children = []

    def __repr__(self) -> str:
        return f"Node(cmd='{self.cmd}', {len(self.children)} children)"

    def _to_string(self) -> str:
        """
        Returns lisp-like string to represent the program
        """
        if self.children:
            return '(' + self.cmd + ' ' + ' '.join((c._to_string() for c in self.children)) + ')'
        else:
            return self.cmd

    def to_string(self) -> str:
        if self.children:
            return self._to_string()
        else:
            return '(' + self._to_string() + ')'


if __name__ == "__main__":
    b = State()
    print(b)
    print(b[0,2])