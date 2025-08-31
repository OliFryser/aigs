# games.py
#   aigs games
# by: Noah Syrkis

# imports
from aigs.types import State, Env
import numpy as np


# connect four
class ConnectFour(Env):
    def init(self) -> State:
        board = np.zeros((6, 7), dtype=int)
        legal = board[0] == 0
        state = State(board=board, legal=legal)
        return state

    def step(self, state: State, action) -> State:
        # hint: use x.diagonal(i)

        # place piece
        board = state.board.copy()
        piecePosition: tuple[int, int] = (-1, -1)

        column = board[:, action]
        assert column[0] == 0

        for i in range(5, -1, -1):
            if column[i] == 0:
                board[i, action] = 1 if state.maxim else -1
                piecePosition = (i, action)
                break

        mask = board == 1 if state.maxim else -1
        winner: bool = self.checkForWinner(mask, piecePosition)

        return State(
            board,
            legal=board[0] == 0,
            ended=(board != 0).all() | winner,
            point=(1 if state.maxim else -1) if winner else 0,
            maxim=not state.maxim,
        )

    def checkForWinner(self, mask, piecePostion: tuple[int, int]) -> bool:
        # Check its row column and diagonal vectors for 4 matching pieces in a row
        row = mask[piecePostion[0]]
        column = mask.T[piecePostion[1]]
        rightDiagonals = [mask.diagonal(i) for i in range(-6, 7)]
        leftDiagonals = [mask.T.diagonal(i) for i in range(-6, 7)]
        lst = [self.checkFourConnectingPieces(v) for v in [row] + [column] + rightDiagonals + leftDiagonals]
        return True in lst

    def checkFourConnectingPieces(self, v) -> bool:
        if len(v) < 4:
            return False

        for i in range(len(v) - 3):
            if v[i] and v[i + 1] and v[i + 2] and v[i + 3]:
                return True

        return False


# tic tac toe
class TicTacToe(Env):
    def init(self) -> State:
        board = np.zeros((3, 3), dtype=int)
        legal = board.flatten() == 0
        state = State(board=board, legal=legal)
        return state

    def step(self, state, action) -> State:
        # make your move
        board = state.board.copy()
        assert board[action // 3, action % 3] == 0, f"Invalid move: {action}"
        board[action // 3, action % 3] = 1 if state.maxim else -1

        # was it a winning move?
        mask = board == (1 if state.maxim else -1)
        winner: bool = (
            mask.all(axis=1).any()  # |
            or mask.all(axis=0).any()  # —
            or mask.trace() == 3  # \
            or np.fliplr(mask).trace() == 3  # /
        )

        # return the next state
        return State(
            board=board,
            legal=board.flatten() == 0,  # empty board positions
            ended=(board != 0).all() | winner,
            point=(1 if state.maxim else -1) if winner else 0,
            maxim=not state.maxim,
        )
