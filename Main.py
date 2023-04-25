import pygame as pg
from pygame.locals import *
import random as rd
import sys
import Logic as lg
import datetime as Dt
import math
#constants of the game

WindowsWidth = 900
WindowsHeight = 600
Bg_Color = (0,0,0)
Text_Color = (255,255,255)
Fps = 1000
Ball_Rad = 10
Ball_Color = (255,255,255)
Ball_Power_Color = (255,255,255)
Ball_Power_Rad = 17
Max_Delta_x = 6
Max_Delta_y = 6
RP_Delta_x = 0
RP_Delta_y = 0
LP_Delta_x = 0
LP_Delta_y = 0
END_GAME = False
EXPLOSION = False
SINGLE_PLAYER = True
ANIMATION = False
STATE_GAME = False,False
LP_Points = 0
RP_Points = 0
SPIRAL = lg.MakeSpiral(WindowsWidth,WindowsHeight)
Power_Ball_Life = 5
Time_freeze = 10
Time_Explosion = 5
DirPlayList = lg.DirectoryWorker.getcwd() + '\\src\\PlayList'
PLAYLIST = lg.GetPlayList(DirPlayList)
Explosion_Sound = lg.DirectoryWorker.getcwd() + '\\src\\Efects\\LightningBolt_S08WT.22 [Angel Roid & FX_Arts].wav'
#items for the players
LP = {'center_x':10,'center_y':300,'x_width':20,'y_width':100}
RP = {'center_x':890,'center_y':300,'x_width':20,'y_width':100}


#item of the ball
BallItem = {'center_x':450,'center_y':300,'rad':Ball_Rad,'color':Ball_Color,'delta_x':rd.random()*Max_Delta_x + 0.5,'delta_y':rd.random()*Max_Delta_y}

balls = [BallItem]

def FinishGame():
    pg.quit()
    sys.exit()
    pass

