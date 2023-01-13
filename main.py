import math
import random
import pygame
from pygame import Surface, SurfaceType


class Pattern:
	data: list[list[int]]
	occurrences: int
	up_wall: list[int]
	down_wall: list[int]
	left_wall: list[int]
	right_wall: list[int]

	def __init__(self, data: list[list[int]], occurrences: int):
		self.data = data
		self.occurrences = occurrences
		self.up_wall = []
		for cell in data[0]:
			self.up_wall.append(cell)
		self.down_wall = []
		for cell in data[-1]:
			self.down_wall.append(cell)
		self.left_wall = []
		self.right_wall = []
		for index in range(len(data)):
			self.left_wall.append(data[index][0])
			self.right_wall.append(data[index][-1])

	def __str__(self):
		return f"data: {self.data}\noccurrences: {self.occurrences}\nUp Wall: {self.up_wall}\nDown Wall: {self.down_wall}\n" \
		       f"Left Wall: {self.left_wall}\nRight Wall: {self.right_wall}"


class Cell:
	patterns: list[Pattern]
	x: int
	y: int
	entropy: float
	collapsed: bool
	final_pattern: Pattern | None

	def __init__(self, patterns: list[Pattern], x: int, y: int):
		self.patterns = patterns
		self.x = x
		self.y = y
		self.collapsed = False
		self.final_pattern = None

	def get_entropy(self) -> float:
		weights = sum(p.occurrences for p in self.patterns)
		entropy = math.log(weights, len(self.patterns)) - (
				sum(p.occurrences * math.log(p.occurrences, len(self.patterns)) for p in
				    self.patterns) / weights)
		return entropy

	def collapse(self) -> None:
		self.collapsed = True
		self.final_pattern = random.choice(self.patterns)
		self.patterns = []

	def __str__(self):
		return f"patterns: {self.patterns}\nx: {self.x}\ny: {self.y}"


def occ(thing):
	return thing.occurrences


def add_to_dic(dictionary, key) -> None:
	if str(key) in dictionary:
		dictionary[str(key)] += 1
	else:
		dictionary[str(key)] = 1


def find_lowest_entropy(cells: list[list[Cell]]) -> Cell:
	lowest = cells[0][0]
	print(lowest)
	for index in range(len(cells)):
		for cell in cells[index]:
			lowest_entropy = lowest.get_entropy()
			cell_entropy = cell.get_entropy()
			if (lowest_entropy == cell_entropy and random.random() > 0.5) or cell_entropy < lowest_entropy:
				lowest = cell
	return lowest


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
				patterns_raw[-1][-1].append(pixels[j + m][i + k])
		add_to_dic(patterns_dict, patterns_raw[-1])
patterns_raw = [element for index, element in enumerate(patterns_raw) if element not in patterns_raw[:index]]
for pattern in patterns_raw:
	patterns_cells.append(Pattern(pattern, patterns_dict[str(pattern)]))
	patterns_cells.sort(key=occ, reverse=True)
output_cells: list[list[Cell]] = []
for i in range(0, int(output_size[0] / cell_size)):
	output_cells.append([])
	for j in range(0, int(output_size[1] / cell_size)):
		output_cells[-1].append(Cell(patterns_cells, i, j))

pixels.close()
# pygame.init()
print(find_lowest_entropy(output_cells))
# pygame.image.save(screen, './pics/hello.jpeg')
# pygame.quit()
