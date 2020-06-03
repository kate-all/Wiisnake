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
def wiimoteSetup():
    '''This function will connect the wii remote'''
    try:
        wm = cwiid.Wiimote()
    except RuntimeError:
        print("Can't connect wii remote")
        quit()
    print("Wii remote connected")

    wm.rpt_mode = cwiid.RPT_BTN
    wm.led = 1

    return wm

def testLEDs(wm):
    '''This function will test the LEDs on the wii remote'''
    for i in range(16):
        wm.led = i
        time.sleep(1)

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

def welcomeScreen():
    '''Displays a welcome screen for user to connect their wii remote(s) to.'''

    #Screen configs
    screen = pygame.display.set_mode([400, 400])
    screen.fill([250, 200, 150])
    pygame.display.set_caption("Welcome!")
    pygame.display.flip()

    #Image configs
    remote1Pos = 70
    imgWiimote = pygame.image.load("./wiimote_diagram.png")
    imgWiimote.convert()
    imgWiimote = pygame.transform.rotozoom(imgWiimote, 90, 0.3)

    imgWiimote2 = pygame.image.load("./wiimote_diagram.png")
    imgWiimote2.convert()
    imgWiimote2 = pygame.transform.rotozoom(imgWiimote2, 90, 0.3)

    #Text configs
    smallFont = pygame.font.Font(None, 20)
    titleTxt = "Welcome to Wiisnake!"
    text1 = font.render(titleTxt, True, [0,0,0])

    spTxtPos = 60
    spTxt = "For single player mode, press 1 and 2 on your wii remote" 
    spTxt2 = "at the same time, and then press A."
    text2 = smallFont.render(spTxt, True, [0,0,0])
    text3 = smallFont.render(spTxt2, True, [0,0,0])

    mpTxtPos = 120
    mpTxt = "For multiplayer mode, press 1 and 2 on both wii remotes in"
    mpTxt2 ="the desired player order, then press A on either remote." 
    text4 = smallFont.render(mpTxt, True, [0,0,0])
    text5 = smallFont.render(mpTxt2, True, [0,0,0])

    #Simulation
    running = True
    while running:
        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(imgWiimote, [(400 - imgWiimote.get_size()[0]) // 2,remote1Pos])
        screen.blit(imgWiimote, [(400 - imgWiimote2.get_size()[0]) // 2, remote1Pos + 100])
        screen.blit(text1, [(400 - font.size(titleTxt)[0]) // 2,10]) 
        screen.blit(text2, [5,spTxtPos]) 
        screen.blit(text3, [5,spTxtPos + 15]) 
        screen.blit(text4, [5,mpTxtPos])
        screen.blit(text5, [5,mpTxtPos + 15])

        pygame.display.flip()

def singlePlayerGame():
    global delay

    #Set up wii remote
    wm = wiimoteSetup()

    #Set up pygame
    screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

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

welcomeScreen()
