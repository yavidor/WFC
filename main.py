import pygame
class WFC:
    def __init__(self, pattern_size, cell_size, data):
        self.pattern_size = pattern_size
        self.cell_size = cell_size
        self.data = data


class Cell:
    def __init__(self, occurrences, neighbors, data):
        self.occurrences = occurrences
        self.neighbors = neighbors
        self.data = data


print("Hello")
