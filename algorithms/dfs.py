
import time
from core.puzzle_state import PuzzleState
from core.utils import make_stats

def solve(start_board, goal_board, max_depth=50):
    """Depth-First Search with depth-limit (Not Optimal)."""
    start_time = time.time()
    start_state = PuzzleState(start_board, g=0)

    if start_state.is_goal(goal_board):
        return [start_state], make_stats([start_state], 0, 1, 1, start_time)

    stack = [(start_state, 0)]
    visited = set()
    nodes_expanded = 0
    max_frontier = 1
    visited_states = 0

    while stack:
        max_frontier = max(max_frontier, len(stack))
        current, depth = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        visited_states = len(visited)
        nodes_expanded += 1

        if current.is_goal(goal_board):
            path = []
            cur = current
            while cur:
                path.append(cur)
                cur = cur.parent
            path.reverse()
            return path, make_stats(path, nodes_expanded, visited_states, max_frontier, start_time)

        if depth < max_depth:
            for n in reversed(current.get_neighbors()):
                stack.append((n, depth + 1))

    return [], make_stats([], nodes_expanded, visited_states, max_frontier, start_time)
