import tkinter as tk
from tkinter import messagebox
from solver import EightPuzzleSolver

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 8-Puzzle Solver")
        # الحالة الابتدائية (يمكنك تغييرها)
        self.current_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
        self.buttons = []
        self.create_widgets()
        self.update_grid()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()
        
        for i in range(9):
            btn = tk.Button(self.frame, text="", font=("Arial", 24, "bold"), 
                          width=4, height=2, bg="lightblue")
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
            
        self.solve_btn = tk.Button(self.root, text="Solve with AI (A*)", 
                                 command=self.animate_solution, bg="green", fg="white")
        self.solve_btn.pack(pady=10)

    def update_grid(self):
        for i, val in enumerate(self.current_state):
            text = str(val) if val != 0 else ""
            color = "white" if val == 0 else "lightblue"
            self.buttons[i].config(text=text, bg=color)

    def animate_solution(self):
        solver = EightPuzzleSolver(self.current_state)
        path = solver.solve_astar()
        
        if not path:
            messagebox.showinfo("Error", "No solution found!")
            return

        def apply_move(moves):
            if not moves:
                messagebox.showinfo("Done", "Puzzle Solved!")
                return
            
            move = moves.pop(0)
            state_list = list(self.current_state)
            zero_idx = state_list.index(0)
            
            # تحديد المكان الجديد بناءً على الحركة
            if move == "UP": new_idx = zero_idx - 3
            elif move == "DOWN": new_idx = zero_idx + 3
            elif move == "LEFT": new_idx = zero_idx - 1
            elif move == "RIGHT": new_idx = zero_idx + 1
            
            state_list[zero_idx], state_list[new_idx] = state_list[new_idx], state_list[zero_idx]
            self.current_state = tuple(state_list)
            self.update_grid()
            
            # سرعة الحركة (500 مللي ثانية بين كل خطوة)
            self.root.after(500, lambda: apply_move(moves))

        apply_move(path)

if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGUI(root)
    root.mainloop()