import random


class Flowers:

    def __init__(self, x, y, color='red', fa='N'):
        self.color = color
        self.food_availability = fa
        self.pos = (x, y)
        self.tag = 'FL'
        self.scent = random.randint(0, 100)
        self.pheromone = 100 - self.scent
