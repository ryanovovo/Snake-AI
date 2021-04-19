import SnakeEnv
import numpy as np


env = SnakeEnv.SnakeEnv(gui=True)
hamiltonian_cycle = np.zeros((10, 10, 4), int)


for j in range(1, 9):
    if j % 2 == 1:
        for i in range(2, 9):
            hamiltonian_cycle[i][j] = [0, 0, 0, 1]
    elif j % 2 == 0:
        for i in range(8, 1, -1):
            hamiltonian_cycle[i][j] = [0, 0, 1, 0]

for i in range(2, 9):
    hamiltonian_cycle[1][i] = [1, 0, 0, 0]

for i in range(1, 9):
    if i % 2 == 1:
        hamiltonian_cycle[8][i] = [0, 1, 0, 0]
    elif i % 2 == 0:
        hamiltonian_cycle[2][i] = [0, 1, 0, 0]

hamiltonian_cycle[1][1] = [0, 0, 0, 1]
hamiltonian_cycle[2][8] = [0, 0, 1, 0]
print(hamiltonian_cycle)

while True:
    head = env.snake_pos[0]
    at = hamiltonian_cycle[tuple(head)]
    env.change_snake_dir(at)
    env.step()
    print(at)
    env.render()

