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

def mutate_program(prog, max_depth):
    prog = Node(prog.to_string())
    nodes = Node.get_flat_nodes(prog)

    # Uniformly select node to mutate
    parent, id, depth, node = random.choice(nodes)
    if parent is None:
        return gen_random_program(max_depth)
    
    parent.children[id] = gen_random_program(max_depth - depth)
    return prog

def mutate_pointwise(prog, mutation_rate=0.1):
    prog = Node(prog.to_string())
    nodes = Node.get_flat_nodes(prog)

    for parent, id, depth, node in nodes:
        if random.random() > mutation_rate:
            continue

        if node.cmd in {'MOVE', 'LEFT', 'RIGHT'}:
            node.cmd = random.choice(['MOVE', 'LEFT', 'RIGHT'])
        elif node.cmd in {'PROG2', 'IF_SENSE'}:
            node.cmd = random.choice(['PROG2', 'IF_SENSE'])

    return prog

def crossover_program(prog1, prog2, max_depth=None):
    prog1 = Node(prog1.to_string())
    prog1_nodes = Node.get_flat_nodes(prog1)
    prog2 = Node(prog2.to_string())
    prog2_nodes = Node.get_flat_nodes(prog2)

    parent1, id1, _, node1 = random.choice(prog1_nodes)
    parent2, id2, _, node2 = random.choice(prog2_nodes)
    if parent1 is None:
        prog1 = node2
    else:
        parent1.children[id1] = node2

    if parent2 is None:
        prog2 = node1
    else:
        parent2.children[id2] = node1

    if max_depth is not None:
        prog1.truncate_depth(max_depth)
        prog2.truncate_depth(max_depth)

    return prog1, prog2

def tournament_selection(pop, k=5):
    inds = random.sample(range(len(pop)), k)
    best = max([pop[i] for i in inds], key=lambda x: x[1])[0]
    return Node(best.to_string())

if __name__ == "__main__":
    for _ in range(10):
        a = gen_random_program(5)
        b = gen_random_program(5)

        c, d = crossover_program(a,b)

        print('--')
        print(a.to_string())
        print(b.to_string())
        print('Crossover')
        print(c.to_string())
        print(d.to_string())