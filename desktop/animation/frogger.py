import intrographics

window = intrographics.window(600,700)

player = window.addOval(450,670,20,20)
player.group = "player"
player.vx = 0

start = window.addRectangle(0,640,600,700)
start.group = "screen"

middle = window.addRectangle(0,300,600,70)
middle.group = "screen"

home = window.addRectangle(0,0,600,60)
home.group = "screen"


# Platforms
platform1 = window.addRectangle(0,260,60,30)
platform1.group = "platforms"
platform1.vx = 2

platform2 = window.addRectangle(0,180,60,30)
platform2.group = "platforms"
platform2.vx = 4

platform3 = window.addRectangle(0,100,60,30)
platform3.group = "platforms"
platform3.vx = 6


# Obstacles
car1 = window.addRectangle(0,600,60,30)
car1.group = "obstacles"
car1.vx=3

car2 = window.addRectangle(0,540,60,30)
car2.group = "obstacles"
car2.vx=4

car3 = window.addRectangle(0,480,60,30)
car3.group = "obstacles"
car3.vx=5

car4 = window.addRectangle(0,420,60,30)
car4.group = "obstacles"
car4.vx=6


# This function moves the obstacles
def moveObstacle():
    for obstacle in window:
        if obstacle.group == "obstacles":
            obstacle.move(obstacle.vx, 0)
            if obstacle.left <= 0 or obstacle.right >= 600:
                obstacle.vx = -obstacle.vx
    for shape in window.touching(player):
        if shape.group == "obstacles":
            window.close()

# This function moves the platforms
def movePlatform():
    for platform in window:
        if platform.group == "platforms":
            platform.move(platform.vx, 0)
            if platform.left <= 0 or platform.right >= 600:
                platform.vx = -platform.vx
    for shape in window.touching(player):
        if shape.group == "platforms":
            player.move(player.vx, 0)
            player.vx = shape.vx
            if player.left <= 0 or player.right >= 600:
                window.close()

# This function moves the player
def navigate(key):
    if key == "Left" and player.left > 0:
        player.move(-player.width, 0)
    elif key == "Right" and player.right < 600:
        player.move(player.width, 0)
    elif key == "Up" and player.top > 0:
        player.move(0, -player.height)
    elif key == "Down" and player.bottom < 700:
        player.move(0, player.height)

window.onKey(navigate)
window.startTimer(30,moveObstacle)
window.startTimer(30,movePlatform)
window.open()