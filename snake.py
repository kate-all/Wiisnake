#Kate Allsebrook
#Welcome to the classic game of snake, but with a wii remote!

import pygame
import cwiid
import time
import random

#Some system parameters
WINDOW_HEIGHT = 450
WINDOW_WIDTH = 400
X = 0
Y = 1

pygame.init()
font = pygame.font.Font(None, 30)

#Global Variable
delay = 0.1

#Snake class
class Snake:
    def __init__ (self):
        self.length = 1
        self.currentPos = [int(WINDOW_WIDTH / 2), int((WINDOW_HEIGHT - 50) / 2)]
        self.prevPos = [self.currentPos] #--> A list of size length previous positions for the snake's tail
        self.colour = [255, 0, 0]
        self.size = 10
        self.headDir = 0
        self.growInc = 4

    def draw(self, screen):
        for pos in self.prevPos:
            pygame.draw.rect(screen, self.colour, [pos[X], pos[Y], self.size, self.size])
            pygame.draw.rect(screen, [160,0,0], [pos[X], pos[Y], self.size, self.size], 1)
    
    def move(self, inc):
        '''This function will move the snake one increment in the direction its head is travelling'''
        if self.headDir == "R":
            self.currentPos = [self.currentPos[X] + int(inc), self.currentPos[Y]]

        elif self.headDir == "L":
            self.currentPos = [self.currentPos[X] - int(inc), self.currentPos[Y]]

        elif self.headDir == "D":
            self.currentPos = [self.currentPos[X], self.currentPos[Y] + int(inc)]

        elif self.headDir == "U":
            self.currentPos = [self.currentPos[X], self.currentPos[Y] - int(inc)]

        self.updateTail()

    def updateTail(self):
        '''Updates the position of each of the tail segments'''
        self.prevPos.append(self.currentPos)
        self.prevPos.pop(0)

    def eatFood(self):
        '''Grows when food is eaten'''
        #Adding to the end of a long snake
        if self.length > 1:
            self.grow(self.findTailDir())
        
        #Adding to the end of a short snake
        else:
            self.grow(self.headDir)
        
        #Update length attribute
        self.length += self.growInc

    def grow(self, direction):
        '''Adds a block to the end of the snake'''
        for i in range(self.growInc):
            if direction == "R":
                self.prevPos.insert(0, [self.prevPos[0][X] - self.size, self.prevPos[0][Y]])

            elif direction == "L":
                self.prevPos.insert(0, [self.prevPos[0][X] + self.size, self.prevPos[0][Y]])

            elif direction == "U":
                self.prevPos.insert(0, [self.prevPos[0][X], self.prevPos[0][Y] + self.size])

            elif direction == "D":
                self.prevPos.insert(0, [self.prevPos[0][X], self.prevPos[0][Y] - self.size])

    def findTailDir(self):
        '''Calculates the direction of the end of the snake's tail
        Returns: A string with a letter (U,D,L,R) representing the direction of the end of the tail's movement'''
        #Calc xDir
        xDir = self.prevPos[1][X] - self.prevPos[0][X] 
        if xDir == -10:
            return "L"
        elif xDir == 10:
            return "R"

        #Calc yDir
        yDir = self.prevPos[1][Y] - self.prevPos[0][Y]
        if yDir == -10:
            return "U"
        elif yDir == 10:
            return "D"

#Food class
class Food:
    def __init__(self):
        self.colour = [255, 255, 0]
        self.size = 10
        self.currentPos = [random.randint(0, WINDOW_WIDTH - self.size), random.randint(0, WINDOW_HEIGHT - self.size)]
        self.currentPos = [self.currentPos[X] - (self.currentPos[X] % 10), self.currentPos[Y] - (self.currentPos[Y] % 10)]

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.currentPos[X], self.currentPos[Y], self.size, self.size])

    def move(self, snake1):
        flag = True
        while flag:
            self.currentPos = [random.randint(0, WINDOW_WIDTH - self.size), random.randint(0, WINDOW_HEIGHT - self.size - 50)]
            self.currentPos = [self.currentPos[X] - (self.currentPos[X] % 10), self.currentPos[Y] - (self.currentPos[Y] % 10)]
            flag =  self.currentPos in snake1.prevPos

#Global methods
def wiimoteSetup(playerNum):
    '''This function will connect the wii remote and return it. If the wii
    remote fails to connect, it will return a value of None'''
    try:
        wm = cwiid.Wiimote()
    except RuntimeError:
        return None

    wm.rpt_mode = cwiid.RPT_BTN
    wm.led = playerNum

    return wm

def gameOverScreen():
    '''Displays a game over message and provides the player options to play again,
    return to the menu, or quit'''

