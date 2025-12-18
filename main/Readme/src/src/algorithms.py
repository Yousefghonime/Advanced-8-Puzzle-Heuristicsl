import heapq

def manhattan_distance(state):
    dist = 0
    for i, val in enumerate(state):
        if val != 0:
            target_x, target_y = divmod(val, 3)
            curr_x, curr_y = divmod(i, 3)
            dist += abs(target_x - curr_x) + abs(target_y - curr_y)
    return dist

def a_star_search(start_state):
    goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    frontier = [(manhattan_distance(start_state), 0, start_state, [])]
    visited = {tuple(start_state): 0}

    while frontier:
        f, cost, current, path = heapq.heappop(frontier)
        
        if current == goal:
            return path

        from .board import Board
        board = Board(current)
        for neighbor, move in board.get_neighbors():
            new_cost = cost + 1
            if neighbor not in visited or new_cost < visited[neighbor]:
                visited[neighbor] = new_cost
                priority = new_cost + manhattan_distance(neighbor)
                heapq.heappush(frontier, (priority, new_cost, neighbor, path + [move]))
    return None