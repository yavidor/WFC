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


class WFC:
	cell_size: int
	screen: Surface | SurfaceType
	input_image: Surface | SurfaceType
	input_size: tuple[int, int]
	patterns_raw: list[list[list[int]]]
	patterns_cells: list[Cell]
	pixels: pygame.PixelArray

	def __init__(self, path: str, cell_size: int, output_size: tuple[int, int]):
		self.cell_size = cell_size
		self.input_image = pygame.image.load(path)
		self.input_size = self.input_image.get_size()
		self.screen = pygame.display.set_mode(output_size)
		self.patterns_raw = []
		self.patterns_cells = []
		self.patterns_dict = {}
		self.pixels = pygame.PixelArray(self.input_image)
		print(self.pixels)
		for i in range(0, self.input_size[0] - cell_size):
			for j in range(0, self.input_size[1] - cell_size):
				self.patterns_raw.append([])
				for k in range(0, cell_size):
					self.patterns_raw[-1].append([])
					for m in range(0, cell_size):
						self.patterns_raw[-1][-1].append(self.pixels[j + m][i + k])
				add_to_dic(self.patterns_dict, self.patterns_raw[-1])
		print(self.patterns_raw)
		print(len(self.patterns_raw))
		self.patterns_raw = [el for index, el in enumerate(self.patterns_raw) if el not in self.patterns_raw[:index]]
		print(len(self.patterns_raw))
		print(self.patterns_dict)
		for pattern in self.patterns_raw:
			self.patterns_cells.append(Cell(pattern, self.patterns_dict[str(pattern)]))
		# print(self.patterns_cells[0])
		self.patterns_cells.sort(key=occ, reverse=True)
		# print(self.patterns_cells[0])
		for cell in self.patterns_cells:
			print(cell)
		self.pixels.close()


def add_to_dic(dictionary, key):
	if str(key) in dictionary:
		dictionary[str(key)] += 1
	else:
		dictionary[str(key)] = 1


pygame.init()
wfc = WFC('Rooms.png', 3, (120, 120))
wfc.screen.blit(wfc.input_image, (0, 0))
print(wfc.screen.get_size())
pygame.display.flip()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

# Quit Pygame
pygame.quit()
