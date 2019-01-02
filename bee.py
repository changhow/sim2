from pheromone import Pheromone
import random


class Bee:

    def __init__(self, x, y):
        self.pos = [x, y]
        self.flower_sequence = []
        self.tag = 'BEE'
        self.flower_list = []
        self.food_capacity = 0
        self.target_flower_color = 'red'
        self.next_target_flower = None
        self.pheromone = Pheromone()
        self.reach_target_flower = False
        self.speed = (0, 0)

    def compute_target_flower_distance(self):
        dx = self.next_target_flower.pos[0] - self.pos[0]
        dy = self.next_target_flower.pos[1] - self.pos[1]

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


