import pygame
import pygame_menu
import random
from queue import PriorityQueue


menu_text = "Welcome to my pathfinding visualizer! \n" \
			"Here is how it works: Click where you want \n" \
			"to start and then where you want to end. You may \n" \
			"then click anywhere to add a wall and right click \n" \
			"to remove a wall. Pressing X will create an x-pattern, \n" \
			"R will generate a random maze, and Q will generate random \n" \
			"walls iteratively. When you're ready to visualize the path- \n" \
			"finding you can press space bar to visualize A*, D will \n" \
			"visualize Depth First Search, B will visualize Breadth \n" \
			"First Search, and G will visualize Greedy-Best-First search. \n" \
			"If you need to return here just hit M"

WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)




menu = pygame_menu.Menu("Visualizer Instructions", WIDTH, WIDTH, theme=pygame_menu.themes.THEME_BLUE)


# This class is the main object of the grid
# Each cell in the grid is one of these objects
class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# Simple heuristic function used to find distance between too spot objects
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2

	return abs(x1 - x2) + abs(y1 - y2)


# These 3 functions are used to recreate the path from the end to the start
# Each one is different since we need to handle the different path
# traversals
def reconstruct_path_astar(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def reconstruct_path_DFS(visited_list, draw):
	for node in visited_list:
		if node.color == PURPLE:
			continue
		node.make_path()
		draw()

def reconstruct_path_BFS(came_from, node, draw):
	while node in came_from:
		if came_from[node] == None:
			return
		node = came_from[node]
		node.make_path()
		draw()


# These next 4 functions are the search algorithms
def best_first_greedy(draw, start, end):

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	open = []
	visited = {}
	scores = {}

	open.append(start)
	visited[start] = None
	while len(open):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		vertex = open.pop(0)

		if vertex == end:
			reconstruct_path_BFS(visited, vertex, draw)
			end.make_end()
			return True

		for neighbor in vertex.neighbors:
			if neighbor not in visited:
				if vertex == end:
					reconstruct_path_BFS(visited, vertex, draw)
					end.make_end()
					return True

				scores[neighbor] = h(neighbor.get_pos(), end.get_pos())
				visited[neighbor] = vertex
				neighbor.make_open()
		if scores:
			node = min(scores, key=scores.get)
			open.append(node)
			del scores[node]
		else:
			vertex.make_closed()
			return

		draw()
		if vertex != start:
			vertex.make_closed()
	return


def BFS(draw, grid, start, end):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	came_from = {}
	visited_bool = {}
	queue = []

	for row in grid:
		for col in row:
			visited_bool[col] = False

	queue.append(start)
	visited_bool[start] = True

	while len(queue):
		vertex = queue.pop(0)

		if vertex == end:
			reconstruct_path_BFS(came_from, vertex, draw)
			end.make_end()
			return True

		for neighbor in vertex.neighbors:
			if not visited_bool[neighbor]:
				came_from[neighbor] = vertex
				if neighbor == end:
					reconstruct_path_BFS(came_from, neighbor, draw)
					end.make_end()
					return True

				queue.append(neighbor)
				visited_bool[neighbor] = True
				neighbor.make_open()

		draw()

		if vertex != start:
			vertex.make_closed()


def DFS(draw, start, end):
	stack = []
	visited_list = []


	stack.append(start)


	while len(stack):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		node = stack.pop()
		visited_list.append(node)
		if node.is_closed():
			continue

		if node == end:
			reconstruct_path_DFS(visited_list, draw)
			end.make_end()
			return True

		for neighbor in node.neighbors:
			if neighbor not in visited_list:

				if neighbor == end:
					reconstruct_path_DFS(visited_list, draw)
					end.make_end()
					return True

				stack.append(neighbor)
				neighbor.make_open()

		draw()

		if node != start:
			node.make_closed()

	return False



def aStar(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path_astar(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

# These functions handle the 3 versions of wall generation
def generate_random_walls(draw, grid, start, end):
	for row in grid:
		for col in row:
			x = random.random()
			x = x+0.28
			if x >= 1 and col != start and col != end:
				col.make_barrier()
		draw()

	return

def x_pattern(draw, grid, start, end, rows):
	for i in range(1, rows - 1):
		if grid[i][i] != start and grid[i][i] != end and grid[i][rows - 1 - i] != start and grid[i][rows - 1 - i] != end:
			grid[i][i].make_barrier()
			grid[i][rows - 1 - i].make_barrier()
			draw()

	return


def iterative_random_maze(draw, grid, start, end, rows, cols):
	count = 0
	while count < rows:
		x = random.randrange(0, rows - int(rows/2))
		for y in range(0, x):
			if grid[count][y] != start and grid[count][y] != end:
				grid[count][y].make_barrier()
				draw()
		count = count + 2

	count = 0
	while count < rows:
		x = random.randrange(0, int(rows/2))
		for y in range(0, x):
			if grid[count][rows - y - 1] != start and grid[count][rows - y - 1] != end:
				grid[count][rows - y - 1].make_barrier()
				draw()

		count = count + 1


	count = 0
	while count < cols:
		x = random.randrange(cols - int(cols / 2), cols-1)
		for y in range(0, x):
			if grid[y][count].is_barrier():
				grid[y - 1][count].reset()
				grid[y][count].reset()
				grid[y + 1][count].reset()
				grid[count][y+1].reset()
				continue
			else:
				grid[y][count].make_barrier()

			start.make_start()
			end.make_end()
			draw()
		count = count + 2




def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col



def close():
	menu.disable()

# This is the main loop that handles all of the events and drawing
def main(win, width):
	menu.enable()
	menu.full_reset()
	menu.add.label(menu_text)
	menu.add.button('Return to visualizer', close)


	ROWS = 30
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		if menu.is_enabled():
			menu.mainloop(WIN)
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					aStar(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_d and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					DFS(lambda: draw(win, grid, ROWS, width), start, end)
				if event.key == pygame.K_b and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					BFS(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_g and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					best_first_greedy(lambda: draw(win, grid, ROWS, width), start, end)
				if event.key == pygame.K_r and start and end:
					generate_random_walls(lambda: draw(win, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_q and start and end:
					iterative_random_maze(lambda: draw(win, grid, ROWS, width), grid, start, end, ROWS, ROWS)
				if event.key == pygame.K_x and start and end:
					x_pattern(lambda: draw(win, grid, ROWS, width), grid, start, end, ROWS)
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				if event.key == pygame.K_m:
					menu.enable()
					menu.mainloop(WIN)

	pygame.quit()





main(WIN, WIDTH)
