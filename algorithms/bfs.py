
import time
from collections import deque
from core.puzzle_state import PuzzleState
from core.utils import make_stats

def solve(start_board, goal_board):
    """Breadth-First Search (Complete & Optimal for unit cost)"""
    start_time = time.time()
    start_state = PuzzleState(start_board, g=0)

    if start_state.is_goal(goal_board):
        return [start_state], make_stats([start_state], 0, 1, 1, start_time)

    frontier = deque([start_state])
    visited = set([start_state])

    nodes_expanded = 0
    max_frontier = 1
    visited_states = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        current = frontier.popleft()
        nodes_expanded += 1

        if current.is_goal(goal_board):
            path = []
            cur = current
            while cur:
                path.append(cur)
                cur = cur.parent
            path.reverse()
            return path, make_stats(path, nodes_expanded, visited_states, max_frontier, start_time)

        for n in current.get_neighbors():
            if n not in visited:
                visited.add(n)
                visited_states += 1
                frontier.append(n)

    return [], make_stats([], nodes_expanded, visited_states, max_frontier, start_time)
