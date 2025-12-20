
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from collections import deque
import heapq
from copy import deepcopy

N = 3
SIZE = N * N


class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board          # 2D list
        self.parent = parent        # previous PuzzleState
        self.move = move            # move name that led here
        self.g = g                  # path cost from start
        self.h = h                  # heuristic value
        self.f = g + h              # total cost (for A*)
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other):
        if other is None:
            return False
        return self.board == other.board

    def __lt__(self, other):
        # Needed for heapq comparisons; prioritize lower f
        return self.f < other.f

    def get_neighbors(self):
        """Generate all possible next states (valid moves)."""
        neighbors = []

        # Find empty tile (0) position
        empty_pos = None
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == 0:
                    empty_pos = (i, j)
                    break
            if empty_pos:
                break

        x, y = empty_pos
        moves = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1)
        }

        for move_name, (dx, dy) in moves.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < N and 0 <= new_y < N:
                new_board = deepcopy(self.board)
                # Swap empty tile with the adjacent tile
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                neighbors.append(PuzzleState(new_board, self, move_name, self.g + 1))

        return neighbors

    def is_goal(self, goal_board):
        return self.board == goal_board


class EightPuzzleSolver:
    def __init__(self, start_board, goal_board):
        self.start_board = start_board
        self.goal_board = goal_board
        self.solution_path = []
        self.nodes_expanded = 0
        self.max_frontier = 0
        self.execution_time = 0
        self.visited_states = 0

    def manhattan_distance(self, state):
        """Heuristic: Manhattan distance from current to goal."""
        distance = 0
        goal_positions = {}

        # Map each tile to its goal position
        for i in range(N):
            for j in range(N):
                goal_positions[self.goal_board[i][j]] = (i, j)

        # Sum |dx| + |dy| for all numbered tiles
        for i in range(N):
            for j in range(N):
                tile = state.board[i][j]
                if tile != 0:
                    goal_x, goal_y = goal_positions[tile]
                    distance += abs(i - goal_x) + abs(j - goal_y)

        return distance

    def bfs(self):
        """Breadth-First Search (Complete & Optimal)."""
        start_time = time.time()
        start_state = PuzzleState(self.start_board, g=0)

        # Already solved?
        if start_state.is_goal(self.goal_board):
            self.solution_path = [start_state]
            self.execution_time = time.time() - start_time
            return True

        frontier = deque([start_state])
        visited = set([start_state])
        self.visited_states = 1

        while frontier:
            self.max_frontier = max(self.max_frontier, len(frontier))
            current_state = frontier.popleft()
            self.nodes_expanded += 1

            if current_state.is_goal(self.goal_board):
                self._reconstruct_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for neighbor in current_state.get_neighbors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    self.visited_states += 1
                    frontier.append(neighbor)

        self.execution_time = time.time() - start_time
        return False

    def dfs(self, max_depth=50):
        """Depth-First Search with depth limit (Not Optimal)."""
        start_time = time.time()
        start_state = PuzzleState(self.start_board, g=0)

        if start_state.is_goal(self.goal_board):
            self.solution_path = [start_state]
            self.execution_time = time.time() - start_time
            return True

        stack = [(start_state, 0)]
        visited = set()

        while stack:
            self.max_frontier = max(self.max_frontier, len(stack))
            current_state, depth = stack.pop()

            if current_state in visited:
                continue
            visited.add(current_state)
            self.visited_states = len(visited)
            self.nodes_expanded += 1

            if current_state.is_goal(self.goal_board):
                self._reconstruct_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            if depth < max_depth:
                for neighbor in reversed(current_state.get_neighbors()):
                    stack.append((neighbor, depth + 1))

        self.execution_time = time.time() - start_time
        return False

    def ucs(self):
        """Uniform Cost Search (Complete & Optimal for uniform step cost)."""
        start_time = time.time()
        start_state = PuzzleState(self.start_board, g=0)

        if start_state.is_goal(self.goal_board):
            self.solution_path = [start_state]
            self.execution_time = time.time() - start_time
            return True

        frontier = []
        heapq.heappush(frontier, (0, start_state))
        visited = {start_state: 0}

        while frontier:
            self.max_frontier = max(self.max_frontier, len(frontier))
            current_cost, current_state = heapq.heappop(frontier)
            self.nodes_expanded += 1

            if current_state.is_goal(self.goal_board):
                self._reconstruct_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for neighbor in current_state.get_neighbors():
                new_cost = current_cost + 1  # uniform step cost
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))

            self.visited_states = len(visited)

        self.execution_time = time.time() - start_time
        return False

    def astar(self):
        """A* Search with Manhattan distance (Complete & Optimal with admissible heuristic)."""
        start_time = time.time()
        start_state = PuzzleState(self.start_board, g=0)
        start_state.h = self.manhattan_distance(start_state)
        start_state.f = start_state.g + start_state.h

        if start_state.is_goal(self.goal_board):
            self.solution_path = [start_state]
            self.execution_time = time.time() - start_time
            return True

        frontier = []
        heapq.heappush(frontier, start_state)
        g_scores = {start_state: 0}

        while frontier:
            self.max_frontier = max(self.max_frontier, len(frontier))
            current_state = heapq.heappop(frontier)
            self.nodes_expanded += 1

            if current_state.is_goal(self.goal_board):
                self._reconstruct_path(current_state)
                self.execution_time = time.time() - start_time
                return True

            for neighbor in current_state.get_neighbors():
                neighbor.h = self.manhattan_distance(neighbor)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in g_scores or neighbor.g < g_scores[neighbor]:
                    g_scores[neighbor] = neighbor.g
                    heapq.heappush(frontier, neighbor)

            self.visited_states = len(g_scores)

        self.execution_time = time.time() - start_time
        return False

    def _reconstruct_path(self, goal_state):
        """Backtrack to build the solution path."""
        path = []
        current = goal_state
        while current:
            path.append(current)
            current = current.parent
        self.solution_path = list(reversed(path))

    def get_solution_stats(self):
        """Return solution statistics for UI."""
        if not self.solution_path:
            return {
                'solution_found': False,
                'path_length': 0,
                'nodes_expanded': self.nodes_expanded,
                'visited_states': self.visited_states,
                'max_frontier': self.max_frontier,
                'execution_time': self.execution_time
            }
        return {
            'solution_found': True,
            'path_length': len(self.solution_path) - 1,
            'nodes_expanded': self.nodes_expanded,
            'visited_states': self.visited_states,
            'max_frontier': self.max_frontier,
            'execution_time': self.execution_time
        }


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle AI Solver")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")

        # Game state
        self.numbers = list(range(1, SIZE)) + [0]
        self.goal_state = list(range(1, SIZE)) + [0]
        self.current_state = self.numbers.copy()

        # GUI variables
        self.buttons = []
        self.moves = 0
        self.start_time = None
        self.timer_running = False
        self.is_solving = False
        self.solution_steps = []
        self.current_step = 0

        # Algorithms
        self.algorithms = ["BFS", "DFS", "UCS", "A*"]

        self.create_widgets()
        self.shuffle_puzzle()
        self.update_display()

    # ---------- UI building ----------
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = tk.Label(
            main_frame, text="8-Puzzle AI Solver",
            font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333"
        )
        title_label.pack(pady=(0, 20))

        # Left panel (puzzle)
        left_panel = tk.Frame(main_frame, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        puzzle_frame = tk.Frame(left_panel, bg="#333", bd=3, relief=tk.RAISED)
        puzzle_frame.pack(pady=10)

        # Create puzzle buttons
        self.buttons = []
        for i in range(N):
            row_buttons = []
            for j in range(N):
                btn = tk.Button(
                    puzzle_frame, text="",
                    font=("Arial", 28, "bold"),
                    width=4, height=2, bd=3, relief=tk.RAISED,
                    bg="#4FC3F7", activebackground="#29B6F6",
                    command=lambda r=i, c=j: self.tile_click(r, c)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Info
        info_frame = tk.Frame(left_panel, bg="#f0f0f0")
        info_frame.pack(pady=15)

        self.moves_label = tk.Label(
            info_frame, text="Moves: 0", font=("Arial", 14, "bold"), bg="#f0f0f0"
        )
        self.moves_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(
            info_frame, text="Time: 00:00", font=("Arial", 14, "bold"), bg="#f0f0f0"
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)

        # Controls
        control_frame = tk.Frame(left_panel, bg="#f0f0f0")
        control_frame.pack(pady=10)

        self.shuffle_btn = tk.Button(
            control_frame, text=" Shuffle",
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
            padx=20, pady=8, command=self.shuffle_puzzle
        )
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            control_frame, text=" Reset",
            font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
            padx=20, pady=8, command=self.reset_game
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # Right panel (solver)
        right_panel = tk.Frame(main_frame, bg="#e0e0e0", bd=2, relief=tk.SUNKEN)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))

        algo_frame = tk.LabelFrame(
            right_panel, text="Search Algorithms",
            font=("Arial", 14, "bold"), bg="#e0e0e0", padx=15, pady=15
        )
        algo_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(algo_frame, text="Select Algorithm:", font=("Arial", 12), bg="#e0e0e0").pack(anchor="w")
        self.algo_var = tk.StringVar(value="A*")
        self.algo_combo = ttk.Combobox(
            algo_frame, textvariable=self.algo_var,
            values=self.algorithms, state="readonly",
            font=("Arial", 11), width=15
        )
        self.algo_combo.pack(fill=tk.X, pady=5)

        self.solve_btn = tk.Button(
            algo_frame, text=" Solve Puzzle",
            font=("Arial", 13, "bold"), bg="#FF9800", fg="white",
            padx=20, pady=10, command=self.solve_puzzle
        )
        self.solve_btn.pack(pady=10)

        info_frame2 = tk.LabelFrame(
            right_panel, text="Algorithm Properties",
            font=("Arial", 12, "bold"), bg="#e0e0e0", padx=10, pady=10
        )
        info_frame2.pack(fill=tk.X, padx=10, pady=5)

        info_text = (
            "• BFS: Complete & Optimal (memory intensive)\n"
            "• DFS: Not optimal (depth limited)\n"
            "• UCS: Complete & Optimal (considers costs)\n"
            "• A*: Complete & Optimal (most efficient)"
        )
        info_label = tk.Label(info_frame2, text=info_text, font=("Arial", 9), bg="#e0e0e0", fg="#555", justify=tk.LEFT)
        info_label.pack()

        solution_frame = tk.LabelFrame(
            right_panel, text="Solution Controls",
            font=("Arial", 14, "bold"), bg="#e0e0e0", padx=15, pady=15
        )
        solution_frame.pack(fill=tk.X, padx=10, pady=10)

        nav_frame = tk.Frame(solution_frame, bg="#e0e0e0")
        nav_frame.pack(pady=5)

        self.prev_btn = tk.Button(
            nav_frame, text="◀ Previous", font=("Arial", 11),
            bg="#607D8B", fg="white", state=tk.DISABLED, command=self.prev_step
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(
            nav_frame, text="Next ▶", font=("Arial", 11),
            bg="#607D8B", fg="white", state=tk.DISABLED, command=self.next_step
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.play_btn = tk.Button(
            solution_frame, text="▶ Play Solution",
            font=("Arial", 11), bg="#009688", fg="white",
            state=tk.DISABLED, command=self.play_solution
        )
        self.play_btn.pack(pady=5)

        results_frame = tk.LabelFrame(
            right_panel, text="Performance Results",
            font=("Arial", 14, "bold"), bg="#e0e0e0",
            padx=15, pady=15
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.results_text = tk.Text(
            results_frame, height=15, width=35,
            font=("Consolas", 10), bg="white", relief=tk.SUNKEN, bd=2
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.results_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_text.yview)

        self.results_text.insert(tk.END, "Performance Results\n")
        self.results_text.insert(tk.END, "=" * 30 + "\n\n")
        self.results_text.insert(tk.END, "Select algorithm and click 'Solve Puzzle'\n")
        self.results_text.insert(tk.END, "to see detailed metrics.\n")

    # ---------- Helpers ----------
    def board_to_2d(self, flat_board):
        """Convert flat list (length 9) to 3x3 grid."""
        board = []
        for i in range(0, SIZE, N):
            board.append(flat_board[i:i + N])
        return board

    def board_to_1d(self, board_2d):
        """Convert 3x3 grid to flat list (length 9)."""
        flat_board = []
        for row in board_2d:
            flat_board.extend(row)
        return flat_board

    def shuffle_puzzle(self):
        """Shuffle the board while ensuring solvability for 3x3 (even inversions)."""
        self.stop_timer()
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 00:00")

        while True:
            random.shuffle(self.numbers)
            inversions = 0
            for i in range(SIZE):
                if self.numbers[i] == 0:
                    continue
                for j in range(i + 1, SIZE):
                    if self.numbers[j] != 0 and self.numbers[i] > self.numbers[j]:
                        inversions += 1
            if inversions % 2 == 0:
                break

        self.current_state = self.numbers.copy()
        self.update_display()
        self.clear_solution()

    def reset_game(self):
        """Reset by reshuffling."""
        self.shuffle_puzzle()

    def update_display(self):
        """Refresh the tiles on the board."""
        for i in range(N):
            for j in range(N):
                idx = i * N + j
                value = self.current_state[idx]
                if value == 0:
                    self.buttons[i][j].config(text="", bg="#BDBDBD")
                else:
                    self.buttons[i][j].config(text=str(value), bg="#4FC3F7")

    def find_empty_position(self):
        """Index (0..8) of empty tile in flat state."""
        for i in range(SIZE):
            if self.current_state[i] == 0:
                return i
        return -1

    def tile_click(self, row, col):
        """Handle tile click and make a move if adjacent to empty."""
        if self.is_solving:
            return

        idx = row * N + col
        empty_idx = self.find_empty_position()

        row_diff = abs(row - (empty_idx // N))
        col_diff = abs(col - (empty_idx % N))

        if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
            self.current_state[empty_idx], self.current_state[idx] = \
                self.current_state[idx], self.current_state[empty_idx]

            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")

            if not self.timer_running:
                self.start_timer()

            self.update_display()

            if self.current_state == self.goal_state:
                self.stop_timer()
                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {self.moves} moves!")

    # ---------- Timer ----------
    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    # ---------- Solution I/O ----------
    def clear_solution(self):
        self.solution_steps = []
        self.current_step = 0
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.play_btn.config(state=tk.DISABLED)

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Performance Results\n")
        self.results_text.insert(tk.END, "=" * 30 + "\n\n")
        self.results_text.insert(tk.END, "Select algorithm and click 'Solve Puzzle'\n")
        self.results_text.insert(tk.END, "to see detailed metrics.\n")

    def solve_puzzle(self):
        if self.is_solving:
            return

        self.is_solving = True
        self.solve_btn.config(state=tk.DISABLED)
        self.shuffle_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

        start_board = self.board_to_2d(self.current_state)
        goal_board = self.board_to_2d(self.goal_state)

        solver = EightPuzzleSolver(start_board, goal_board)
        algorithm = self.algo_var.get()

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Solving with {algorithm}...\n")
        self.results_text.see(tk.END)
        self.root.update()

        success = False
        try:
            if algorithm == "BFS":
                success = solver.bfs()
            elif algorithm == "DFS":
                success = solver.dfs()
            elif algorithm == "UCS":
                success = solver.ucs()
            elif algorithm == "A*":
                success = solver.astar()
        except Exception as e:
            self.results_text.insert(tk.END, f"Error: {str(e)}\n")

        stats = solver.get_solution_stats()

        if success:
            self.results_text.insert(tk.END, f" {algorithm} Solution Found!\n")
            self.results_text.insert(tk.END, "=" * 40 + "\n\n")

            # Flatten solution to 1D states for playback
            self.solution_steps = []
            for state in solver.solution_path:
                flat_state = self.board_to_1d(state.board)
                self.solution_steps.append(flat_state)

            self.current_step = 0
            if len(self.solution_steps) > 1:
                self.next_btn.config(state=tk.NORMAL)
                self.play_btn.config(state=tk.NORMAL)

            # Performance metrics
            self.results_text.insert(tk.END, "PERFORMANCE METRICS:\n")
            self.results_text.insert(tk.END, "─" * 20 + "\n")
            self.results_text.insert(tk.END, f"• Solution Path: {stats['path_length']} moves\n")
            self.results_text.insert(tk.END, f"• Time Taken: {stats['execution_time']:.4f} seconds\n")
            self.results_text.insert(tk.END, f"• Nodes Expanded: {stats['nodes_expanded']:,}\n")
            self.results_text.insert(tk.END, f"• States Visited: {stats['visited_states']:,}\n")
            self.results_text.insert(tk.END, f"• Max Frontier Size: {stats['max_frontier']:,}\n")

            if stats['path_length'] > 0:
                efficiency = stats['nodes_expanded'] / stats['path_length']
                self.results_text.insert(tk.END, f"• Efficiency Ratio: {efficiency:.2f}\n")

            # Algorithm properties
            self.results_text.insert(tk.END, "\nALGORITHM PROPERTIES:\n")
            self.results_text.insert(tk.END, "─" * 20 + "\n")
            if algorithm == "BFS":
                self.results_text.insert(tk.END, "• Completeness: Yes\n")
                self.results_text.insert(tk.END, "• Optimality: Yes\n")
                self.results_text.insert(tk.END, "• Time Complexity: O(b^d)\n")
                self.results_text.insert(tk.END, "• Space Complexity: O(b^d)\n")
            elif algorithm == "DFS":
                self.results_text.insert(tk.END, "• Completeness: Limited (depth)\n")
                self.results_text.insert(tk.END, "• Optimality: No\n")
                self.results_text.insert(tk.END, "• Time Complexity: O(b^m)\n")
                self.results_text.insert(tk.END, "• Space Complexity: O(bm)\n")
            elif algorithm == "UCS":
                self.results_text.insert(tk.END, "• Completeness: Yes\n")
                self.results_text.insert(tk.END, "• Optimality: Yes\n")
                self.results_text.insert(tk.END, "• Time Complexity: O(b^{C*/ε})\n")
                self.results_text.insert(tk.END, "• Space Complexity: O(b^{C*/ε})\n")
            elif algorithm == "A*":
                self.results_text.insert(tk.END, "• Completeness: Yes\n")
                self.results_text.insert(tk.END, "• Optimality: Yes\n")
                self.results_text.insert(tk.END, "• Time Complexity: O(b^d)\n")
                self.results_text.insert(tk.END, "• Space Complexity: O(b^d)\n")
                self.results_text.insert(tk.END, "• Heuristic Used: Manhattan Distance\n")
        else:
            self.results_text.insert(tk.END, f" {algorithm}: No Solution Found\n")
            self.results_text.insert(tk.END, "=" * 40 + "\n\n")
            self.results_text.insert(tk.END, f"• Time Taken: {stats['execution_time']:.4f} seconds\n")
            self.results_text.insert(tk.END, f"• Nodes Expanded: {stats['nodes_expanded']:,}\n")
            self.results_text.insert(tk.END, f"• Max Frontier Size: {stats['max_frontier']:,}\n")
            if algorithm == "DFS":
                self.results_text.insert(tk.END, "\nNote: DFS depth limit (50) reached.\n")
                self.results_text.insert(tk.END, "Try BFS, UCS, or A* for guaranteed solution.\n")

        self.results_text.see(tk.END)
        self.is_solving = False
        self.solve_btn.config(state=tk.NORMAL)
        self.shuffle_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.current_state = self.solution_steps[self.current_step].copy()
            self.update_display()
            if self.current_step == 0:
                self.prev_btn.config(state=tk.DISABLED)
            if self.current_step < len(self.solution_steps) - 1:
                self.next_btn.config(state=tk.NORMAL)

    def next_step(self):
        if self.current_step < len(self.solution_steps) - 1:
            self.current_step += 1
            self.current_state = self.solution_steps[self.current_step].copy()
            self.update_display()
            if self.current_step > 0:
                self.prev_btn.config(state=tk.NORMAL)
            if self.current_step == len(self.solution_steps) - 1:
                self.next_btn.config(state=tk.DISABLED)

    def play_solution(self):
        if not self.solution_steps or self.is_solving:
            return

        self.is_solving = True
        self.solve_btn.config(state=tk.DISABLED)
        self.shuffle_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.play_btn.config(state=tk.DISABLED)

        def animate_step(step):
            if step < len(self.solution_steps):
                self.current_state = self.solution_steps[step].copy()
                self.update_display()
                self.current_step = step
                if step == len(self.solution_steps) - 1:
                    self.is_solving = False
                    self.solve_btn.config(state=tk.NORMAL)
                    self.shuffle_btn.config(state=tk.NORMAL)
                    self.reset_btn.config(state=tk.NORMAL)
                    self.prev_btn.config(state=tk.NORMAL)
                else:
                    self.root.after(300, lambda: animate_step(step + 1))

        animate_step(0)


def main():
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