def calcHighScore(highScore, currentScore):
    '''Checks if a new high score has been earned, and replaces it if necessary
    Takes in: An integer representing the current high score and an integer representing the current score'''
    if currentScore > highScore:
        try:
            hsFile = open("./highScore.txt", 'w')
            hsFile.write(str(currentScore))
        except:
            print("hsFile not opening")
        
        hsFile.close()

def wiimoteImgSetup(filePath):
    '''Configures the wii remote image and returns the finished product'''
    imgWiimote = pygame.image.load(filePath)
    imgWiimote.convert()
    imgWiimote = pygame.transform.rotozoom(imgWiimote, 90, 0.3)
    return imgWiimote

def drawCornerRect(screen):
    pygame.draw.rect(screen, [0,0,0], [250, 373, 145, 20])

def welcomeScreen():
    '''Displays a welcome screen for user to connect their wii remote(s) to.'''
    #Wii remote objects
    wm1 = None
    wm2 = None

    #Screen flags
    screen1 = True
    screen2 = False
    screen3 = False
    
    #Screen configs
    screen = pygame.display.set_mode([400, 400])
    screen.fill([250, 200, 150])
    pygame.display.set_caption("Welcome!")
    pygame.display.flip()

    #Image configs
    remote1Pos = 50
    imgWiimote = wiimoteImgSetup("./wiimote_diagram.png")
    imgWiimote2 = wiimoteImgSetup("./wiimote_diagram.png")

    #Text configs
    smallFont = pygame.font.Font(None, 20)

    titleTxt = "Welcome to Wiisnake!"
    text1 = font.render(titleTxt, True, [0,0,0])

    wlcTxtPos = 70
    wlcTxt = "To start, press 1 and 2 on your wii remote at the same time."
    text2 = smallFont.render(wlcTxt, True, [0,0,0])

    nxtTxt = "Press A to continue"
    text3 = smallFont.render(nxtTxt, True, [255,255,255])

    chooseTxt = "Press + to play single player"
    chooseTxt2 = "Press - to play multi player"
    text4 = smallFont.render(chooseTxt, True, [0,0,0])
    text5 = smallFont.render(chooseTxt2, True, [0,0,0])

    wlcTxt2 = "Press 1 and 2 on your other wii remote at the same time."
    text6 = smallFont.render(wlcTxt2, True, [0,0,0])

    mpTxt = "Press A to start game"
    text7 = smallFont.render(mpTxt, True, [255,255,255])

    #Simulation
    running = True
    while running:
        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        #Screen 1
        if screen1:
            #Display
            screen.blit(imgWiimote, [(400 - imgWiimote.get_size()[0]) // 2,remote1Pos])
            #screen.blit(imgWiimote2, [(400 - imgWiimote2.get_size()[0]) // 2, remote1Pos + 100])
            screen.blit(text1, [(400 - font.size(titleTxt)[0]) // 2,10]) 
            screen.blit(text2, [(400 - smallFont.size(wlcTxt)[0]) // 2,wlcTxtPos]) 

            pygame.display.flip()
       
            #Connect Wii remote
            while wm1 == None:
                wm1 = wiimoteSetup(1)

            #Show blue wii remote
            imgWiimote = wiimoteImgSetup("./wiimote_diagram_backup.png") 
            screen.blit(imgWiimote, [(400 - imgWiimote.get_size()[0]) // 2,remote1Pos])

            #Continue Prompt
            drawCornerRect(screen)
            screen.blit(text3, [260,375])

            pygame.display.flip()

            if wm1.state['buttons'] & cwiid.BTN_A:
                screen.fill([250, 200, 150])
                screen1 = False
                screen2 = True

        elif screen2:
            #Display
            pygame.draw.rect(screen,[255,100,100],[(400 - smallFont.size(chooseTxt)[0]) // 2,70,smallFont.size(chooseTxt)[0],smallFont.size(chooseTxt)[1]])
            pygame.draw.rect(screen,[100,100,255],[(400 - smallFont.size(chooseTxt2)[0]) // 2,100,smallFont.size(chooseTxt2)[0],smallFont.size(chooseTxt2)[1]])

            screen.blit(text1, [(400 - font.size(titleTxt)[0]) // 2,10])
            screen.blit(text4, [(400 - smallFont.size(chooseTxt)[0]) // 2,70])
            screen.blit(text5, [(400 - smallFont.size(chooseTxt2)[0]) // 2,100])

            pygame.display.flip()

            if wm1.state['buttons'] & cwiid.BTN_PLUS:
                singlePlayerGame(wm1)

            elif wm1.state['buttons'] & cwiid.BTN_MINUS:
                screen.fill([250, 200, 150])
                screen2 = False
                screen3 = True

        elif screen3:
            #Display
            screen.blit(imgWiimote, [(400 - imgWiimote.get_size()[0]) // 2,remote1Pos])
            screen.blit(imgWiimote2, [(400 - imgWiimote2.get_size()[0]) // 2, remote1Pos + 100])
            screen.blit(text1, [(400 - font.size(titleTxt)[0]) // 2,10]) 
            screen.blit(text6, [(400 - smallFont.size(wlcTxt2)[0]) // 2,wlcTxtPos]) 

            pygame.display.flip()
            
            #Connect second wii remote
            while wm2 == None:
                wm2 = wiimoteSetup(2)

            #Show blue wii remote
            imgWiimote2 = wiimoteImgSetup("./wiimote_diagram_backup.png") 
            screen.blit(imgWiimote2, [(400 - imgWiimote2.get_size()[0]) // 2, remote1Pos + 100])

            #Prompt multiplayer game start
            drawCornerRect(screen)
            screen.blit(text7, [255,375])

            #Start game
            if (wm1.state['buttons'] & cwiid.BTN_A) or (wm2.state['buttons'] & cwiid.BTN_A):
                print("it works")
                multiplayerGame(wm1,wm2)

def singlePlayerGame(wm):
    global delay

    #Set up pygame
    screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wiisnake")

    #Get high score
    try:
        hsFile = open("./highScore.txt", 'r')
        currentHighScore = hsFile.readline().strip()
    except:
        print("Error opening hsFile")
    hsFile.close()

    #Initialize Snake object and food
    snek1 = Snake()
    currentFood = Food()
    
    #Simulation loop:
    running = True
    while running:

        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #Handle user input NOTE: Turn wiimote sideways
        #Down
        if ((wm.state['buttons'] & cwiid.BTN_LEFT) and
                ((snek1.headDir != "U" and snek1.length > 1) or (snek1.length == 1))): #Snake cannot move on top of its tail
            snek1.headDir = "D"
            time.sleep(delay)         
        
        #Up
        elif ((wm.state['buttons'] & cwiid.BTN_RIGHT) and 
                ((snek1.headDir != "D" and snek1.length > 1) or (snek1.length == 1))):
            snek1.headDir = "U"
            time.sleep(delay)          

        #Left
        elif ((wm.state['buttons'] & cwiid.BTN_UP) and
                ((snek1.headDir != "R" and snek1.length > 1) or (snek1.length == 1))): 
            snek1.headDir = "L"
            time.sleep(delay)          
        
        #Right
        elif ((wm.state['buttons'] & cwiid.BTN_DOWN) and 
                ((snek1.headDir != "L" and snek1.length > 1) or (snek1.length == 1))):
            snek1.headDir = "R"
            time.sleep(delay) 

        #Move Snake
        snek1.move(snek1.size)
        time.sleep(delay)

        #Draw background
        screen.fill([0,0,0])
        
        #Draw foreground
        currentFood.draw(screen)
        snek1.draw(screen)

        pygame.draw.rect(screen, [25,100,220], [0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50]) #Bottom blue block

        #Text
        textLength = font.render("Length: " + str(snek1.length), True, [0,0,0])
        screen.blit(textLength, [20,WINDOW_HEIGHT - textLength.get_height() - 15]) 

        textHighScore = font.render("High Score: " + currentHighScore, True, [0,0,0])
        screen.blit(textHighScore, [WINDOW_WIDTH - textHighScore.get_width() - 40, WINDOW_HEIGHT - textHighScore.get_height() - 15]) 

        #Check if...
        #Snake hits the edge
        if ((snek1.currentPos[X] < 0 or int(snek1.currentPos[X]) + int(snek1.size) > WINDOW_WIDTH) or 
                (snek1.currentPos[Y] < 0 or int(snek1.currentPos[Y]) + int(snek1.size) > WINDOW_HEIGHT - 50)):
            print("Game over")
            calcHighScore(int(currentHighScore), snek1.length)
            running = False

        #Snake hits itself
        if snek1.currentPos in snek1.prevPos[:-1]:
            print("Game over 2")
            calcHighScore(int(currentHighScore), snek1.length)
            running = False

        #Snake eats food 
        if (snek1.currentPos[X] == currentFood.currentPos[X] and snek1.currentPos[Y] == currentFood.currentPos[Y]):
            snek1.eatFood()
            currentFood.move(snek1)

            #Speed up snake
            if delay >= 0.04:
                delay -= 0.003

        #Refresh
        pygame.display.flip()
        clock.tick(300)  

def multiplayerGame(wm1,wm2):
    '''This is the multiplayer version of wiisnake'''

welcomeScreen()
