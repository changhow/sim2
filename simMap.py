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
floral_constancy_multiplier = 9


class SimMap:

    def __init__(self, width, height):
        self.width = width - 1
        self.height = height - 1
        self.center = (width/2, height/2)
        self.grid = numpy.empty(shape=(width, height, 2), dtype=object)
        self.grid[:, :, 0] = Grass()
        self.grid[:, :, 1] = Air()
        self.flowers = []
        self.multiplier = 1
        self.bees = []
        self.quitt = False

    def add_flowers(self, x, y, color='red', fa='N'):
        flower = Flowers(x, y, color, fa)
        self.grid[x, y, 0] = flower
        self.flowers.append(flower)

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

    def bee_scan_visual_radius(self, bee):
        normal_flower_list = []
        preferred_flower_list = []
        flowers_found = True
        for x in range(bee.pos[0] - bee_visual_radius * self.multiplier,
                       bee.pos[0] + bee_visual_radius * self.multiplier + 1):
            for y in range(bee.pos[1] - bee_visual_radius * self.multiplier,
                           bee.pos[1] + bee_visual_radius * self.multiplier + 1):
                if self.grid[x, y, 0].tag == 'FL' and self.grid[x, y, 1].tag != 'PH':
                    if self.grid[x, y, 0] not in bee.flower_list:
                        self.multiplier = 1
                        if self.grid[x, y, 0].color == bee.target_flower_color:
                            preferred_flower_list.append(self.grid[x, y, 0])
                        else:
                            normal_flower_list.append(self.grid[x, y, 0])

        if len(normal_flower_list) + len(preferred_flower_list) <= 0:
            self.multiplier *= 2
            flowers_found = False

        return flowers_found, normal_flower_list, preferred_flower_list

    def bee_target_next_flowers(self, bee):
        # check number of flowers in surrounding radius
        flowers_found = False
        while flowers_found == False:
            flowers_found, normal_flower_list, preferred_flower_list = self.bee_scan_visual_radius(bee)


        # calc probability
        p = random.random()
        p_floral = (1.0/(len(normal_flower_list) + floral_constancy_multiplier * len(preferred_flower_list)))

        if len(normal_flower_list) > 0 and len(preferred_flower_list) > 0:
            # print("a mix of flowers nearby")
            if p <= len(normal_flower_list) * p_floral:
                bee.next_target_flower = random.choice(normal_flower_list)
            else:
                bee.next_target_flower = random.choice(preferred_flower_list)
        elif len(normal_flower_list) == 0 and len(preferred_flower_list) > 0:
            # print("choosing from preferred list")
            bee.next_target_flower = random.choice(preferred_flower_list)
        elif len(normal_flower_list) > 0 and len(preferred_flower_list) == 0:
            # print("choosing from normal list")
            bee.next_target_flower = random.choice(normal_flower_list)
        else:
            print("no flower nearby, lets do levy")

        #
        # while bee.next_target_flower in bee.flower_list:
        #     p = random.random()
        #     if len(normal_flower_list) > 0 and len(preferred_flower_list) > 0:
        #         # print("a mix of flowers nearby")
        #         if p <= len(normal_flower_list) * p_floral:
        #             bee.next_target_flower = random.choice(normal_flower_list)
        #         else:
        #             bee.next_target_flower = random.choice(preferred_flower_list)
        #     elif len(normal_flower_list) == 0 and len(preferred_flower_list) > 0:
        #         # print("choosing from preferred list")
        #         bee.next_target_flower = random.choice(preferred_flower_list)
        #     elif len(normal_flower_list) > 0 and len(preferred_flower_list) == 0:
        #         # print("choosing from normal list")
        #         bee.next_target_flower = random.choice(normal_flower_list)
        #     else:
        #         print("no flower nearby, lets do levy")
            # print("NOOOOO")
            # self.bee_target_next_flowers(bee)


    def bee_move_routine(self):
        task_complete = True

        # for bee in self.bees:
        #     self.bee_target_next_flowers(bee)
        """
        i = 0
        while self.avoid_flower(bee.next_target_flower.pos[0], bee.next_target_flower.pos[1]):
            i += 1
            # print("choose new flower")
            self.bee_target_next_flowers(bee)
            if i > 5:
                bee.reach_target_flower = True
                break
        """
        for bee in self.bees:
            task_complete *= int(bee.reach_target_flower)
        # print("Current pos", bee.pos, "\ttarget pos", bee.next_target_flower.pos, "color", bee.next_target_flower.color)
        # print("task = ", task_complete == True, task_complete)

        if task_complete:
            self.quitt = True
            print("Done")
            j = 0
            for bee in self.bees:
                j += 1
                for i in range(len(bee.flower_list)):
                    print(j, bee.flower_list[i].pos, bee.flower_list[i].color)

        else:
            i = 0
            for bee in self.bees:
                print("Current pos", bee.pos, "\ttarget pos", bee.next_target_flower.pos, "color", bee.next_target_flower.color)
                i += 1
                if bee.next_target_flower != None and bee.reach_target_flower == False:
                    bee.move()

                if bee.reach_target_flower == True and bee.food_capacity < 75:
                    bee.reach_target_flower = False
                    bee.flower_list.append(bee.next_target_flower)
                    bee.food_capacity += 5
                    bee.next_target_flower.pheromone += 25
                    bee.next_target_flower.scent -= 25
                    self.bee_target_next_flowers(bee)
                    print(i, bee.food_capacity, bee.reach_target_flower, "choosing new flower")

        # else:

                    # print(self.grid[bee.flower_list[i].pos[0],bee.flower_list[i].pos[1], 0].scent)
            # print(self.grid[bee.next_target_flower.pos[0], bee.next_target_flower.pos[1], 0].pheromone)



    def avoid_flower(self, x, y):
        result = False
        if self.grid[x, y, 0].tag == 'FL':
            p = self.grid[x, y, 0].pheromone / (self.grid[x, y, 0].pheromone + self.grid[x, y, 0].scent)

            if random.random() < p:
                result = True
            else:
                result = False

        return result
