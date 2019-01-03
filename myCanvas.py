
import tkinter as tk      # for python 2, replace with import Tkinter as tk
import random
from simMap import SimMap
width, height = (800, 800)
flower_distribution_percent = 0.5
flower_patches = int(width*height*flower_distribution_percent/1000)
# class Ball:
#
#     def __init__(self):
#         self.xpos = random.randint(0, 254)
#         self.ypos = random.randint(0, 310)
#         self.xspeed = random.randint(1, 5)
#         self.yspeed = random.randint(1, 5)


class MyCanvas(tk.Canvas):

    def __init__(self, master):
        super().__init__(master, width=width, height=height, bg="snow2", bd=0, highlightthickness=0, relief="ridge")
        self.pack()

        self.map = SimMap(int(width/10), int(height/10))
        # self.map.add_flowers_patches(20, 20, 'blue', 5)
        # self.map.add_flowers_patches(60, 60, 'red', 5)
        # self.map.add_flowers_patches(20, 60, 'green', 5)
        # self.map.add_flowers_patches(60, 20, 'red', 5)
        self.map.add_flowers_row(10, 10, 'red', 20, 'h')
        self.map.add_flowers_row(12, 10, 'blue', 20, 'v')
        self.map.add_flowers_row(50, 12, 'red', 20, 'h')
        self.map.add_flowers_row(10, 50, 'green', 20, 'v')
        self.fls = []
        for flower in self.map.flowers:
            self.fls.append(self.create_oval(flower.pos[0]*10 - 10, flower.pos[1]*10 - 10,
                                             flower.pos[0]*10 + 10, flower.pos[1]*10 + 10,
                                             fill=flower.color))

        self.map.add_bee_colonies(self.map.center[0], self.map.center[1], 10)
        self.bs = []
        for bee in self.map.bees:
            self.bs.append(self.create_oval(bee.pos[0]*10 - 5, bee.pos[1]*10 - 5,
                                            bee.pos[0]*10 + 5, bee.pos[1]*10 + 5,
                                            fill="yellow"))
        self.run()

    def run(self):
        task_complete = False
        for bee in self.map.bees:
            bee.move_routine(self.map.grid)

        for b, bee in zip(self.bs, self.map.bees):
            task_complete = True
            self.move(b, bee.speed[0]*10, bee.speed[1]*10)
            task_complete *= int(bee.task_complete)

        if not bool(task_complete):
            self.after(50, self.run)
        else:
            self.quit()
