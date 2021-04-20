import tensorflow.keras.models
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import mse
from tensorflow.keras.models import Sequential
import numpy as np
import random


class Buffer:
    def __init__(self, mem_size, n_actions, state_rank):
        # init buffer
        self.mem_size = mem_size
        self.state_mem = np.zeros((mem_size, state_rank), int)
        self.action_mem = np.zeros((mem_size, n_actions), int)
        self.reward_mem = np.zeros(mem_size, int)
        self.next_state_mem = np.zeros((mem_size, state_rank), int)
        self.terminal_mem = np.zeros(mem_size, int)
        self.mem_ctr = 0

    def sample(self, batch_size):
        if self.mem_ctr < batch_size:
            idx = self.mem_ctr
            return self.state_mem[0:idx], self.action_mem[0:idx], self.reward_mem[0:idx], self.next_state_mem[0:idx], self.terminal_mem[0:idx]
        else:
            idx = np.random.choice(min(self.mem_ctr, self.mem_size), batch_size)
            return self.state_mem[idx], self.action_mem[idx], self.reward_mem[idx], self.next_state_mem[idx], self.terminal_mem[idx]

    def store(self, st, at, rt, next_st, done):
        assert st.ndim == 1
        idx = self.mem_ctr % self.mem_size
        self.state_mem[idx] = st
        self.action_mem[idx] = at
        self.reward_mem[idx] = rt
        self.next_state_mem[idx] = next_st
        self.terminal_mem[idx] = done
        self.mem_ctr += 1




def build_nn(n_actions, state_dim, lr):
    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=(state_dim, )))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(n_actions))
    model.compile(optimizer=Adam(lr=lr), loss='mse')
    return model


class Agent:
    def __init__(self, alpha, gamma, n_actions, state_rank, epsilon=1.0, epsilon_dec=0.001, epsilon_min=0.1, batch_size=5000, mem_size=100000):
        self.n_actions = n_actions
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.alpha = alpha
        self.gamma = gamma
        self.memory = Buffer(mem_size, n_actions, state_rank)
        self.q_eval = build_nn(n_actions, state_rank, self.alpha)
        self.q_target = build_nn(n_actions, state_rank, self.alpha)
        self.action_space = np.zeros((n_actions, n_actions), int)
        self.learn_ctr = 0
        for i in range(0, n_actions):
            self.action_space[i][i] = 1

    def train(self, st, at, rt, next_st, done):
        if st.ndim == 1:
            st = st.reshape(1, len(st))
            next_st = next_st.reshape(1, len(next_st))
            at = at.reshape(1, self.n_actions)
            rt = np.full(1, rt)
            done = np.full(1, done)

        q_eval_predict = self.q_eval.predict(st)
        q_eval_next_predict = self.q_eval.predict(next_st)
        q_target = q_eval_predict.copy()
        q_target_next_predict = self.q_target.predict(next_st)
        for i in range(0, len(q_target)):
            q_target[i][np.argmax(at[i])] = self.gamma * (rt[i] + q_target_next_predict[i][np.argmax(q_eval_next_predict[i])])
            if done[i] == True:
                q_target[i][np.argmax(at[i])] = rt[i]

        self.q_eval.fit(st, q_target, verbose=1)
        self.learn_ctr += len(q_target)
        if self.learn_ctr > 100:
            self.copy_model()
            self.learn_ctr = 0

    def choose_action(self, st):
        if st.ndim == 1:
            st = st.reshape(1, len(st))

        rand = random.random()
        action = None
        if self.epsilon > rand:
            idx = random.randint(0, self.n_actions-1)
            action = self.action_space[idx]
        else:
            action = self.q_eval.predict(st)
        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_dec

        return action

    def learn_from_buffer(self):
        st, at, rt, next_st, done = self.memory.sample(self.batch_size)
        self.train(st, at, rt, next_st, done)

    def save_model(self):
        self.q_eval.save("beta_model.h5")

    def load_model(self):
        self.q_eval = tensorflow.keras.models.load_model("beta_model.h5")

    def copy_model(self):
        self.q_target.set_weights(self.q_eval.get_weights())
