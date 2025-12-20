import heapq
from collections import deque
import time

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0):
        self.state = state  # الحالة الحالية (Tuple)
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost  # التكلفة التراكمية (لـ UCS)

    # لترتيب النود في خوارزمية A* بناءً على التكلفة الإجمالية
    def __lt__(self, other):
        return (self.cost + self.depth) < (other.cost + other.depth)

class EightPuzzleSolver:
    def __init__(self, start_state, goal_state=(0, 1, 2, 3, 4, 5, 6, 7, 8)):
        self.start_state = tuple(start_state)
        self.goal_state = goal_state
        self.nodes_expanded = 0
        self.max_depth = 0

    def get_manhattan_distance(self, state):
        """حساب المسافة المانهاتنية للهيوريستك في A*"""
        distance = 0
        for i, value in enumerate(state):
            if value != 0:
                target_x, target_y = divmod(value, 3)
                curr_x, curr_y = divmod(i, 3)
                distance += abs(target_x - curr_x) + abs(target_y - curr_y)
        return distance

    def get_neighbors(self, node):
        """الحصول على الحالات المجاورة مع الحركات الممكنة"""
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
                # التكلفة = 1 لكل حركة (يمكن تعديلها)
                neighbors.append(PuzzleNode(
                    tuple(new_state), 
                    node, 
                    move, 
                    node.depth + 1,
                    node.cost + 1  # تكلفة تراكمية لكل حركة
                ))
        return neighbors

    # ==================== BFS ====================
    def solve_bfs(self):
        """Breadth-First Search"""
        self.nodes_expanded = 0
        self.max_depth = 0
        
        start_node = PuzzleNode(self.start_state)
        frontier = deque([start_node])
        explored = {self.start_state}
        
        while frontier:
            node = frontier.popleft()
            self.nodes_expanded += 1
            self.max_depth = max(self.max_depth, node.depth)
            
            if node.state == self.goal_state:
                return self.get_path(node), self.nodes_expanded, self.max_depth
            
            for neighbor in self.get_neighbors(node):
                if neighbor.state not in explored:
                    explored.add(neighbor.state)
                    frontier.append(neighbor)
        return None, self.nodes_expanded, self.max_depth

    # ==================== DFS ====================
    def solve_dfs(self, max_depth=50):
        """Depth-First Search مع حد أقصى للعمق"""
        self.nodes_expanded = 0
        self.max_depth = 0
        
        start_node = PuzzleNode(self.start_state)
        frontier = [start_node]  # استخدام list كـ stack
        explored = {self.start_state}
        
        while frontier:
            node = frontier.pop()  # LIFO
            self.nodes_expanded += 1
            self.max_depth = max(self.max_depth, node.depth)
            
            if node.state == self.goal_state:
                return self.get_path(node), self.nodes_expanded, self.max_depth
            
            # إذا وصلنا للحد الأقصى، لا نستمر في التعمق
            if node.depth < max_depth:
                for neighbor in self.get_neighbors(node):
                    if neighbor.state not in explored:
                        explored.add(neighbor.state)
                        frontier.append(neighbor)
        return None, self.nodes_expanded, self.max_depth

    # ==================== UCS ====================
    def solve_ucs(self):
        """Uniform-Cost Search (Dijkstra's Algorithm)"""
        self.nodes_expanded = 0
        self.max_depth = 0
        
        start_node = PuzzleNode(self.start_state)
        frontier = []
        heapq.heappush(frontier, (start_node.cost, id(start_node), start_node))
        explored = {self.start_state: 0}  # state -> best cost
        
        while frontier:
            _, _, node = heapq.heappop(frontier)
            self.nodes_expanded += 1
            self.max_depth = max(self.max_depth, node.depth)
            
            if node.state == self.goal_state:
                return self.get_path(node), self.nodes_expanded, self.max_depth
            
            # تحقق إذا كان لدينا بالفعل تكلفة أفضل
            if node.cost > explored.get(node.state, float('inf')):
                continue
            
            for neighbor in self.get_neighbors(node):
                # إذا كانت هذه المسار أرخص من المسارات السابقة
                if neighbor.state not in explored or neighbor.cost < explored[neighbor.state]:
                    explored[neighbor.state] = neighbor.cost
                    heapq.heappush(frontier, (neighbor.cost, id(neighbor), neighbor))
        
        return None, self.nodes_expanded, self.max_depth

    # ==================== A* ====================
    def solve_astar(self):
        """A* Search مع Manhattan Heuristic"""
        self.nodes_expanded = 0
        self.max_depth = 0
        
        start_node = PuzzleNode(self.start_state)
        start_heuristic = self.get_manhattan_distance(self.start_state)
        frontier = []
        heapq.heappush(frontier, (start_heuristic, id(start_node), start_node))
        explored = {self.start_state: 0}  # state -> cost_so_far
        
        while frontier:
            _, _, node = heapq.heappop(frontier)
            self.nodes_expanded += 1
            self.max_depth = max(self.max_depth, node.depth)
            
            if node.state == self.goal_state:
                return self.get_path(node), self.nodes_expanded, self.max_depth
            
            # تحقق إذا كان لدينا بالفعل تكلفة أفضل
            if node.cost > explored.get(node.state, float('inf')):
                continue
            
            for neighbor in self.get_neighbors(node):
                neighbor_heuristic = self.get_manhattan_distance(neighbor.state)
                total_cost = neighbor.cost + neighbor_heuristic
                
                # إذا كانت هذه المسار أرخص من المسارات السابقة
                if neighbor.state not in explored or neighbor.cost < explored[neighbor.state]:
                    explored[neighbor.state] = neighbor.cost
                    heapq.heappush(frontier, (total_cost, id(neighbor), neighbor))
        
        return None, self.nodes_expanded, self.max_depth

    def get_path(self, node):
        """إعادة بناء المسار من العقدة الأخيرة إلى البداية"""
        path = []
        while node.parent:
            path.append(node.action)
            node = node.parent
        return path[::-1]

    # ==================== Benchmarking ====================
    def benchmark_all(self, max_dfs_depth=50):
        """تشغيل جميع الخوارزميات ومقارنة النتائج"""
        results = {}
        algorithms = [
            ('BFS', self.solve_bfs),
            ('DFS', lambda: self.solve_dfs(max_dfs_depth)),
            ('UCS', self.solve_ucs),
            ('A*', self.solve_astar)
        ]
        
        for name, func in algorithms:
            start_time = time.time()
            path, nodes_expanded, max_depth = func()
            end_time = time.time()
            
            results[name] = {
                'path': path,
                'time': end_time - start_time,
                'nodes_expanded': nodes_expanded,
                'max_depth': max_depth,
                'path_length': len(path) if path else None,
                'solution_found': path is not None
            }
            
            print(f"\n{name}:")
            print(f"  Time: {results[name]['time']:.4f} seconds")
            print(f"  Nodes expanded: {nodes_expanded}")
            print(f"  Max depth: {max_depth}")
            print(f"  Path length: {len(path) if path else 'No solution'}")
            print(f"  Solution found: {'Yes' if path else 'No'}")
        
        return results
