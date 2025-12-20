
import time
import heapq
from core.puzzle_state import PuzzleState
from core.utils import make_stats

def solve(start_board, goal_board):
    """Uniform Cost Search (Complete & Optimal for unit step cost)."""
    start_time = time.time()
    start_state = PuzzleState(start_board, g=0)

    if start_state.is_goal(goal_board):
        return [start_state], make_stats([start_state], 0, 1, 1, start_time)

    frontier = []
    heapq.heappush(frontier, (0, start_state))
    best_cost = {start_state: 0}

    nodes_expanded = 0
    max_frontier = 1
    visited_states = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        cost, current = heapq.heappop(frontier)
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
            new_cost = cost + 1
            if n not in best_cost or new_cost < best_cost[n]:
                best_cost[n] = new_cost
                heapq.heappush(frontier, (new_cost, n))
                visited_states = len(best_cost)

    return [], make_stats([], nodes_expanded, visited_states, max_frontier, start_time)
