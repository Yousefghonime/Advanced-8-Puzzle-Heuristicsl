
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

from core.utils import board_to_2d, board_to_1d
from algorithms import bfs, dfs, ucs, astar

N = 3
SIZE = N * N

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle AI Solver")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")

        self.numbers = list(range(1, SIZE)) + [0]
        self.goal_state = list(range(1, SIZE)) + [0]
        self.current_state = self.numbers.copy()

        self.buttons = []
        self.moves = 0
        self.start_time = None
        self.timer_running = False
        self.is_solving = False
        self.solution_steps = []
        self.current_step = 0

        self.algorithms = ["BFS", "DFS", "UCS", "A*"]
        self.create_widgets()
        self.shuffle_puzzle()
        self.update_display()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = tk.Label(main_frame, text="8-Puzzle AI Solver",
                               font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=(0, 20))

        left_panel = tk.Frame(main_frame, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        puzzle_frame = tk.Frame(left_panel, bg="#333", bd=3, relief=tk.RAISED)
        puzzle_frame.pack(pady=10)

        self.buttons = []
        for i in range(N):
            row_buttons = []
            for j in range(N):
                btn = tk.Button(
                    puzzle_frame, text="", font=("Arial", 28, "bold"),
                    width=4, height=2, bd=3, relief=tk.RAISED,
                    bg="#4FC3F7", activebackground="#29B6F6",
                    command=lambda r=i, c=j: self.tile_click(r, c)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        info_frame = tk.Frame(left_panel, bg="#f0f0f0")
        info_frame.pack(pady=15)

        self.moves_label = tk.Label(info_frame, text="Moves: 0", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.moves_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(info_frame, text="Time: 00:00", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.timer_label.pack(side=tk.LEFT, padx=20)

        control_frame = tk.Frame(left_panel, bg="#f0f0f0")
        control_frame.pack(pady=10)

        self.shuffle_btn = tk.Button(control_frame, text=" Shuffle", font=("Arial", 12, "bold"),
                                     bg="#4CAF50", fg="white", padx=20, pady=8, command=self.shuffle_puzzle)
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(control_frame, text=" Reset", font=("Arial", 12, "bold"),
                                   bg="#2196F3", fg="white", padx=20, pady=8, command=self.reset_game)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        right_panel = tk.Frame(main_frame, bg="#e0e0e0", bd=2, relief=tk.SUNKEN)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))

        algo_frame = tk.LabelFrame(right_panel, text="Search Algorithms",
                                   font=("Arial", 14, "bold"), bg="#e0e0e0", padx=15, pady=15)
        algo_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(algo_frame, text="Select Algorithm:", font=("Arial", 12), bg="#e0e0e0").pack(anchor="w")
        self.algo_var = tk.StringVar(value="A*")
        self.algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var,
                                       values=self.algorithms, state="readonly", font=("Arial", 11), width=15)
        self.algo_combo.pack(fill=tk.X, pady=5)

        self.solve_btn = tk.Button(algo_frame, text=" Solve Puzzle", font=("Arial", 13, "bold"),
                                   bg="#FF9800", fg="white", padx=20, pady=10, command=self.solve_puzzle)
        self.solve_btn.pack(pady=10)

        info_frame2 = tk.LabelFrame(right_panel, text="Algorithm Properties",
                                    font=("Arial", 12, "bold"), bg="#e0e0e0", padx=10, pady=10)
        info_frame2.pack(fill=tk.X, padx=10, pady=5)

        info_text = (
            "• BFS: Complete & Optimal (memory intensive)
"
            "• DFS: Not optimal (depth limited)
"
            "• UCS: Complete & Optimal (considers costs)
"
            "• A*: Complete & Optimal (most efficient)"
        )
        info_label = tk.Label(info_frame2, text=info_text, font=("Arial", 9),
                              bg="#e0e0e0", fg="#555", justify=tk.LEFT)
        info_label.pack()

        solution_frame = tk.LabelFrame(right_panel, text="Solution Controls",
                                       font=("Arial", 14, "bold"), bg="#e0e0e0", padx=15, pady=15)
        solution_frame.pack(fill=tk.X, padx=10, pady=10)

        nav_frame = tk.Frame(solution_frame, bg="#e0e0e0")
        nav_frame.pack(pady=5)

        self.prev_btn = tk.Button(nav_frame, text="◀ Previous", font=("Arial", 11),
                                  bg="#607D8B", fg="white", state=tk.DISABLED, command=self.prev_step)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(nav_frame, text="Next ▶", font=("Arial", 11),
                                  bg="#607D8B", fg="white", state=tk.DISABLED, command=self.next_step)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.play_btn = tk.Button(solution_frame, text="▶ Play Solution", font=("Arial", 11),
                                  bg="#009688", fg="white", state=tk.DISABLED, command=self.play_solution)
        self.play_btn.pack(pady=5)

        results_frame = tk.LabelFrame(right_panel, text="Performance Results",
                                      font=("Arial", 14, "bold"), bg="#e0e0e0", padx=15, pady=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.results_text = tk.Text(results_frame, height=15, width=35,
                                    font=("Consolas", 10), bg="white", relief=tk.SUNKEN, bd=2)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.results_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_text.yview)

        self.results_text.insert(tk.END, "Performance Results
")
        self.results_text.insert(tk.END, "=" * 30 + "

")
        self.results_text.insert(tk.END, "Select algorithm and click 'Solve Puzzle'
")
        self.results_text.insert(tk.END, "to see detailed metrics.
")

    # Helpers
    def board_to_2d(self, flat): return board_to_2d(flat, N)
    def board_to_1d(self, grid): return board_to_1d(grid)

    def shuffle_puzzle(self):
        self.stop_timer()
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 00:00")
        while True:
            random.shuffle(self.numbers)
            inversions = 0
            for i in range(SIZE):
                if self.numbers[i] == 0: continue
                for j in range(i + 1, SIZE):
                    if self.numbers[j] != 0 and self.numbers[i] > self.numbers[j]:
                        inversions += 1
            if inversions % 2 == 0:
                break
        self.current_state = self.numbers.copy()
        self.update_display()
        self.clear_solution()

    def reset_game(self):
        self.shuffle_puzzle()

    def update_display(self):
        for i in range(N):
            for j in range(N):
                idx = i * N + j
                value = self.current_state[idx]
                if value == 0:
                    self.buttons[i][j].config(text="", bg="#BDBDBD")
                else:
                    self.buttons[i][j].config(text=str(value), bg="#4FC3F7")

    def find_empty_idx(self):
        for i in range(SIZE):
            if self.current_state[i] == 0:
                return i
        return -1

    def tile_click(self, row, col):
        if self.is_solving:
            return
        idx = row * N + col
        empty_idx = self.find_empty_idx()
        row_diff = abs(row - (empty_idx // N))
        col_diff = abs(col - (empty_idx % N))
        if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
            self.current_state[empty_idx], self.current_state[idx] = self.current_state[idx], self.current_state[empty_idx]
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            if not self.timer_running:
                self.start_timer()
            self.update_display()
            if self.current_state == self.goal_state:
                self.stop_timer()
                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {self.moves} moves!")

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

    def clear_solution(self):
        self.solution_steps = []
        self.current_step = 0
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.play_btn.config(state=tk.DISABLED)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Performance Results
")
        self.results_text.insert(tk.END, "=" * 30 + "

")
        self.results_text.insert(tk.END, "Select algorithm and click 'Solve Puzzle'
")
        self.results_text.insert(tk.END, "to see detailed metrics.
")

    def solve_puzzle(self):
        if self.is_solving:
            return
        self.is_solving = True
        self.solve_btn.config(state=tk.DISABLED)
        self.shuffle_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

        start_board = self.board_to_2d(self.current_state)
        goal_board = self.board_to_2d(self.goal_state)
        algo = self.algo_var.get()

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Solving with {algo}...
")
        self.root.update()

        try:
            if algo == "BFS":
                path, stats = bfs.solve(start_board, goal_board)
            elif algo == "DFS":
                path, stats = dfs.solve(start_board, goal_board)
            elif algo == "UCS":
                path, stats = ucs.solve(start_board, goal_board)
            elif algo == "A*":
                path, stats = astar.solve(start_board, goal_board)
            else:
                path, stats = [], {'solution_found': False}
        except Exception as e:
            self.results_text.insert(tk.END, f"Error: {e}
")
            path, stats = [], {'solution_found': False}

        if stats.get('solution_found'):
            self.results_text.insert(tk.END, f" {algo} Solution Found!
")
            self.results_text.insert(tk.END, "=" * 40 + "

")
            self.solution_steps = [self.board_to_1d(s.board) for s in path]
            self.current_step = 0
            if len(self.solution_steps) > 1:
                self.next_btn.config(state=tk.NORMAL)
                self.play_btn.config(state=tk.NORMAL)
            self._print_stats(stats, algo)
        else:
            self.results_text.insert(tk.END, f" {algo}: No Solution Found
")
            self.results_text.insert(tk.END, "=" * 40 + "

")
            self._print_stats(stats, algo)
            if algo == "DFS":
                self.results_text.insert(tk.END, "
Note: DFS depth limit (50) reached.
")
                self.results_text.insert(tk.END, "Try BFS, UCS, or A* for guaranteed solution.
")

        self.results_text.see(tk.END)
        self.is_solving = False
        self.solve_btn.config(state=tk.NORMAL)
        self.shuffle_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)

    def _print_stats(self, stats, algo):
        self.results_text.insert(tk.END, "PERFORMANCE METRICS:
")
        self.results_text.insert(tk.END, "─" * 20 + "
")
        self.results_text.insert(tk.END, f"• Solution Path: {stats.get('path_length', 0)} moves
")
        self.results_text.insert(tk.END, f"• Time Taken: {stats.get('execution_time', 0):.4f} seconds
")
        self.results_text.insert(tk.END, f"• Nodes Expanded: {stats.get('nodes_expanded', 0):,}
")
        self.results_text.insert(tk.END, f"• States Visited: {stats.get('visited_states', 0):,}
")
        self.results_text.insert(tk.END, f"• Max Frontier Size: {stats.get('max_frontier', 0):,}
")

        self.results_text.insert(tk.END, "
ALGORITHM PROPERTIES:
")
        self.results_text.insert(tk.END, "─" * 20 + "
")
        if algo == "BFS":
            self.results_text.insert(tk.END, "• Completeness: Yes
• Optimality: Yes
• Time Complexity: O(b^d)
• Space Complexity: O(b^d)
")
        elif algo == "DFS":
            self.results_text.insert(tk.END, "• Completeness: Limited (depth)
• Optimality: No
• Time Complexity: O(b^m)
• Space Complexity: O(bm)
")
        elif algo == "UCS":
            self.results_text.insert(tk.END, "• Completeness: Yes
• Optimality: Yes
• Time Complexity: O(b^{C*/ε})
• Space Complexity: O(b^{C*/ε})
")
        elif algo == "A*":
            self.results_text.insert(tk.END, "• Completeness: Yes
• Optimality: Yes
• Time Complexity: O(b^d)
• Space Complexity: O(b^d)
• Heuristic Used: Manhattan Distance
")

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
