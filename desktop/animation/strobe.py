#Purpose change window color raandomly every second
import intrographics

import random
import intrographics

w=400
h=400

window=intrographics.window(w,h)

def strobe():
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)

    window.fill((r,g,b))


window.startTimer(1000,strobe)
window.open()