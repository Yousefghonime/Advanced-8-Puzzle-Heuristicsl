
import time
import heapq
from core.puzzle_state import PuzzleState
from core.utils import make_stats, manhattan_distance

def solve(start_board, goal_board):
    """A* Search with Manhattan distance (Admissible & Consistent for 8-puzzle)."""
    start_time = time.time()
    start_state = PuzzleState(start_board, g=0)
    start_state.h = manhattan_distance(start_state, goal_board)
    start_state.f = start_state.g + start_state.h

    if start_state.is_goal(goal_board):
        return [start_state], make_stats([start_state], 0, 1, 1, start_time)

    frontier = []
    heapq.heappush(frontier, start_state)
    g_scores = {start_state: 0}

    nodes_expanded = 0
    max_frontier = 1
    visited_states = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        current = heapq.heappop(frontier)
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
            n.h = manhattan_distance(n, goal_board)
            n.f = n.g + n.h
            if n not in g_scores or n.g < g_scores[n]:
                g_scores[n] = n.g
                heapq.heappush(frontier, n)
                visited_states = len(g_scores)

    return [], make_stats([], nodes_expanded, visited_states, max_frontier, start_time)
