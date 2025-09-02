# %% qd.py
#   quality diversity exercises
# by: Noah Syrkis

# Imports
import numpy as np
from pcgym.envs import PcgrlEnv
from typing import Tuple
from pcgym.envs.helper import get_string_map

# import qdax
# from qdax.core.map_elites import MAPElites
from PIL import Image
# from qdax.core.emitters.mutation_operators import polynomial_mutation


# %% Init population (maps)
def init(cfg) -> Tuple[PcgrlEnv, np.ndarray]:
    env = PcgrlEnv(prob=cfg.qd.game, rep=cfg.qd.rep, render_mode="rgb_array")
    env.reset()
    pop = np.random.randint(0, env.get_num_tiles(), (cfg.qd.n, *env._rep._map.shape))  # type: ignore
    return env, pop


# %% using gym-pcg to evaluate map quality
def eval(env, p) -> Tuple[int, np.ndarray]:
    env._rep._map = p
    string_map = get_string_map(env._rep._map, env._prob.get_tile_types())
    stats = env._prob.get_stats(string_map)
    behavior = np.array([stats["disjoint-tubes"], stats["empty"]])
    return env._prob.get_reward(stats, {k: 0 for k in stats.keys()}), behavior


def mutate(cfg, env, p) -> np.ndarray:
    mask = np.random.random(p.shape) < cfg.qd.p
    p[mask] = np.random.randint(0, env.get_num_tiles(), p[mask].shape)
    return p


def archive(state, p):
    pass


# %% Setup
def main(ctx):
    print("9")
    exit()
    env, pop = init(ctx.config)
    env._rep._mep = pop[0]
    Image.fromarray(env.render()).save("map.png")
    fitness, behavior = map(np.array, zip(*list(map(lambda p: eval(env, p), pop))))
    print(behavior.shape, fitness.shape)
    # print(fitness)
    # print(behavior)
    # print(list(map(lambda p: mutate(ctx.config, env, p), pop)))
