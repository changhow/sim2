import time
from simMap import SimMap
import tkinter as tk
from myCanvas import MyCanvas

animation = tk.Tk()
c = MyCanvas(animation)
animation.mainloop()



# width, height = (100, 100)
# canvas = Canvas(animation, width=width, height=height)
# canvas.pack()
#
# # canvas.update()
#
# simMap = SimMap(width, height)
# a = width * height / 2
# simMap.random_distribute_flowers_patches(int(a))
# simMap.add_bee_colonies(30, 60, 10)
# simMap.bee_move_routine()
# time.sleep(1)
