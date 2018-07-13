# Purpose; Move an ovalv around window
#Purpose: Move rect smoothly by small random amts

import random
import intrographics

w=400
h=400
diameter=30

window=intrographics.window(w,h)

oval=window.addOval(0,0,diameter,diameter)
oval.paint("blue")


 #Function moves ball in curent direction and bounces off
def bounce():
    
    
    oval.move(oval.vx,oval.vy)
    if oval.bottom>=h or oval.top<=0:
        oval.vy=-oval.vy
        
    if oval.right>=w or oval.left<=0:
        oval.vx=-oval.vx
        
        
oval.vx=3
oval.vy=5

        


window.startTimer(30,bounce)
window.open()

