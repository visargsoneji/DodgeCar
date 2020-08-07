import pygame
import time
import random
from pygame import mixer

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (150,0,0)
green = (0, 150, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

car_height = 140
car_width = 60

pause = False

carIMG = pygame.image.load('final_car.png')
game_icon = pygame.transform.scale(carIMG, (32,32))
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dodge Car')
clock = pygame.time.Clock()


carImg = pygame.transform.scale(carIMG, (car_width,car_height))


pygame.display.set_icon(game_icon)
carImg_r = pygame.transform.rotate(carImg, 180)

play_width = 100
playImg = pygame.image.load('play_white.png')
exitImg = pygame.image.load('close.png')
pauseImg = pygame.image.load('pause.png')
resetImg = pygame.image.load('reset.png')

mixer.music.load("background.wav")
mixer.music.play(-1)

def car(x,y):
    gameDisplay.blit(carImg,(int(x),int(y)))

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score : "+str(count*10), True, white)
    gameDisplay.blit(text,(0,0))

def text_objects(text, font, color = white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text, score, color = black):
    largeText = pygame.font.Font('freesansbold.ttf',45)
    TextSurf, TextRect = text_objects(str(text) + str(score*10), largeText, color)
    TextRect.center = ((display_width//2),(display_height//4))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

def crash(score):
    explosionSound = mixer.Sound("explosion.wav")
    explosionSound.play()
    mixer.music.pause()
    message_display('You Crashed | Score = ', score, bright_red)
    time.sleep(1)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    mixer.music.unpause()
                    game_loop()
        gameDisplay.fill(black)

        button(200,250,100,100,black,black,resetImg,game_loop)
        button(500,250,100,100,black,black,exitImg,quit)

        pygame.display.update()


def object_rect(x, y, color, length, breadth):
    pygame.draw.rect(gameDisplay, color, [x, y, length, breadth])

def button(x,y,w,h,ic,ac,Img,action=None,f_size=20,msg = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #click is tuple of three values : (left_click,middle_click,right_click)
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        Img_scaled = pygame.transform.scale(Img, (w,w))
        gameDisplay.blit(Img_scaled, (int(x),int(y)))
        if click[0] == 1 and action!= None:
            action()
    else:
        #pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
        Img_scaled = pygame.transform.scale(Img, (w-10,w-10))
        gameDisplay.blit(Img_scaled, (int(x+2),int(y+2)))

    smallText = pygame.font.Font("freesansbold.ttf",f_size)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( int(x+(w/2)), int(y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)



def paused():
    global pause
    mixer.music.pause()
    gameDisplay.fill(black)
    largeText = pygame.font.SysFont(None,90)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = (int(display_width/2),int(display_height/4))

    #pause = True
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    mixer.music.unpause()
                    game_loop()
                if event.key == pygame.K_p:
                    unpause()

        gameDisplay.fill(black)
        gameDisplay.blit(TextSurf, TextRect)
        button(350,250,100,100,black,black,playImg,unpause)
        button(150,250,100,100,black,black,resetImg,game_loop)
        button(550,250,100,100,black,black,exitImg,quit)

        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pause = False
    mixer.music.unpause()

def game_intro():

    y1 = display_height + 50
    y2 = - car_height - 50
    intro = True
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        gameDisplay.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = text_objects("Dodge Car", largeText, white)
        TextRect.center = (int(display_width//2),int(display_height//2.5 - 20))

        owner = pygame.font.SysFont(None,20)
        TextSurf1, TextRect1 = text_objects("© Visarg Soneji",owner)
        TextRect1.center = (int(display_width//2), int(display_height-20))

        gameDisplay.blit(TextSurf1, TextRect1)
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(carImg, (650, y1))
        gameDisplay.blit(carImg_r, (95, y2))
        y1 -= 5
        y2 += 5
        if y1 < -car_height - 50: y1 = display_height + 50
        if y2 > display_height + 50: y2 = - car_height - 50


        #gameDisplay.blit(resetImg, (0,0))

        mouse = pygame.mouse.get_pos()

        button(display_width/2 - 65,display_height/1.8 - 10,130,120,black,black,playImg,game_loop,35)
        #button("Exit",550,450,100,50,red,bright_red,quit,35)

        pygame.display.update()
        clock.tick(60)


def game_loop():
    global pause
    pause = False

    x = (display_width/2)-(car_width/2)
    y = (display_height - car_height - 50)

    x_change = 0
    y_change = 0
    count = 0

    thing_speed = 5
    thing_width = []
    thing_height = 50
    thing_startx = []
    thing_starty = []
    thing_count = 1
    thing_width.append(random.randrange(50,75))
    thing_startx.append(random.randrange(0,display_width - thing_width[0]))
    thing_starty.append(random.randrange(-300,-100))

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_r:
                    game_loop()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change

        gameDisplay.fill(black)

        car(x,y)

        for i in range(thing_count):
            if thing_starty[i] > display_height:
                thing_starty[i] = random.randrange(-300, -100)
                thing_startx[i] = random.randrange(0, display_width - thing_width[i])

            object_rect(thing_startx[i], thing_starty[i], white, thing_width[i], thing_height)
            thing_starty[i] += thing_speed

            if y < thing_starty[i] + thing_height and y + car_height > thing_starty[i]:
                if thing_startx[i] + thing_width[i] > x and thing_startx[i] < x + car_width:
                    crash(count)

        button(725,5,70,70,black,black,pauseImg,action=paused)

        things_dodged(count)

        if x > display_width - car_width : x = display_width - car_width
        elif x < 0 : x = 0

        if y < 0: y = 0
        elif y > display_height - car_height : y = display_height - car_height

        if thing_starty[0] > display_height:
            count += 1
            if count % 5 == 0 and count < 10:
                thing_speed += 2
            if count == 15:
                thing_speed += 1
            if thing_count <= 5:
                thing_width.append(random.randrange(50,100))
                thing_startx.append(random.randrange(0,display_width - thing_width[thing_count]))
                thing_starty.append(random.randrange(-300,-100))
                thing_count += 1

        pygame.display.update()
        clock.tick(60)

game_intro()
pygame.quit()
quit()
