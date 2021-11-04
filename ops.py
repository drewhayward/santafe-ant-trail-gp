from state import TERMINALS, NONTERMINALS, NONTERMINAL_ARGS, Node
import random

def gen_random_program(max_depth, depth=0):
    if depth >= max_depth:
        return Node(random.sample(TERMINALS,1)[0])
    else:
        cmd = random.sample(TERMINALS | NONTERMINALS, 1)[0]
        if cmd in NONTERMINALS:
            node = Node()
            node.cmd = cmd
            node.children = [gen_random_program(max_depth, depth + 1) for _ in range(NONTERMINAL_ARGS[cmd])]
            return node
        else:
            return Node(cmd)
            

if __name__ == "__main__":
    for _ in range(10):
        print(gen_random_program(10).to_string())