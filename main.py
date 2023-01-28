import numpy as np
import pygame
from pygame import Surface, SurfaceType


class Pattern:
	data: np.ndarray
	occurrences: int
	walls: list[np.ndarray]

	def __init__(self, data: np.ndarray, occurrences: int):
		self.data = data
		self.occurrences = occurrences
		self.walls = [data[0], data[-1], data[:, 0], data[:, -1]]

	def __str__(self):
		return f"data: {self.data}\noccurrences: {self.occurrences}"


class Cell:
	patterns: list[Pattern]
	x: int
	y: int
	entropy: float
	collapsed: bool
	final_pattern: Pattern | None

	def __init__(self, patterns: list[Pattern], y: int, x: int):
		self.patterns = patterns
		self.y = y
		self.x = x
		self.collapsed = False
		self.final_pattern = None

	def get_entropy(self) -> float:
		if self.collapsed:
			return 1
		try:
			occurrences = np.array([p.occurrences for p in self.patterns])
			weights = np.sum(occurrences)
			if weights == 0:
				return 100
			entropy = np.log(weights) - (np.sum(occurrences * np.log(occurrences)) / weights)
		except Exception as e:
			print("hello", e)
			entropy = 100
		return entropy

	def collapse(self) -> None:
		self.collapsed = True
		pattern_weights = np.array([x.occurrences for x in self.patterns])
		pattern_weights = pattern_weights / np.sum(pattern_weights)
		self.final_pattern = np.random.choice(self.patterns, p=pattern_weights)
		# self.final_pattern = np.random.choice(self.patterns)
		self.patterns = [self.final_pattern]

	def match_wall(self, wall, pos):
		self.patterns = [temp_pattern for temp_pattern in self.patterns if
		                 jaccard_similarity(temp_pattern.walls[pos], wall)>0.33]

	def __str__(self):
		return f"patterns: {self.patterns}\ny,x: {(self.y, self.x)}\ncollapsed: {self.collapsed}"


def jaccard_similarity(wall_a, wall_b):
	# convert to set
	wall_a = set(wall_a)
	wall_b = set(wall_b)
	# calculate jaccard similarity
	jaccard = float(len(wall_a.intersection(wall_b))) / len(wall_a.union(wall_b))
	return jaccard


def occ(thing):
	return thing.occurrences


def add_to_dic(dictionary, key) -> None:
	if str(key) in dictionary:
		dictionary[str(key)] += 1
	else:
		dictionary[str(key)] = 1


def find_lowest_entropy(cells: list[list[Cell]]) -> Cell:
	cells = np.array(cells)
	lowest = cells[0][0]
	for index in range(len(cells)):
		for cell in cells[index]:
			lowest_entropy = lowest.get_entropy()
			cell_entropy = cell.get_entropy()
			if lowest_entropy == cell_entropy or cell_entropy < lowest_entropy and cell.collapsed is False:
				lowest = cell
	return lowest


def get_neighbors(board: list[list[Cell]], pos: tuple[int, int]) -> list[tuple[Cell, int]]:
	ret: list[tuple[Cell, int]] = []
	if pos[0] > 0:
		ret.append((board[pos[0] - 1][pos[1]], 0))
	if pos[0] < len(board) - 1:
		ret.append((board[pos[0] + 1][pos[1]], 1))
	if pos[1] > 0:
		ret.append((board[pos[0]][pos[1] - 1], 2))
	if pos[1] < len(board[0]) - 1:
		ret.append((board[pos[0]][pos[1] + 1], 3))
	return ret


# def propagate(board: list[list[Cell]], origin: Cell):
# 	for neighbor in enumerate(get_neighbors(board, (origin.y, origin.x))):
# 		neighbor[1].match_wall(origin.final_pattern.walls[neighbor[0]], neighbor[0])
def propagate(board: list[list[Cell]], pos: tuple[int, int]) -> None:
	collapsed_cell = board[pos[0]][pos[1]]
	if collapsed_cell.collapsed is False:
		return
	neighbors = get_neighbors(board, pos)
	for neighbor in neighbors:
		neighbor[0].match_wall(collapsed_cell.final_pattern.walls[neighbor[1]], neighbor[1])


def draw_board(pixel_board: pygame.PixelArray, output: list[list[Cell]], size: int):
	for i_inner in range(0, len(pixel_board), size):
		for j_inner in range(0, len(pixel_board[0]), size):
			if output[int(i_inner / size)][int(j_inner / size)].collapsed is True:
				choice = output[int(i_inner / size)][int(j_inner / size)].final_pattern
			else:
				try:
					choice = output[int(i_inner / size)][int(j_inner / size)].patterns[0]
				# choice = np.random.choice(output[int(i_inner / size)][int(j_inner / size)].patterns)
				except Exception as e:
					print(e, (output[int(i_inner / size)][int(j_inner / size)].y,
					          output[int(i_inner / size)][int(j_inner / size)].x), "hello")
					print("______________________")
			for k_inner in range(size):
				for m_inner in range(size):
					pixel_board[i_inner + k_inner][j_inner + m_inner] = int(choice.data[k_inner][m_inner])

	return pixel_board


# Declaring variables
cell_size: int = 3
path: str = "Rooms.png"
output_size: tuple[int, int] = (120, 120)
input_image: Surface | SurfaceType = pygame.image.load(path)
input_size: tuple[int, int] = input_image.get_size()
screen: Surface | SurfaceType = pygame.display.set_mode(output_size)
patterns_raw: list[list[list[int]]] = []
patterns_cells: list[Pattern] = []
patterns_dict = {}
pixels: pygame.PixelArray = pygame.PixelArray(input_image)
# Creating the patterns
for i in range(0, input_size[0] - cell_size):
	for j in range(0, input_size[1] - cell_size):
		patterns_raw.append([])
		for k in range(0, cell_size):
			patterns_raw[-1].append([])
			for m in range(0, cell_size):
				patterns_raw[-1][-1].append(pixels[i + k][j + m])
		add_to_dic(patterns_dict, patterns_raw[-1])
patterns_raw = [element for index, element in enumerate(patterns_raw) if element not in patterns_raw[:index]]
for pattern in patterns_raw:
	patterns_cells.append(Pattern(np.array(pattern), patterns_dict[str(pattern)]))
	patterns_cells.sort(key=occ, reverse=True)
output_cells: list[list[Cell]] = []
for i in range(0, int(output_size[0] / cell_size)):
	output_cells.append([])
	for j in range(0, int(output_size[1] / cell_size)):
		output_cells[-1].append(Cell(patterns_cells[:], i, j))

counter = 0
while not output_cells[0][0].collapsed and counter < 500:
	counter += 1
	lowest_one = find_lowest_entropy(output_cells)
	lowest_one.collapse()
	propagate(output_cells, (lowest_one.y, lowest_one.x))
pygame.init()
a = draw_board(pygame.PixelArray(screen), output_cells, cell_size)
surf = a.make_surface()
a.close()
screen.blit(surf, (0, 0))
pixels.close()
pygame.image.save(screen, './pics/hello.jpeg')
pygame.quit()
