import SnakeEnv
import ddqn
import numpy as np
env = SnakeEnv.SnakeEnv(gui=True)
dqn = ddqn.Agent(alpha=0.001, gamma=0.95, n_actions=4, state_rank=21)

step = 0
def convert():
    v = np.array([[0, -1], [0, 1], [-1, 0], [1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]])
    d_fruit = np.zeros(8, float)
    d_danger = np.zeros(8, float)
    head = np.array(env.snake_pos[0])
    for t in range(1, env.game_board_size):
        for i in range(0, 8):
            if ((head+v[i]*t) >= 0).all() and ((head+v[i]*t) < env.game_board_size).all():
                if env.game_board[tuple(head + v[i]*t)] == 2:
                    d_fruit[i] = t / env.game_board_size
                if env.game_board[tuple(head + v[i]*t)] == 1 or env.game_board[tuple(head + v[i]*t)] == 3:
                    if d_danger[i] == 0:
                        d_danger[i] = t / env.game_board_size

    state = np.append(d_danger, d_fruit)
    state = np.append(state, env.snake_dir)
    state = np.append(state, step*0.01)

    return state


max_step = 100
learn_cnt = 0
score = 0
dqn.load_model()
dqn.epsilon = 0

while True:
    env.reset()
    step = 0
    while step < max_step:
        env.render()
        st = convert()
        at = dqn.choose_action(st)
        env.change_snake_dir(at)
        rt = env.step()
        done = False
        next_st = convert()
        rt *= 3
        if rt < 0:
            done = True
            env.reset()
            break

        else:
            if rt > 0:
                step = 0
            else:
                rt -= step * 0.01
                step += 1