import argparse
from collections import deque
import matplotlib.pyplot as plt
import tqdm
import wandb

from state import *
from ops import *


param_defaults = {
    "max_tree_depth":5,
    "max_generations":300,
    "pop_size" : 300,
    "elitism_k" : 5,
    "tournament_k" : 15,
    "mutation_prob" : 0.7
}

parser = argparse.ArgumentParser()
args, unknown = parser.parse_known_args()

param_defaults.update(vars(args))

wandb.init(project="evocomp-hw4", config=param_defaults, entity="drewhayward")

config = wandb.config

MAX_FITNESS = 89
OPT = """(IF_SENSE MOVE (PROG2 LEFT (IF_SENSE MOVE (PROG2 LEFT (IF_SENSE MOVE (PROG2 LEFT (IF_SENSE MOVE (PROG2 LEFT MOVE))))))))"""

def run(program: Node, board: State = State(), max_steps=500):
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


def gp_search(
    max_tree_depth=5,
    max_generations=50,
    pop_size = 500,
    elitism_k = 7,
    tournament_k = 7,
    mutation_prob = 0.4
):
    # Create initial population
    pop = [gen_random_program(max_tree_depth) for _ in range(pop_size)]
    pop = [(p, run(p, State())) for p in pop]

    gen = 0
    pbar = tqdm.tqdm(total=max_generations)
    while gen < max_generations:
        # Top 5 elitism
        new_pop = {Node(p.to_string()) for p, _ in pop[elitism_k:]}
        # Build new population
        while len(new_pop) < pop_size:
            # Mix between reproduced individuals and 
            # cross over individuals 
            # with elitism
            if random.random() < 0.5: # Mutation
                ind = tournament_selection(pop, k=tournament_k)
                if random.random() < mutation_prob:
                    new_pop.add(mutate_program(ind, max_depth=max_tree_depth))
                else:
                    new_pop.add(Node(ind.to_string()))
            else: # crossover
                ind1 = tournament_selection(pop, k=tournament_k)
                ind2 = tournament_selection(pop, k=tournament_k)

                c1, c2 = crossover_program(ind1, ind2)
                if random.random() < mutation_prob:
                    c1 = mutate_program(c1, max_depth=max_tree_depth)
                if random.random() < mutation_prob:
                    c2 = mutate_program(c2, max_depth=max_tree_depth)
                
                new_pop.update([c1, c2])
        pop = list(new_pop)

        # Eval population fitness
        pop = [(p, run(p, State())) for p in pop]
        pop.sort(key=lambda x: x[1])

        # Stats
        wandb.log({
            'best_fitness': pop[-1][1],
            'worst_fitness': pop[0][1],
            'avg_fitness': sum((p[1] for p in pop)) / len(pop),
            'avg_depth': sum(p[0].max_depth() for p in pop) / len(pop),
            'avg_nodes': sum(p[0].num_nodes() for p in pop) / len(pop)
        })

        # If best is max, break
        if pop[-1][0] == MAX_FITNESS:
            break

        gen += 1
        pbar.update()

    pbar.close()


    # # Graph generations
    # plt.figure()

    # # Fitness plot
    # plt.subplot(2,1,1)
    # x = list(range(max_generations))
    # plt.plot(x, worst)
    # plt.plot(x, avg)
    # plt.plot(x, best)
    # plt.legend(['Worst', 'Avg', 'Best'])
    # plt.ylim(0, MAX_FITNESS)
    # plt.xlabel('Generations')
    # plt.ylabel('Fitness')

    # # Tree stats
    # plt.subplot(2,1,2)
    # plt.plot(x, avg_nodes)
    # plt.plot(x, avg_depth)
    # plt.legend(['Avg #Nodes in Tree', 'Avg Tree Depth'])
    # plt.xlabel('Generations')

    # plt.savefig('fitness.png')

    # # Return best program
    # print(pop[-1][0].to_string())
    with open('sln.txt', 'w') as f:
        f.write(pop[-1][0].to_string())
    wandb.save('sln.txt')

if __name__ == "__main__":
    gp_search(**config)