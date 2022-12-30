import pygame
from pygame import Surface, SurfaceType


class Cell:
	data: list[list[int]]
	occurrences: int
	up_wall: list[int]
	down_wall: list[int]
	left_wall: list[int]
	right_wall: list[int]

	def __init__(self, data: list[list[int]], occurrences: int):
		self.occurrences = occurrences
		self.data = data
		self.up_wall = []
		for cell in data[0]:
			self.up_wall.append(cell)
		self.down_wall = []
		for cell in data[-1]:
			self.down_wall.append(cell)
		self.left_wall = []
		for i in range(len(data)):
			self.left_wall.append(data[i][0])
		self.right_wall = []
		for i in range(len(data)):
			self.right_wall.append(data[i][-1])

	def __str__(self):
		return f"data: {self.data}\noccurrences: {self.occurrences}\nUp Wall: {self.up_wall}\nDown Wall: {self.down_wall}\n" \
	f"Left Wall: {self.left_wall}\nRight Wall: {self.right_wall} "


def occ(thing):
	return thing.occurrences


def add_to_dic(dictionary, key):
	if str(key) in dictionary:
		dictionary[str(key)] += 1
	else:
		dictionary[str(key)] = 1


cell_size: int = 3
path: str = "Rooms.png"
output_size: tuple[int, int] = (120, 120)
input_image: Surface | SurfaceType = pygame.image.load(path)
input_size: tuple[int, int] = input_image.get_size()
screen: Surface | SurfaceType = pygame.display.set_mode(output_size)
patterns_raw: list[list[list[int]]] = []
patterns_cells: list[Cell] = []
patterns_dict = {}
pixels: pygame.PixelArray = pygame.PixelArray(input_image)
print(pixels)
for i in range(0, input_size[0] - cell_size):
	for j in range(0, input_size[1] - cell_size):
		patterns_raw.append([])
		for k in range(0, cell_size):
			patterns_raw[-1].append([])
			for m in range(0, cell_size):
				patterns_raw[-1][-1].append(pixels[j + m][i + k])
		add_to_dic(patterns_dict, patterns_raw[-1])
print(patterns_raw)
print(len(patterns_raw))
patterns_raw = [el for index, el in enumerate(patterns_raw) if el not in patterns_raw[:index]]
print(len(patterns_raw))
print(patterns_dict)
for pattern in patterns_raw:
	patterns_cells.append(Cell(pattern, patterns_dict[str(pattern)]))
	patterns_cells.sort(key=occ, reverse=True)
for cell in patterns_cells:
	print(cell)
pixels.close()
pygame.init()
pygame.display.flip()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

# Quit Pygame
pygame.quit()
