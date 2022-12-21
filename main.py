from typing import Tuple

import pygame
from pygame import Surface, SurfaceType


class Cell:
	def __init__(self, occurrences, neighbors, data):
		self.occurrences = occurrences
		self.neighbors = neighbors
		self.data = data


class WFC:
	screen: Surface | SurfaceType
	pattern: Surface | SurfaceType
	pattern_size: tuple[int, int]
	cell_size: int

	def __init__(self, path, cell_size, output_size):
		self.path = path
		self.pattern = pygame.image.load(path)
		self.pattern_size = self.pattern.get_size()
		self.screen = pygame.display.set_mode(output_size)
		self.cell_size = cell_size


pygame.init()
wfc = WFC('Rooms.png', 3, (120, 120))
wfc.screen.blit(wfc.pattern, (0, 0))
print(wfc.screen.get_size())
pygame.display.flip()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

# Quit Pygame
pygame.quit()
