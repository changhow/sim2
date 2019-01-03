import numpy
import random
from flowers import Flowers
from bee import Bee
from grass import Grass
from air import Air

flower_colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'white']
food_availability = [None, 'N', 'P']
bee_colony_radius = 2
bee_visual_radius = 2
floral_constancy_multiplier = 20


class SimMap:

    def __init__(self, width, height):
        self.width = width - 1
        self.height = height - 1
        self.center = (width/2, height/2)
        self.grid = numpy.empty(shape=(width, height, 2), dtype=object)
        self.grid[:, :, 0] = Grass()
        self.grid[:, :, 1] = Air()
        self.flowers = []
        self.bees = []
        print(self.grid.shape)

    def add_flowers(self, x, y, color='red', fa='N'):
        flower = Flowers(x, y, color, fa)
        self.grid[x, y, 0] = flower
        self.flowers.append(flower)

    def add_flowers_patches(self, x, y, color, num_flower_patches, radius=5):
        xmin, xmax = x - radius, x + radius
        ymin, ymax = y - radius, y + radius
        if xmin <= 0:
            xmin = 0
        if ymin <= 0:
            ymin = 0
        if xmax >= self.width:
            xmax = self.width
        if ymax >= self.height:
            ymax = self.height

        for _ in range(num_flower_patches):
            xpos = random.randint(xmin, xmax)
            ypos = random.randint(ymin, ymax)

            self.add_flowers(xpos, ypos, color, random.choice(food_availability))

    def add_flowers_row(self, x, y, color, num_flower_patches, direction='v', distance=2):
        xpos = x
        ypos = y

        for _ in range(num_flower_patches):
            if xpos >= 0 and ypos >= 0 and xpos < self.width and ypos < self.height:
                self.add_flowers(xpos, ypos, color, random.choice(food_availability))
                if direction == 'v':
                    xpos += distance
                else:
                    ypos += distance

    def random_distribute_flowers_patches(self, num_flower_patches):
        for _ in range(num_flower_patches):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.add_flowers(x, y, random.choice(['red', 'green', 'blue', 'red', 'red']), random.choice(food_availability))

    def add_bees(self, x, y):
        bee = Bee(x, y)
        self.grid[x, y, 1] = bee
        self.bees.append(bee)

    def add_bee_colonies(self, x, y, number_of_bees):
        for _ in range(number_of_bees):
            self.add_bees(random.randint(x - bee_colony_radius, x + bee_colony_radius),
                          random.randint(y - bee_colony_radius, y + bee_colony_radius))
