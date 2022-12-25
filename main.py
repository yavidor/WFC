import pygame
from pygame import Surface, SurfaceType


class Cell:
	up_wall: list[int]
	down_wall: list[int]
	left_wall: list[int]
	right_wall: list[int]

	def __init__(self, occurrences, neighbors, data):
		self.occurrences = occurrences
		self.neighbors = neighbors
		self.data = data


class WFC:
	cell_size: int
	screen: Surface | SurfaceType
	input_image: Surface | SurfaceType
	input_size: tuple[int, int]
	patterns: list[list[list[int]]]
	pixels: pygame.PixelArray

	def __init__(self, path: str, cell_size: int, output_size: tuple[int, int]):
		self.cell_size = cell_size
		self.input_image = pygame.image.load(path)
		self.input_size = self.input_image.get_size()
		self.screen = pygame.display.set_mode(output_size)
		self.patterns = []
		self.pixels = pygame.PixelArray(self.input_image)
		print(self.pixels)
		for i in range(0, self.input_size[0] - cell_size):
			for j in range(0, self.input_size[1] - cell_size):
				self.patterns.append([])
				for k in range(0, cell_size):
					self.patterns[-1].append([])
					for m in range(0, cell_size):
						self.patterns[-1][-1].append(self.pixels[j + m][i + k])
		print(self.patterns)
		self.patterns_dict = {}
		for pattern in self.patterns:
			add_to_dic(self.patterns_dict, pattern)
		print(self.patterns_dict)
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
