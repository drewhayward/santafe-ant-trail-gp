from collections import deque
from state import *
from ops import *

OPT = """(IF_SENSE MOVE (PROG2 LEFT (IF_SENSE MOVE (PROG2 LEFT (IF_SENSE MOVE (PROG2 LEFT (IF_SENSE MOVE (PROG2 LEFT MOVE))))))))"""

def run(program: Node, board: State, max_steps=500):
    # Repeatedly run program while we have steps
    while board.steps < max_steps:

        # Run program
        commands = [program]
        while commands:
            if board.steps >= max_steps:
                break

            node = commands.pop()

            # print(board)
            # print(f"Next action: {node.cmd}")
            # input()

            if node.cmd in TERMINALS:
                board.take_action(node.cmd)
            elif node.cmd == 'IF_SENSE':
                assert(len(node.children) == 2)
                if board.sense_food():
                    commands.append(node.children[0])
                else:
                    commands.append(node.children[1])
            elif node.cmd.startswith('PROG'):
                n = int(node.cmd[-1])
                assert(len(node.children) == n)
                commands.extend(reversed(node.children))
            else:
                raise Exception(f'Invalid command {node.cmd}')

    return board.collected

if __name__ == "__main__":
    optimal = Node(OPT)
    run(optimal, State())