def DrawText(text,font,screen,color,x,y):
    text_obj = font.render(text,1,color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = x,y
    screen.blit(text_obj,text_rect)
    pass

def LoadNextMusic(playlist,mixer):
    music = playlist.pop(0)
    mixer.queue(music)
    playlist.append(music)
    pass

def InitPlayList(playlist,mixer):
    music = playlist.pop(0)
    mixer.load(music)
    playlist.append(music)
    following = playlist.pop(0)
    mixer.queue(following)
    playlist.append(following)
    mixer.set_endevent(pg.USEREVENT)
    pass

def InitPageOfGame(screen,width,height,spiral):
    single_player = False
    close = False
    dt_global = Dt.datetime.now()
    color_to_change = 0
    delta_color = 1
    color = 0,0,0
    while True:
        dt_local = Dt.datetime.now()
        if abs(dt_global.second - dt_local.second) > 10:
            color_to_change = rd.randint(0,2)
            dt_global = dt_local
            pass
        if color[color_to_change] == 0:
            delta_color = 1
            pass
        elif color[color_to_change] == 255:
            delta_color = -1
            pass
        if color_to_change == 0:
            color = color[0] + delta_color,color[1],color[2]
            pass
        elif color_to_change == 1:
            color = color[0],color[1] + delta_color,color[2]
            pass
        else:
            color = color[0],color[1],color[2] + delta_color
            pass
        screen.fill(color)
        spiral = lg.RotatePoints(spiral,WindowsWidth // 2,WindowsHeight // 2,0.02)
        pg.draw.lines(screen,(255 - color[0],255 - color[1],255 - color[2]),0,spiral,40)
        for event in pg.event.get():
            if event.type == QUIT:
                FinishGame()
                pass
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    single_player = True
                    pass
                if event.key == K_DOWN:
                    single_player = False
                    pass
                if event.key == K_SPACE:
                    close = True
                    break
                pass
            pass

        if close:
            break

        if single_player:
            pg.draw.rect(screen,(255,255,255),(width//3,height//3,300,50))
            pg.draw.circle(screen,(255,255,255),(width//3 - 30,height//3 + 25),20,0)
            DrawText('Single Player',font,screen,(51,51,51),width//3 + 50,height//3 + 10)
            pg.draw.rect(screen,(51,51,51),(width//3,2*(height//3),300,50))
            DrawText('MultiPlayer',font,screen,(255,255,255),width//3 + 50,2*(height//3) +10)
            pass
        else:
            pg.draw.rect(screen,(51,51,51),(width//3,height//3,300,50))
            DrawText('Single Player',font,screen,(255,255,255),width//3 + 50,height//3 + 10)
            pg.draw.rect(screen,(255,255,255),(width//3,2*(height//3),300,50))
            pg.draw.circle(screen,(255,255,255),(width//3 -30,2*(height//3) + 25),20,0)
            DrawText('MultiPlayer',font,screen,(51,51,51),width//3 + 50,2*(height//3) + 10)
            pass
        pg.display.update()
        pass
    return single_player

def SpiralAnimation(spiral,screen,x_center,y_center):
    spiral = lg.RotatePoints(spiral, x_center, y_center, 0.02)
    pg.draw.lines(screen,Text_Color,0,spiral,40)
    return spiral

#we init the game_engine
pg.init()
MainClock = pg.time.Clock()
SCREEN = pg.display.set_mode((WindowsWidth,WindowsHeight))
pg.display.set_caption('Pin Pon')
pg.mouse.set_visible(False)
#load the font of the text
font = pg.font.SysFont(None,48)
Power_Balls_Font = pg.font.SysFont(None,20)
#load the background_music and play it
PLAYLIST = lg.MakePlayList(PLAYLIST,DirPlayList)

init_music = pg.mixer.Sound(PLAYLIST[len(PLAYLIST) - 1])

InitPlayList(PLAYLIST,pg.mixer.music)


init_music.play(-1)
SINGLE_PLAYER = InitPageOfGame(SCREEN,WindowsWidth,WindowsHeight,SPIRAL)
init_music.stop()

DTM = Dt.datetime.now()
DTA = Dt.datetime.now()
pg.mixer.music.play()
explosion_sound = pg.mixer.Sound(Explosion_Sound)
explosion_time = None


#main loop of the game
while True:
    #we clear the window


    SCREEN.fill(Bg_Color)
    pg.draw.line(SCREEN,Text_Color,(450,0),(450,600),10)

    #draw the puntuations
    DrawText(str(LP_Points), font, SCREEN, Text_Color, 300, 50)
    DrawText(str(RP_Points),font,SCREEN,Text_Color,600,50)

    dt = Dt.datetime.now()

    if ANIMATION:
        SPIRAL = SpiralAnimation(SPIRAL,SCREEN,WindowsWidth // 2, WindowsHeight // 2)
        if abs(dt.second - DTA.second) > 20:
            ANIMATION = False
            DTA = dt
            pass
        pass
    else:
        if abs(dt.minute - DTA.minute) == 1:
            ANIMATION = True
            DTA = dt
            pass
        pass

    if explosion_time != None and abs(dt.second - explosion_time.second) > Time_Explosion:
        explosion_time = None
        EXPLOSION = False
        pass

    power_ball = lg.RaisePowerBall(DTM.second, dt.second,Time_freeze, rd,Ball_Power_Rad, Ball_Power_Color,Power_Ball_Life,WindowsWidth,WindowsHeight)
    if power_ball != None:
        balls.append(power_ball)
        DTM = dt
        pass

    #move and draw the balls
    for ball in balls:
        lg.MoveBall((ball))
        pg.draw.circle(SCREEN,ball['color'],(ball['center_x'],ball['center_y']),ball['rad'],0)
        if EXPLOSION:
            ball['color'] = Bg_Color
            pass
        #change the color of the power ball
        if ball['rad'] == 17:
            Ball_Power_Color = rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)
            ball['color'] = Ball_Power_Color
            DrawText(str(ball['life']),Power_Balls_Font,SCREEN,(0,0,0),ball['center_x'] - 5,ball['center_y'] - 5)
            lg.CollidePowerBall(ball, balls)
            pass

        #change the movment of the balls
        lg.BallCollideWalls(ball, 0, WindowsHeight,0,WindowsWidth)
        
        if lg.BallCollidePlayers(ball, LP) or lg.BallCollidePlayers(ball, RP):
            if ball['delta_x'] < 0:
                ball['delta_x'] = rd.randint(1,Max_Delta_y)
                pass
            else:
                ball['delta_x'] = -1*rd.randint(1,Max_Delta_y)
                pass
            if ball['delta_y'] < 0:
                ball['delta_y'] = -1*rd.randint(0,Max_Delta_y)
                pass
            else:
                ball['delta_y'] = rd.randint(0,Max_Delta_y)
                pass
            Ball_Color = rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)
            Text_Color = Ball_Color
            if not EXPLOSION:
                ball['color'] = Ball_Color
                pass
            if ball['rad'] == 17:
                ball['life'] -= 1
                if ball['life'] == 0:
                    EXPLOSION = True
                    pass
                pass
            pass

        STATE_GAME = lg.EndGame(ball, 0, WindowsWidth)
        if STATE_GAME[0] or STATE_GAME[1]:
            END_GAME = True
            break
        pass

    data = lg.KillPowerBalls(balls)
    balls = data[0]

    if data[1]:
        EXPLOSION = True
        explosion_time = Dt.datetime.now()
        explosion_sound.play()
        pass
    
    if EXPLOSION:
        Text_Color = rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)
        Bg_Color = 255 - Text_Color[0],255 - Text_Color[1],255 - Text_Color[2]
        pass

    
    if END_GAME:
        lg.RestartBalls(balls, WindowsWidth, WindowsHeight)
        if STATE_GAME[0]:
            balls[0]['delta_x'] = -1*rd.random()*Max_Delta_x - 0.5
            RP_Points += 1
            pass
        else:
            balls[0]['delta_x'] = rd.random()*Max_Delta_x + 0.5
            LP_Points += 1
            pass
        balls[0]['delta_y'] = rd.random()*Max_Delta_y*rd.choice([1,-1])
        STATE_GAME = False,False
        END_GAME = False
        pass

    #check for all posible events in the game
    for event in pg.event.get():
        if event.type == QUIT:
            FinishGame()
            pass
        if event.type == KEYDOWN:
            if event.key == K_UP:
                RP_Delta_y = -5
                pass
            elif event.key == K_DOWN:
                RP_Delta_y = 5
                pass
            if event.key == K_w and not SINGLE_PLAYER:
                LP_Delta_y = -5
                pass
            elif event.key == K_s and not SINGLE_PLAYER:
                LP_Delta_y = 5
                pass
            pass
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                RP_Delta_y = 0
                pass
            if event.key == K_s or event.key == K_w:
                LP_Delta_y = 0
                pass
            pass
        if event.type == pg.USEREVENT:
            LoadNextMusic(PLAYLIST, pg.mixer.music)
            pass
        pass

    info = lg.AutomaticMovePlayer(LP,BallItem)
    if SINGLE_PLAYER and BallItem['delta_x'] < 0 and info[0]:
        if info[1] > LP["center_y"] + 2:
            LP_Delta_y = 5
            pass
        elif info[1] < LP['center_y'] - 2:
            LP_Delta_y = -5
            pass
        else:
            LP_Delta_y = 0
            pass
        pass
    if not info[0]:
        LP_Delta_y = 0
        pass

    #movemos los jugadores
    if RP['center_y'] > 0 and RP['center_y'] < WindowsHeight:
        lg.MovePlayer(RP,RP_Delta_x,RP_Delta_y)
        pass
    else:
        if RP['center_y'] <= 0 and RP_Delta_y > 0:
            lg.MovePlayer(RP,RP_Delta_x,RP_Delta_y)
            pass
        elif RP['center_y'] >= WindowsHeight and RP_Delta_y < 0:
            lg.MovePlayer(RP,RP_Delta_x,RP_Delta_y)
            pass
        pass

    if LP['center_y'] > 0 and LP['center_y'] < WindowsHeight:
        lg.MovePlayer(LP,LP_Delta_x,LP_Delta_y)
        pass
    else:
        if LP['center_y'] <= 0 and LP_Delta_y > 0:
            lg.MovePlayer(LP,LP_Delta_x,LP_Delta_y)
            pass
        elif LP['center_y'] >= WindowsHeight and LP_Delta_y < 0:
            lg.MovePlayer(LP,LP_Delta_x,LP_Delta_y)
            pass

    LPRect = lg.GetRect(LP)
    RPRect = lg.GetRect(RP)
    #draw the items of the players
    pg.draw.rect(SCREEN,Text_Color,(LPRect[0],LPRect[1],LP['x_width'],LP['y_width']))
    pg.draw.rect(SCREEN,Text_Color,(RPRect[0],RPRect[1],RP['x_width'],RP['y_width']))
    
    #update the window
    pg.display.update()
    MainClock.tick(Fps)
    pass