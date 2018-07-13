#Purpose: Move rect smoothly by small random amts

import random
import intrographics

w=400
h=400
length=10

window=intrographics.window(w,h)

rectangle=window.addRectangle(w/2,h/2,10,10)
rectangle.paint("black")


 #Function moves rect
def migrate():
    dx=random.choice([-2,2])
    dy=random.choice([-2,2])
    
    rectangle.move(dx,dy)
   


window.startTimer(30,migrate)
window.open()

