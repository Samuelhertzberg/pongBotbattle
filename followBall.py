# This function is called for you to decide what action to take with your player.
# Return should be a integer between -maxSpeed and maxSpeed, however if the return is larger/smaller the value will be set to the closest limit.
def move(ballPos, position, opponentPosition, maxSpeed):
    return ballPos[1] - position[1]
