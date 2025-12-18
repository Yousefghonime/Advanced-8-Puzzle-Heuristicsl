import heapq
from collections import deque

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0):
        self.state = state  # الحالة الحالية (Tuple)
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

    # لترتيب النود في خوارزمية A* بناءً على التكلفة الإجمالية
    def __lt__(self, other):
        return (self.cost + self.depth) < (other.cost + other.depth)

class EightPuzzleSolver:
    def __init__(self, start_state, goal_state=(0, 1, 2, 3, 4, 5, 6, 7, 8)):
        self.start_state = tuple(start_state)
        self.goal_state = goal_state

    def get_manhattan_distance(self, state):
        distance = 0
        for i, value in enumerate(state):
            if value != 0:
                target_x, target_y = divmod(value, 3)
                curr_x, curr_y = divmod(i, 3)
                distance += abs(target_x - curr_x) + abs(target_y - curr_y)
        return distance

    def get_neighbors(self, node):
        neighbors = []
        state = list(node.state)
        blank_idx = state.index(0)
        r, c = divmod(blank_idx, 3)

        moves = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        
        for move, (dr, dc) in moves.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_idx = nr * 3 + nc
                new_state = state[:]
                new_state[blank_idx], new_state[new_idx] = new_state[new_idx], new_state[blank_idx]
                neighbors.append(PuzzleNode(tuple(new_state), node, move, node.depth + 1))
        return neighbors

    def solve_bfs(self):
        start_node = PuzzleNode(self.start_state)
        frontier = deque([start_node])
        explored = {self.start_state}
        
        while frontier:
            node = frontier.popleft()
            if node.state == self.goal_state:
                return self.get_path(node)
            
            for neighbor in self.get_neighbors(node):
                if neighbor.state not in explored:
                    explored.add(neighbor.state)
                    frontier.append(neighbor)
        return None

    def solve_astar(self):
        start_node = PuzzleNode(self.start_state)
        start_node.cost = self.get_manhattan_distance(self.start_state)
        frontier = [start_node]
        explored = {}

        while frontier:
            node = heapq.heappop(frontier)
            
            if node.state == self.goal_state:
                return self.get_path(node)

            explored[node.state] = node.depth
            
            for neighbor in self.get_neighbors(node):
                neighbor.cost = self.get_manhattan_distance(neighbor.state)
                if neighbor.state not in explored or neighbor.depth < explored[neighbor.state]:
                    heapq.heappush(frontier, neighbor)
                    explored[neighbor.state] = neighbor.depth
        return None

    def get_path(self, node):
        path = []
        while node.parent:
            path.append(node.action)
            node = node.parent
        return path[::-1]