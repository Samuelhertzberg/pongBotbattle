from graphics import *
from time import sleep
import random
import importlib 

p1Bot = importlib.import_module(sys.argv[1])
p2Bot = importlib.import_module(sys.argv[2])

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
    p1MoveRaw = p2Bot.move(ballPos, p1Pos, p2Pos, playerSpeed)
    p1Move[0] = makeLegal(p1MoveRaw, p2Pos)
    
def moveP2(direction):
    p2MoveRaw = p2Bot.move(ballPos, p2Pos, p1Pos, playerSpeed)
    p2Move[0] = makeLegal(p2MoveRaw, p2Pos)


def makeLegal(move, playerPos):
    if(move == None):
        return 0
    if(move < 0 and playerPos[1] + move - playerDimensions[1]/2 < 0):
        return 0
    if(move > 0 and playerPos[1] + move + playerDimensions[1]/2 > windowHeight):
        return 0
    if(move > playerSpeed):
        return playerSpeed
    if(move < -playerSpeed):
        return -playerSpeed
    return move


def updatePlayer1():
    p1Pos[1] += p1Move[0]
    p1Rect.move(0,p1Move[0])
            
def updatePlayer2():
    p2Pos[1] += p2Move[0]
    p2Rect.move(0,p2Move[0])

while updateBall():
    moveP1(ballPos[1] - p1Pos[1] - 50)
    moveP2(ballPos[1] - p2Pos[1] - 50)
    updatePlayer1()
    updatePlayer2()
    sleep(1/goalfps)
win.close()
