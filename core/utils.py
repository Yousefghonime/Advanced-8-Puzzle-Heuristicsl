
import time

def board_to_2d(flat, N=3):
    return [flat[i:i+N] for i in range(0, len(flat), N)]

def board_to_1d(grid):
    flat = []
    for row in grid:
        flat.extend(row)
    return flat

def manhattan_distance(state, goal_board, N=3):
    goal_pos = {}
    for i in range(N):
        for j in range(N):
            goal_pos[goal_board[i][j]] = (i, j)
    dist = 0
    for i in range(N):
        for j in range(N):
            tile = state.board[i][j]
            if tile != 0:
                gx, gy = goal_pos[tile]
                dist += abs(i - gx) + abs(j - gy)
    return dist

def make_stats(solution_path, nodes_expanded, visited_states, max_frontier, start_time):
    exec_time = time.time() - start_time
    if solution_path:
        return {
            'solution_found': True,
            'path_length': len(solution_path) - 1,
            'nodes_expanded': nodes_expanded,
            'visited_states': visited_states,
            'max_frontier': max_frontier,
            'execution_time': exec_time,
        }
    else:
        return {
            'solution_found': False,
            'path_length': 0,
            'nodes_expanded': nodes_expanded,
            'visited_states': visited_states,
            'max_frontier': max_frontier,
            'execution_time': exec_time,
        }
