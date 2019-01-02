
import tkinter as tk      # for python 2, replace with import Tkinter as tk
import random
from simMap import SimMap
width, height = (800, 800)
flower_distribution_percent = 5
flower_patches = int(width*height*flower_distribution_percent/1000)
class Ball:

    def __init__(self):
        self.xpos = random.randint(0, 254)
        self.ypos = random.randint(0, 310)
        self.xspeed = random.randint(1, 5)
        self.yspeed = random.randint(1, 5)


class MyCanvas(tk.Canvas):

    def __init__(self, master):

        super().__init__(master, width=width, height=height, bg="snow2", bd=0, highlightthickness=0, relief="ridge")
        self.pack()

        self.map = SimMap(int(width/10), int(height))
        self.map.random_distribute_flowers_patches(flower_patches)
        self.fls = []
        for flower in self.map.flowers:
            self.fls.append(self.create_oval(flower.pos[0]*10 - 10, flower.pos[1]*10 - 10,
                                             flower.pos[0]*10 + 10, flower.pos[1]*10 + 10,
                                             fill=flower.color))
        self.map.add_bees(20, 30)
        self.bs = []
        self.bs.append(self.create_oval(self.map.bees[0].pos[0]*10 - 5, self.map.bees[0].pos[1]*10 - 5,
                                        self.map.bees[0].pos[0]*10 + 5, self.map.bees[0].pos[1]*10 + 5,
                                        fill="yellow"))

        self.map.bee_target_next_flowers(self.map.bees[0])
        # self.balls = []   # keeps track of Ball objects
        # self.bs = []      # keeps track of Ball objects representation on the Canvas
        # for _ in range(1):
        #     ball = Ball()
        #     self.balls.append(ball)
        #     self.bs.append(self.create_oval(ball.xpos - 10, ball.ypos - 10, ball.xpos + 10, ball.ypos + 10, fill="saddle brown"))
        self.run()


    def run(self):
        self.map.bee_move_routine()

        # print(len(self.bs), len(self.map.bees))

        for b, bee in zip(self.bs, self.map.bees):
            # print(b, bee)
            self.move(b, bee.speed[0]*10, bee.speed[1]*10)

        if self.map.quitt ==  False:
            # print("quit", self.map.quit)
            self.after(100, self.run)
        else:
            self.quit()


        # for b, ball in zip(self.bs, self.balls):
        #     print(b, ball)
        #     self.move(b, ball.xspeed, ball.yspeed)
        #     pos = self.coords(b)
        #     print(pos, ball.xpos, ball.ypos, ball.xspeed, ball.yspeed)
        #     if pos[3] >= 310 or pos[1] <= 0:
        #         ball.yspeed = - ball.yspeed
        #     if pos[2] >= 254 or pos[0] <= 0:
        #         ball.xspeed = - ball.xspeed
        # self.after(1000, self.run)


if __name__ == '__main__':

    shop_window = tk.Tk()
    shop_window.geometry("254x310")
    c = MyCanvas(shop_window)

    shop_window.mainloop()