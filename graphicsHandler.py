from graphics import *
from time import sleep
import random
windowWidth = 1000
windowHeight = 800

ballPos = [windowWidth/2, windowHeight/2]
ballVec = [2,0.15]
ballRadius = 10
playerMargin = 50
playerDimensions = [10,100]
p1Pos = [playerMargin + playerDimensions[0]/2, windowHeight/2]
p2Pos = [windowWidth - playerMargin - playerDimensions[0]/2, windowHeight/2]

playerSpeed = 5

p1Move = [0]
p2Move = [0]

deflectionFactor = 10

gameOver = False
goalfps = 600

win = GraphWin('PONG', windowWidth, windowHeight)  # give title and dimensions
win.setBackground("black")

p1Rect = Rectangle(
    Point(p1Pos[0] - playerDimensions[0], p1Pos[1] - (playerDimensions[1] / 2)),
    Point(p1Pos[0], p1Pos[1] + (playerDimensions[1] / 2))
)
p2Rect = Rectangle(
    Point(p2Pos[0], p2Pos[1] - (playerDimensions[1] / 2)),
    Point(p2Pos[0] + playerDimensions[0], p2Pos[1] + (playerDimensions[1] / 2))
)
ball = Circle(
    Point(ballPos[0], ballPos[1]), ballRadius
)
p1Rect.setFill("white")
p2Rect.setFill("white")
ball.setFill("white")
p1Rect.draw(win)
p2Rect.draw(win)
ball.draw(win)

def playerCollision(playerPos):
    xDist = abs(ballPos[0] - playerPos[0]) - ballRadius
    yDist = abs(ballPos[1] - playerPos[1]) - ballRadius
    if(xDist > abs(ballVec[0]/2)):
        return
    if(yDist > playerDimensions[1]/2):
        return
    ballVec[0] *= -1
    deflection = yDist/playerDimensions[1]/2
    deflection *= deflectionFactor
    sign = (1, -1)[ballPos[1] - playerPos[1] < 0]
    deflection *= sign
    ballVec[1] += deflection
    

def updateBall():
    ballPos[0] += ballVec[0]
    ballPos[1] += ballVec[1]
    ball.move(ballVec[0], ballVec[1])

    if ballPos[1] - ballRadius <= 0:
        ballVec[1] *= -1 
    if ballPos[1] + ballRadius >= windowHeight:
        ballVec[1] *= -1
    playerCollision(p1Pos)
    playerCollision(p2Pos)
    if(ballPos[0] < 0 or ballPos[0] > windowWidth):
        return False
    return True

def moveP1(direction):
    if(direction > playerSpeed or direction < -playerSpeed):
        p1Move[0] = (playerSpeed, -playerSpeed)[direction < 0]
    else:
        p1Move[0] = direction

def moveP2(direction):
    if(direction > playerSpeed or direction < -playerSpeed):
        p2Move[0] = (playerSpeed, -playerSpeed)[direction < 0]
    else:
        p2Move[0] = direction

def updatePlayer1():
    if(p1Move[0] < 0 and p1Pos[1] + p1Move[0] - playerDimensions[1]/2 < 0):
        return
    if(p1Move[0] > 0 and p1Pos[1] + p1Move[0] + playerDimensions[1]/2 > windowHeight):
        return
    p1Pos[1] += p1Move[0]
    p1Rect.move(0,p1Move[0])
            
def updatePlayer2():
    if(p2Move[0] < 0 and p2Pos[1] + p2Move[0] - playerDimensions[1]/2 < 0):
        return
    if(p2Move[0] > 0 and p2Pos[1] + p2Move[0] + playerDimensions[1]/2 > windowHeight):
        return
    p2Pos[1] += p2Move[0]
    p2Rect.move(0,p2Move[0])

while updateBall():
    moveP1(ballPos[1] - p1Pos[1] - 50)
    moveP2(ballPos[1] - p2Pos[1] - 50)
    updatePlayer1()
    updatePlayer2()
    sleep(1/goalfps)
win.close()