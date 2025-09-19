# %% qd.py
#   quality diversity exercises
# by: Noah Syrkis

# Imports
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
from typing import Tuple
from pcgym import PcgrlEnv


# %% n-dimensional function with a strange topology
@partial(np.vectorize, signature="(d)->()")
def griewank_function(pop):  # this is kind of our fitness function (except we a minimizing)
    return 1 + np.sum(pop**2) / 4000 - np.prod(np.cos(pop / np.sqrt(np.arange(1, pop.size + 1))))


def rosenbrock_function(x):
    acc = 0
    for i in range(len(x) - 1):
        acc += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
    return acc


@partial(np.vectorize, signature="(d)->(d)", excluded=[0])
def mutate(sigma, pop):  # What are we doing here?
    return pop + np.random.normal(0, sigma, pop.shape)


@partial(np.vectorize, signature="(d),(d)->(d)")
def crossover(x1, x2):  # TODO: think about what we are doing here. Is it smart?
    return x1 * np.random.rand() + x2 * (1 - np.random.rand())


def step(pop, cfg):
    loss = np.array([rosenbrock_function(x) for x in pop])
    idxs = np.argsort(loss)[: int(cfg.population * cfg.proportion)]  # select best
    best = np.tile(pop[idxs], (int(cfg.population * cfg.proportion), 1))  # cross over
    pop = crossover(best, best[np.random.permutation(best.shape[0])])  # mutate
    return mutate(cfg.sigma, pop), loss  # return new generation and loss


# %% Setup
def main(cfg):
    # pop = np.random.rand(cfg.population, cfg.dimensions)
    # fitnesses = []
    # for gen in range(cfg.generation):
    #     pop, fitness = step(pop, cfg)
    #     fitnesses.append(fitness.min())
    #     print(f"Generation {gen}: Best fitness = {fitness.min()}")

    # our_plot_function(griewank_function)
    # plt.plot(fitnesses)
    # plt.yscale("log")
    # plt.xlabel("Generation")
    # plt.ylabel("Best Fitness")
    # plt.show()

    env, pop = init_pcgym(cfg)

    # create the levels
    env._rep._map = pop[0]
    # random agent
    terminated = False
    while True:
        random_action = env.action_space.sample()
        print(random_action)
        observation, reward, terminated, truncated, info = env.step(random_action)
        img = env.render()
        if img is not None:
            plt.imshow(img)
            fig = plt.gcf()  # get current figure
            # Option 1: set figure size (in inches)
            fig.set_size_inches(18, 5)
            plt.show(block=True)


# %% Init population (maps)
def init_pcgym(cfg) -> Tuple[PcgrlEnv, np.ndarray]:
    env = PcgrlEnv(prob=cfg.game, rep=cfg.rep, render_mode="rgb_array")
    env.reset()
    pop = np.random.randint(0, env.get_num_tiles(), (cfg.n, *env._rep._map.shape))  # type: ignore
    return env, pop


#########################################################################
##  BELOW HERE THERE BE DRAGONS (left over stuff i played around with) ##
#########################################################################

# %% Plotting function that I think we should put in utils.py
# def our_plot_function(fn):
#     x1 = np.linspace(-10, 10, 100)
#     x2 = np.linspace(-10, 10, 100)
#     xs = np.stack(np.meshgrid(x1, x2), axis=-1)
#     ys = fn(xs)
#     plt.imshow(ys, cmap="viridis")
#     plt.colorbar()
#     plt.show()


# env, pop = init(ctx.config)
# from pcgym.envs import PcgrlEnv
# from typing import Tuple
# from pcgym.envs.helper import get_string_map

# import qdax
# from qdax.core.map_elites import MAPElites
# from PIL import Image
# from qdax.core.emitters.mutation_operators import polynomial_mutation
# env._rep._mep = pop[0]
# Image.fromarray(env.render()).save("map.png")
# fitness, behavior = map(np.array, zip(*list(map(lambda p: eval(env, p), pop))))
# print(behavior.shape, fitness.shape)
# # print(fitness)
# # print(behavior)
# # print(list(map(lambda p: mutate(ctx.config, env, p), pop)))


# # %% using gym-pcg to evaluate map quality
# def eval(env, p) -> Tuple[int, np.ndarray]:
#     env._rep._map = p
#     string_map = get_string_map(env._rep._map, env._prob.get_tile_types())
#     stats = env._prob.get_stats(string_map)
#     behavior = np.array([stats["disjoint-tubes"], stats["empty"]])
#     return env._prob.get_reward(stats, {k: 0 for k in stats.keys()}), behavior


# def mutate(cfg, env, p) -> np.ndarray:
#     mask = np.random.random(p.shape) < cfg.qd.p
#     p[mask] = np.random.randint(0, env.get_num_tiles(), p[mask].shape)
#     return p


# def archive(state, p):
#     raise NotImplementedError
