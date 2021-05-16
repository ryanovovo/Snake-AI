import numpy as np
from collections import deque
import random
import time
from findpath import Search

class SnakeEnv:
	def __init__(self, game_board_size=10, snake_color=(255, 0, 0), fruit_color=(0, 255, 0), gui = False):
		# initialize gui
		# ---------------------------------------------------
		if gui:
			# import required libraries
			global pygame
			import pygame
			global freetype
			import pygame.freetype as freetype

			self.screen = pygame.display.set_mode((game_board_size*50, game_board_size*50))
			pygame.display.set_caption("貪食蛇")
			self.clock = pygame.time.Clock()
			pygame.freetype.init()
			self.score_font = pygame.freetype.Font(r"C:\Users\wang\PycharmProjects\Snake-Ai\fonts\font1.otf", 18)

		# initialize game_board
		# ---------------------------------------------------
		self.game_board_size = game_board_size
		self.game_board = np.zeros((game_board_size, game_board_size), int)
		for i in range(0, self.game_board_size):  # create wall (3)
			self.game_board[i][0] = 3
			self.game_board[i][self.game_board_size-1] = 3
			self.game_board[0][i] = 3
			self.game_board[self.game_board_size - 1][i] = 3

		# ---------------------------------------------------

		# initialize snake
		# ---------------------------------------------------
		self.snake_color = snake_color
		self.snake_pos = deque()
		init_snake_pos = [random.randint(1, self.game_board_size - 2), random.randint(1, self.game_board_size - 2)]
		self.snake_pos.append(init_snake_pos)
		self.game_board[tuple(init_snake_pos)] = 1
		self.snake_dir = np.zeros(4, int)  # one hot encoding up, down, left, right
		self.snake_score = 0
		# ---------------------------------------------------

		# initialize fruit
		# ---------------------------------------------------
		self.fruit_color = fruit_color
		empty_space = np.argwhere(self.game_board == 0)
		self.fruit_pos = empty_space[random.randint(1, np.size(empty_space, 0)-1)]
		self.fruit_score = 1
		self.game_board[tuple(self.fruit_pos)] = 2
		# ---------------------------------------------------

	def reset(self):
		# reset game_board
		# ---------------------------------------------------
		self.game_board = np.zeros((self.game_board_size, self.game_board_size), int)
		for i in range(0, self.game_board_size):  # create wall (3)
			self.game_board[i][0] = 3
			self.game_board[i][self.game_board_size - 1] = 3
			self.game_board[0][i] = 3
			self.game_board[self.game_board_size - 1][i] = 3
		# ---------------------------------------------------

		# reset snake
		# ---------------------------------------------------
		self.snake_pos.clear()
		init_snake_pos = [random.randint(1, self.game_board_size - 2), random.randint(1, self.game_board_size - 2)]
		self.snake_pos.append(init_snake_pos)
		self.game_board[tuple(init_snake_pos)] = 1
		self.snake_dir = np.zeros(4, int)  # one hot encoding up, down, left, right
		self.snake_score = 0
		# ---------------------------------------------------

		# reset fruit
		# ---------------------------------------------------
		empty_space = np.argwhere(self.game_board == 0)
		self.fruit_pos = empty_space[random.randint(1, np.size(empty_space, 0) - 1)]
		self.fruit_score = 1
		self.game_board[tuple(self.fruit_pos)] = 2
		# ---------------------------------------------------

	def new_fruit(self):
		# new a fruit on the game_board
		empty_space = np.argwhere(self.game_board == 0)
		self.game_board[tuple(self.fruit_pos)] = 0
		self.fruit_pos = empty_space[random.randint(1, np.size(empty_space, 0) - 1)]
		self.fruit_score = 1
		self.game_board[tuple(self.fruit_pos)] = 2

	def change_snake_dir(self, new_dir): # new_dir should be one hot encoded
		# change snake direction to new_dir
		self.snake_dir = np.array(new_dir)

	def step(self):
		# move snake by snake_dir and return collections, eaten fruit or normal exit
		actions = np.array([[0, -1], [0, 1], [-1, 0], [1, 0]])
		if (self.snake_dir == 0).all():
			# no input
			return 0
		new_head = np.array(self.snake_pos[0]) + actions[np.argmax(self.snake_dir)]
		if self.game_board[tuple(new_head)] == 1 or self.game_board[tuple(new_head)] == 3:
			# collections
			print(new_head)
			return -1
		elif self.game_board[tuple(new_head)] == 2:
			# eaten a fruit
			self.new_fruit()
			self.snake_pos.appendleft(new_head)
			self.snake_score += self.fruit_score
			self.game_board[tuple(new_head)] = 1
			return 1
		else:
			# normal exit
			self.game_board[tuple(self.snake_pos[-1])] = 0
			self.game_board[tuple(new_head)] = 1
			self.snake_pos.appendleft(new_head)
			self.snake_pos.pop()
			return 0

	def render(self):
		# render the snake game gui
		# pygame stuff
		# ---------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				break
		self.clock.tick(60)
		self.screen.fill((255, 255, 255))
		# ---------------------------------------------------

		# draw snake, fruit, and wall on screen
		# ---------------------------------------------------
		for i in range(0, self.game_board_size):
			for j in range(0, self.game_board_size):
				if self.game_board[i][j] == 1:
					pygame.draw.rect(self.screen, (255, 0, 0), (i*50, j*50, 50, 50))
				elif self.game_board[i][j] == 2:
					pygame.draw.rect(self.screen, (0, 255, 0), (i * 50, j * 50, 50, 50))
				elif self.game_board[i][j] == 3:
					pygame.draw.rect(self.screen, (0, 0, 255), (i * 50, j * 50, 50, 50))
		# ---------------------------------------------------

		# show snake score on screen
		# ---------------------------------------------------
		self.score_font.render_to(self.screen, (1, 1), "Score:" + str(self.snake_score), (0, 0, 0), None, size=20)
		pygame.display.update()
		time.sleep(0.3) # move speed
		# ---------------------------------------------------

	def keyboard_control(self):
		# use keyboard manual control snake
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.change_snake_dir([1, 0, 0, 0])
				elif event.key == pygame.K_DOWN:
					self.change_snake_dir([0, 1, 0, 0])
				elif event.key == pygame.K_LEFT:
					self.change_snake_dir([0, 0, 1, 0])
				elif event.key == pygame.K_RIGHT:
					self.change_snake_dir([0, 0, 0, 1])

def go(pathList):
	while True:
		for i in range(0, len(pathList) - 1):
			this = pathList[i]
			next = pathList[i + 1]
			if (this[0] > next[0]):
				env.change_snake_dir([1, 0, 0, 0])
			if (this[0] < next[0]):
				env.change_snake_dir([0, 1, 0, 0])
			if (this[1] > next[1]):
				env.change_snake_dir([0, 0, 1, 0])
			if (this[1] < next[1]):
				env.change_snake_dir([0, 0, 0, 1])
			env.step()
			env.render()
			if env.step() == -1:
				env.reset()
#snake walk based on the pathList

env = SnakeEnv(gui=True)
pathList = Search(env.snake_pos[0])
go(pathList)
