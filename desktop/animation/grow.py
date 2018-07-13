#Grow an oval smoothly
import random
import intrographics

w=400
h=400
diameter=30

window=intrographics.window(w,h)

oval=window.addOval(0,0,1,1)
oval.paint("blue")


def grow():
    oval.resize(oval.width+1, oval.height+1)
    if oval.width==w or oval.height==h:
        window.stopTimer(grow)

window.startTimer(30,grow)
window.open()
