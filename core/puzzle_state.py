
from copy import deepcopy

N = 3
SIZE = N * N

class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other):
        return isinstance(other, PuzzleState) and self.board == other.board

    def __lt__(self, other):
        return self.f < other.f

    def is_goal(self, goal_board):
        return self.board == goal_board

    def get_neighbors(self):
        neighbors = []
        # locate empty tile (0)
        x = y = None
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == 0:
                    x, y = i, j
                    break
            if x is not None:
                break

        moves = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1),
        }
        for name, (dx, dy) in moves.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N:
                new_board = deepcopy(self.board)
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbors.append(PuzzleState(new_board, self, name, self.g + 1))
        return neighbors
