class Board:
    def __init__(self, state):
        self.state = tuple(state)
        self.size = 3

    def get_empty_pos(self):
        return self.state.index(0)

    def get_neighbors(self):
        neighbors = []
        zero_pos = self.get_empty_pos()
        r, c = divmod(zero_pos, self.size)
        
        directions = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for dr, dc, move in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                new_state = list(self.state)
                target_idx = nr * self.size + nc
                new_state[zero_pos], new_state[target_idx] = new_state[target_idx], new_state[zero_pos]
                neighbors.append((tuple(new_state), move))
        return neighbors