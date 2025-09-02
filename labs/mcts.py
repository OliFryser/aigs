# imports
from __future__ import annotations
import numpy as np
import aigs
from aigs import State, Env
from dataclasses import dataclass
from omegaconf import DictConfig


# %% Setup
env: Env
cfg: DictConfig


def pieceCountHeuristic(state: State, maxim: bool) -> float:
    sumOfPoints = 0
    for idx, col in enumerate(state.board.T):
        for i in range(6):
            if col[i] == 0:
                continue
            point = 0
            distanceFromMiddle = abs(idx - 3)
            if distanceFromMiddle == 0:
                point = 5
            elif distanceFromMiddle == 1:
                point = 3
            elif distanceFromMiddle == 2:
                point = 2
            else:
                point = 1
            sumOfPoints += point * col[i]
    evaluation = sumOfPoints / 100

    return evaluation


# %%
def minimax(state: State, maxim: bool, depth: int) -> float:
    if state.ended:
        return state.point
    if depth > cfg.maxDepth:
        # heuristic
        return pieceCountHeuristic(state, maxim)
    else:
        values = [minimax(env.step(state, a), not maxim, depth + 1) for a in np.where(state.legal)[0]]
        return max(values) if maxim else min(values)


def alpha_beta(state: State, maxim: bool, alpha: float, beta: float, depth: int) -> float:
    if state.ended:
        return state.point
    if depth > cfg.maxDepth:
        return pieceCountHeuristic(state, maxim)
    else:
        bestSoFar: float = -10 if maxim else 10
        for a in np.where(state.legal)[0]:
            currentValue = alpha_beta(env.step(state, a), not maxim, alpha, beta, depth + 1)
            bestSoFar = max(currentValue, bestSoFar) if maxim else min(currentValue, bestSoFar)
            if maxim:
                if bestSoFar >= beta:
                    break
                alpha = max(alpha, bestSoFar)
            else:
                if bestSoFar <= alpha:
                    break
                beta = min(beta, bestSoFar)

        return bestSoFar


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
def main(_cfg) -> None:
    global env, cfg
    cfg = _cfg
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
                values = [minimax(env.step(state, a), not state.maxim, 1) for a in actions]
                a = actions[np.argmax(values) if state.maxim else np.argmin(values)]

            case "alpha_beta":
                values = [alpha_beta(env.step(state, a), not state.maxim, -1, 1, depth=1) for a in actions]
                a = actions[np.argmax(values) if state.maxim else np.argmin(values)]

            case "monte_carlo":
                raise NotImplementedError

            case _:
                raise ValueError(f"Unknown player {state.player}")

        state = env.step(state, a)

    print(f"{['nobody', 'o', 'x'][int(state.point)]} won", state, sep="\n")
