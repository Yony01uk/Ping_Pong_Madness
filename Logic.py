import os as DirectoryWorker
import math

#get the params for the rectangle of one player
def GetRect(player):
    return player['center_x'] - player['x_width'] / 2,player['center_y'] - player['y_width'] / 2

#return true if there is a collision betwen one ball and one player
def BallCollidePlayers(ball,player):
    if abs(ball['center_x'] - player['center_x']) < ball['rad'] + player['x_width'] / 2 and abs(ball['center_y'] - player['center_y']) < ball['rad'] + player['y_width'] / 2:
        return True
    return False

#return true if there is a collision betwen one ball and the walls
def BallCollideWalls(ball,top,bottom,left,right):
    if abs(ball['center_y'] - top) < ball['rad'] or abs(ball['center_y'] - bottom) < ball['rad']:
        ball['delta_y'] *= -1
        pass
    if ball['rad'] == 17:
        if abs(ball['center_x'] - left) < ball['rad'] or abs(ball['center_x'] - right) < ball['rad']:
            ball['delta_x'] *= -1
            pass
        pass
    pass

def CollidePowerBall(power_ball,balls):
    for ball in balls:
        if not ball == power_ball:
            if abs(power_ball['center_x'] - ball['center_x']) < power_ball['rad'] + ball['rad'] and abs(power_ball['center_y'] - ball['center_y']) < power_ball['rad'] + ball['rad']:
                ball["delta_x"] *= -1
                power_ball['delta_x'] *= -1
                ball['delta_y'] *= -1
                power_ball['delta_y'] *= -1
                power_ball['life'] -= 1
                pass
            pass
        pass
    pass

def KillPowerBalls(balls):
    explosion = False
    result = []
    for ball in balls:
        if ball['rad'] == 17:
            if ball['life'] > 0:
                result.append(ball)
                pass
            else:
                explosion = True
            pass
        else:
            result.append(ball)
            pass
        pass
    return result,explosion

#return a 2-tuple with true in the side where the ball gone
def EndGame(ball,left,right):
    if ball['rad'] != 17:
        if ball['center_x'] < left:
            return True,False
        elif ball['center_x'] > right:
            return False,True
        pass
    return False,False

def RaisePowerBall(t0,t1,delta_t,rd,ball_rad,ball_color,life,width,height):
    if abs(t0 -t1) > delta_t:
        return {'center_x':rd.randint(0,width),'center_y':rd.randint(0,height),'rad':ball_rad,'color':ball_color,'delta_x':rd.random(),'delta_y':rd.random(),'life':life}
    return None

def RestartBalls(balls,width,height):
    while len(balls) > 1:
        balls.pop()
        pass
    balls[0]['center_x'] = width / 2
    balls[0]['center_y'] = height / 2
    pass

#move one ball
def MoveBall(ball):
    ball['center_x'] += ball['delta_x']
    ball['center_y'] += ball['delta_y']
    pass

def GetPlayList(dir):
    return DirectoryWorker.listdir(dir)

def MakePlayList(playlist,dir):
    result = []
    for music in playlist:
        result.append(dir + '\\' + music)
        pass
    return result

#move one player
def MovePlayer(player,delta_x,delta_y):
    player['center_x'] += delta_x
    player['center_y'] += delta_y
    pass

def AutomaticMovePlayer(player,ball):
    if player['center_y'] == ball['center_y'] - (ball['delta_y'] / ball['delta_x']) * ball['center_x']:
        return False,ball['center_y'] - (ball['delta_y'] / ball['delta_x']) * ball['center_x']
    return True,ball['center_y'] - (ball['delta_y'] / ball['delta_x']) * ball['center_x']

def MakeSpiral(width,height):
    angle = 0.0
    distance = 5
    sections =[(width//2,height//2)]
    while len(sections) < 500:
        x1 = distance * math.cos(angle) + width // 2
        y1 = distance * math.sin(angle) + height // 2
        sections.append((x1,y1))
        angle += 0.1
        distance += 1.5
        pass
    return sections

def RotatePoints(points,x_center,y_center,angle):
    result = []
    for point in points:
        x = (point[0] - x_center) * math.cos(angle) + (point[1] - y_center) * math.sin(angle)
        y = (point[1] - y_center) * math.cos(angle) - (point[0] - x_center) * math.sin(angle)
        result.append((x + x_center,y + y_center))
        pass
    return result