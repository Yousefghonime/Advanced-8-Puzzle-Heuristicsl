from solver import EightPuzzleSolver

def print_board(state):
    for i in range(0, 9, 3):
        print(f"{state[i]} {state[i+1]} {state[i+2]}")
    print("-" * 10)

if __name__ == "__main__":
    # مثال للحالة الابتدائية (يمكنك تغييرها)
    # 0 يمثل المربع الفارغ
    initial_puzzle = [1, 2, 5, 3, 4, 0, 6, 7, 8]
    
    print("--- 8-Puzzle Solver ---")
    print("Initial Board:")
    print_board(initial_puzzle)
    
    solver = EightPuzzleSolver(initial_puzzle)
    
    print("Solving with A* (Manhattan)...")
    path = solver.solve_astar()
    
    if path:
        print(f"Solution found in {len(path)} moves!")
        print("Path:", " -> ".join(path))
    else:
        print("No solution exists.")