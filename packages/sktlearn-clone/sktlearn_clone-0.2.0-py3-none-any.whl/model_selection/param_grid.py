import numpy as np

class ParameterGrid:
    def __init__(self, param_grid):
        self.param_grid = param_grid
        self.keys = list(param_grid)
        self.param_grid_values = [param_grid[key] for key in self.keys]
        self.grid_size = np.prod([len(v) for v in self.param_grid_values])

    def __iter__(self):
        for i in range(self.grid_size):
            params = {}
            for j, key in enumerate(self.keys):
                idx = int((i // np.prod([len(v) for v in self.param_grid_values[j+1:]])) % len(self.param_grid_values[j]))
                params[key] = self.param_grid_values[j][idx]
            yield params


    def __len__(self):
        return self.grid_size
