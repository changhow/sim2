from pheromone import Pheromone
import random


class Bee:

    def __init__(self, x, y):
        self.pos = [x, y]
        self.flower_sequence = []
        self.tag = 'BEE'
        self.flower_list = []
        self.food_capacity = 0
        self.next_flower_color = 'red'
        self.next_flower = None
        self.pheromone = Pheromone()
        self.reach_target_flower = False
        self.speed = (0, 0)
        self.visual_radius = 2
        self.levy = 1
        self.floral_constancy = 100
        self.task_complete = False

    def compute_target_flower_distance(self):
        dx = self.next_flower.pos[0] - self.pos[0]
        dy = self.next_flower.pos[1] - self.pos[1]

        return dx, dy

    def move(self):
        dx, dy = self.compute_target_flower_distance()

        """ NW | N | NE
            ------------ 
             W |   | E 
            ------------ 
            SW | S | SE """

        directional_choice = [0, 1]
        next_pos = (0, 0)

        if dy == 0 and dx != 0:
            if dx > 0:
                next_pos = (1, random.choice([-1, 0, 1]))
            elif dx < 0:
                next_pos = (-1, random.choice([-1, 0, 1]))
        elif dx == 0 and dy != 0:
            if dy > 0:
                next_pos = (random.choice([-1, 0, 1]), 1)
            elif dy < 0:
                next_pos = (random.choice([-1, 0, 1]), -1)
        elif dx > 0 and dy != 0:
            if dy > 0:
                next_pos = (random.choice(directional_choice), random.choice(directional_choice))
            elif dy < 0:
                next_pos = (random.choice(directional_choice), -1*random.choice(directional_choice))
        elif dx < 0 and dy != 0:
            if dy > 0:
                next_pos = (-1*random.choice(directional_choice), random.choice(directional_choice))
            elif dy < 0:
                next_pos = (-1*random.choice(directional_choice), -1*random.choice(directional_choice))
        elif dy > 0 and dx != 0:
            if dx > 0:
                next_pos = (random.choice(directional_choice), random.choice(directional_choice))
            elif dx < 0:
                next_pos = (-1*random.choice(directional_choice), random.choice(directional_choice))
        elif dy < 0 and dx != 0:
            if dx > 0:
                next_pos = (random.choice(directional_choice), -1*random.choice(directional_choice))
            elif dx < 0:
                next_pos = (-1*random.choice(directional_choice), -1*random.choice(directional_choice))
        else:
            self.reach_target_flower = True

        self.speed = next_pos
        self.pos[0] += next_pos[0]
        self.pos[1] += next_pos[1]

    def scan_visual_radius(self, grid):
        normal_flower_list = []
        preferred_flower_list = []
        flowers_found = True
        visual_radius = self.visual_radius * self.levy

        for x in range(self.pos[0] - visual_radius, self.pos[0] + visual_radius):
            for y in range(self.pos[1] - visual_radius, self.pos[1] + visual_radius):
                if (x >= 0 and y >= 0) and (x < grid.shape[0] and y < grid.shape[1]):
                    if grid[x, y, 0].tag == 'FL':
                        flower = grid[x, y, 0]
                        if flower not in self.flower_sequence and not self.avoid_flower(flower):
                            self.levy = 1
                            if flower.color == self.next_flower_color:
                                preferred_flower_list.append(flower)
                            else:
                                normal_flower_list.append(flower)

        if len(normal_flower_list) + len(preferred_flower_list) <= 0:
            flowers_found = False
            self.levy *= 2
            # print("found no flower", self.levy)

        return flowers_found, normal_flower_list, preferred_flower_list

    def next_target_flower(self, grid):
        flowers_found = False
        normal_flower_list = []
        preferred_flower_list = []

        while not flowers_found:
            flowers_found, normal_flower_list, preferred_flower_list = self.scan_visual_radius(grid)

        p = random.random()
        p_floral = (1.0/(len(normal_flower_list) + self.floral_constancy * len(preferred_flower_list)))

        if len(normal_flower_list) > 0 and len(preferred_flower_list) > 0:
            # print("a mix of flowers nearby")
            if p <= len(normal_flower_list) * p_floral:
                self.next_flower = random.choice(normal_flower_list)
            else:
                self.next_flower = random.choice(preferred_flower_list)
        elif len(normal_flower_list) == 0 and len(preferred_flower_list) > 0:
            # print("choosing from preferred list")
            self.next_flower = random.choice(preferred_flower_list)
        elif len(normal_flower_list) > 0 and len(preferred_flower_list) == 0:
            # print("choosing from normal list")
            self.next_flower = random.choice(normal_flower_list)
        else:
            print("no flower nearby, lets do levy")

    def move_routine(self, grid):

        if not self.next_flower:
            self.next_target_flower(grid)

        if self.next_flower and not self.reach_target_flower:
            self.move()
        elif self.reach_target_flower and self.food_capacity < 80:
            self.flower_sequence.append(self.next_flower)
            self.next_flower.pheromone += 10
            self.next_flower.scent -= 10
            self.food_capacity += 10
            self.reach_target_flower = False
            self.next_target_flower(grid)
        else:
            self.task_complete = True
            print(self.reach_target_flower, self.food_capacity)

    @staticmethod
    def avoid_flower(cell):
        result = False
        if cell.tag == 'FL':
            p = cell.pheromone/(cell.pheromone + cell.scent)

            if random.random() < p:
                result = True
            else:
                result = False

        return result

