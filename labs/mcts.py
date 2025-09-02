# imports
from __future__ import annotations
import numpy as np
import aigs
from aigs import State, Env
from dataclasses import dataclass, field


# %% Setup
env: Env


# %%
def minimax(state: State, maxim: bool, depth: int, maxDepth: int) -> int:
    if state.ended:
        return state.point
    else:
        depth += 1
        temp: int = -10 if maxim else 10
        for action in np.where(state.legal)[0]:  # for all legal actions
            value = minimax(env.step(state, action), not maxim, depth, maxDepth)
            temp = max(temp, value) if maxim else min(temp, value)
        return temp


def alpha_beta(state: State, maxim: bool, alpha: int, beta: int) -> int:
    raise NotImplementedError  # you do this


@dataclass
class Node:
    state: State  # Add more fields


# Intuitive but difficult in terms of code
def monte_carlo(state: State, cfg) -> int:
    raise NotImplementedError  # you do this


def tree_policy(node: Node, cfg) -> Node:
    raise NotImplementedError  # you do this


def expand(v: Node) -> Node:
    raise NotImplementedError  # you do this


def best_child(root: Node, c) -> Node:
    raise NotImplementedError  # you do this


def default_policy(state: State) -> int:
    raise NotImplementedError  # you do this


def backup(node, delta) -> None:
    raise NotImplementedError  # you do this


# Main function
def main(cfg) -> None:
    global env
    env = aigs.make(cfg.game)
    state = env.init()

    while not state.ended:
        actions = np.where(state.legal)[0]  # the actions to choose from

        match getattr(cfg, state.player):
            case "random":
                a = np.random.choice(actions).item()

            case "human":
                print(state, end="\n\n")
                a = int(input(f"Place your piece ({'x' if state.minim else 'o'}): "))

            case "minimax":
                values = [minimax(env.step(state, a), not state.maxim, 0, 10) for a in actions]
                a = actions[np.argmax(values) if state.maxim else np.argmin(values)]

            case "alpha_beta":
                values = [alpha_beta(env.step(state, a), not state.maxim, -1, 1) for a in actions]
                a = actions[np.argmax(values) if state.maxim else np.argmin(values)]

            case "monte_carlo":
                raise NotImplementedError

            case _:
                raise ValueError(f"Unknown player {state.player}")

        state = env.step(state, a)

    print(f"{['nobody', 'o', 'x'][state.point]} won", state, sep="\n")
