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

            #Red snake outline
            if self.colour == [255,0,0]:
                pygame.draw.rect(screen, [160,0,0], [pos[X], pos[Y], self.size, self.size], 1)
            elif self.colour == [0,255,0]:
                pygame.draw.rect(screen, [0,160,0], [pos[X], pos[Y], self.size, self.size], 1)
    
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
        self.currentPos = [(random.randint(0, WINDOW_WIDTH - self.size)) // 10 * 10, (random.randint(0, WINDOW_HEIGHT - self.size)) // 10 * 10]

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.currentPos[X], self.currentPos[Y], self.size, self.size])

    def move(self, snake1, snake2):
        flag = True
        while flag:
            self.currentPos = [(random.randint(0, WINDOW_WIDTH - self.size)) // 10 * 10, (random.randint(0, WINDOW_HEIGHT - self.size)) // 10 * 10]
            flag =  (self.currentPos in snake1.prevPos) or (snake2 != None and (self.currentPos in snake2.prevPos))

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

def calcHighScore(highScore, currentScore):
    '''Checks if a new high score has been earned, and replaces it if necessary
    Takes in: An integer representing the current high score and an integer representing the current score
    Returns: A boolean value that is true if a new high score has been achieved, and false otherwise.'''
    if currentScore > highScore:
        try:
            hsFile = open("./highScore.txt", 'w')
            hsFile.write(str(currentScore))
        except:
            print("hsFile not opening")
        return True

        hsFile.close()

    return False

def wiimoteImgSetup(filePath):
    '''Configures the wii remote image and returns the finished product'''
    imgWiimote = pygame.image.load(filePath)
    imgWiimote.convert()
    imgWiimote = pygame.transform.rotozoom(imgWiimote, 90, 0.3)
    return imgWiimote

def drawCornerRect(screen):
    pygame.draw.rect(screen, [0,0,0], [250, 373, 145, 20])

def gameOver1Player(isHighScore, score, wm1, wm2):
    '''Displays a game over window displaying the winner.
    Takes in: A boolean representing if the user achieved a new high score, the player's current score,
    the first wii remote, and the second wii remote, which will be None if not connected.'''

    #Screen configs
    screen1 = True
    screen2 = False

    screen = pygame.display.set_mode([300, 200])
    screen.fill([250, 200, 150])
    pygame.display.set_caption("Game Over")

    #Text Configs
    medFont = pygame.font.Font(None, 50)
    smallFont = pygame.font.Font(None, 20)
    otherFont = pygame.font.Font(None, 40)

    #Score display
    hsCount = 1
    if isHighScore:
        newHSTxt = "New High Score!"
        textNewHS = otherFont.render(newHSTxt, True, [200,0,0])

        hsCount = 0

    scoreTxt = "Your Score: " + str(score)
    textScore = medFont.render(scoreTxt, True, [0,0,0])

    contTxt = "Press A to continue"
    textCont = smallFont.render(contTxt, True, [0,0,0])
    
    menu1Txt = "Play again"
    textMenu1 = smallFont.render(menu1Txt, True, [0,0,0])
    
    menu2Txt = "Play multiplayer mode"
    textMenu2 = smallFont.render(menu2Txt, True, [0,0,0])

    menu3Txt = "Exit"
    textMenu3 = smallFont.render(menu3Txt, True, [0,0,0])

    plusText = "+"
    textPlus = otherFont.render(plusText, True, [0,0,0])

    oneText = "1"
    text1 = otherFont.render(oneText, True, [0,0,0])

    minusText = "-"
    textMinus = otherFont.render(minusText, True, [0,0,0])

    #Simulation
    running = True
    while running:
        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if screen1:
            #Display
            #Flashing high score
            if hsCount % 500 == 0:
                textNewHS = otherFont.render(newHSTxt, True, [0,200,0])
            elif hsCount % 250 == 0:
                textNewHS = otherFont.render(newHSTxt, True, [200,0,0])

            if isHighScore:
                hsCount += 1
                screen.blit(textNewHS, [(300 - otherFont.size(newHSTxt)[0]) // 2,30])

            screen.blit(textScore, [(300 - medFont.size(scoreTxt)[0]) // 2,(200 - medFont.size(scoreTxt)[1]) // 2])
            screen.blit(textCont, [300 - (smallFont.size(contTxt)[0] + 10),200 - (smallFont.size(contTxt)[1] + 10)])

            pygame.display.flip()

            #Move to Screen 2
            if (wm1.state['buttons'] & cwiid.BTN_A) or (wm2 != None and (wm2.state['buttons'] & cwiid.BTN_A)):
                screen.fill([250, 200, 150])
                screen1 = False
                screen2 = True

        elif screen2:
            #Display
            pygame.display.set_caption("Menu")
            screen.fill([250, 200, 150])

            pygame.draw.rect(screen,[255,100,100],[(300 - smallFont.size(menu1Txt)[0]) // 2 - 65,25,smallFont.size(menu2Txt)[0] + 60,smallFont.size(menu2Txt)[1] * 2])
            pygame.draw.rect(screen,[150,150,255],[(300 - smallFont.size(menu2Txt)[0]) // 2 - 27,75,smallFont.size(menu2Txt)[0] + 60,smallFont.size(menu2Txt)[1] * 2])
            pygame.draw.rect(screen,[200,255,200],[(300 - smallFont.size(menu3Txt)[0]) // 2 - 85,125,smallFont.size(menu2Txt)[0] + 60,smallFont.size(menu2Txt)[1] * 2])

            screen.blit(textMenu1, [(300 - smallFont.size(menu1Txt)[0]) // 2,32])
            screen.blit(textMenu2, [(300 - smallFont.size(menu2Txt)[0]) // 2,82])
            screen.blit(textMenu3, [(300 - smallFont.size(menu3Txt)[0]) // 2,132])

            screen.blit(textPlus, [15,20])
            screen.blit(text1, [15,75])
            screen.blit(textMinus, [18,125])

            pygame.display.flip()

            #Interaction
            if (wm1.state['buttons'] & cwiid.BTN_PLUS) or (wm2 != None and (wm2.state['buttons'] & cwiid.BTN_PLUS)):
                singlePlayerGame(wm1,wm2)
                quit()

            elif (wm1.state['buttons'] & cwiid.BTN_1) or (wm2 != None and (wm2.state['buttons'] & cwiid.BTN_1)):
                if wm2 == None:
                    welcomeScreen(True, wm1) #Starts at screen 3 to connect second wii remote
                else:
                    multiplayerGame(wm1,wm2)
                quit()

            elif (wm1.state['buttons'] & cwiid.BTN_MINUS) or (wm2 != None and (wm2.state['buttons'] & cwiid.BTN_MINUS)):
                running = False
                quit()

def gameOver2Player(winner, wm1, wm2):
    '''Displays a game over window displaying the winner.
    Takes in: A string representing which player won, or if there was a tie. Both wii remote objects.'''

    #Screen configs
    screen1 = True
    screen2 = False

    screen = pygame.display.set_mode([300, 200])
    screen.fill([250, 200, 150])
    pygame.display.set_caption("Game Over")

    #Text Configs
    medFont = pygame.font.Font(None, 50)
    smallFont = pygame.font.Font(None, 20)
    otherFont = pygame.font.Font(None, 40)

    #Winner display
    tieCount = 1
    if winner == "Tie":
        winnerTxt = "Tie!"
        medFont = pygame.font.Font(None, 100)
        textWinner = medFont.render(winnerTxt, True, [255,0,0])
        tieCount = 0
    else:
        winnerTxt = winner + " wins!"

        if winner == "Player 1":
            textWinner = medFont.render(winnerTxt, True, [200,0,0])

        else:
            textWinner = medFont.render(winnerTxt, True, [0,200,0])

    contTxt = "Press A to continue"
    textCont = smallFont.render(contTxt, True, [0,0,0])
    
    menu1Txt = "Play again"
    textMenu1 = smallFont.render(menu1Txt, True, [0,0,0])
    
    menu2Txt = "Play single player mode"
    textMenu2 = smallFont.render(menu2Txt, True, [0,0,0])

    menu3Txt = "Exit"
    textMenu3 = smallFont.render(menu3Txt, True, [0,0,0])

    plusText = "+"
    textPlus = otherFont.render(plusText, True, [0,0,0])

    oneText = "1"
    text1 = otherFont.render(oneText, True, [0,0,0])

    minusText = "-"
    textMinus = otherFont.render(minusText, True, [0,0,0])

    #Simulation
    running = True
    while running:
        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if screen1:
            #Display
            #Flashing Tie
            if tieCount % 500 == 0:
                textWinner = medFont.render(winnerTxt, True, [0,200,0])
            elif tieCount % 250 == 0:
                textWinner = medFont.render(winnerTxt, True, [200,0,0])

            if winner == "Tie":
                tieCount += 1

            screen.blit(textWinner, [(300 - medFont.size(winnerTxt)[0]) // 2,(200 - medFont.size(winnerTxt)[1]) // 2])
            screen.blit(textCont, [300 - (smallFont.size(contTxt)[0] + 10),200 - (smallFont.size(contTxt)[1] + 10)])

            pygame.display.flip()

            #Move to Screen 2
            if (wm1.state['buttons'] & cwiid.BTN_A) or (wm2.state['buttons'] & cwiid.BTN_A):
                screen.fill([250, 200, 150])
                screen1 = False
                screen2 = True

        elif screen2:
            #Display
            pygame.display.set_caption("Menu")
            screen.fill([250, 200, 150])

            pygame.draw.rect(screen,[255,100,100],[(300 - smallFont.size(menu1Txt)[0]) // 2 - 65,25,smallFont.size(menu2Txt)[0] + 40,smallFont.size(menu2Txt)[1] * 2])
            pygame.draw.rect(screen,[150,150,255],[(300 - smallFont.size(menu2Txt)[0]) // 2 - 20,75,smallFont.size(menu2Txt)[0] + 40,smallFont.size(menu2Txt)[1] * 2])
            pygame.draw.rect(screen,[200,255,200],[(300 - smallFont.size(menu3Txt)[0]) // 2 - 85,125,smallFont.size(menu2Txt)[0] + 40,smallFont.size(menu2Txt)[1] * 2])

            screen.blit(textMenu1, [(300 - smallFont.size(menu1Txt)[0]) // 2,32])
            screen.blit(textMenu2, [(300 - smallFont.size(menu2Txt)[0]) // 2,82])
            screen.blit(textMenu3, [(300 - smallFont.size(menu3Txt)[0]) // 2,132])

            screen.blit(textPlus, [15,20])
            screen.blit(text1, [15,75])
            screen.blit(textMinus, [18,125])

            pygame.display.flip()

            #Interaction
            if (wm1.state['buttons'] & cwiid.BTN_PLUS) or (wm2.state['buttons'] & cwiid.BTN_PLUS):
                multiplayerGame(wm1,wm2)
                quit()

            elif (wm1.state['buttons'] & cwiid.BTN_1) or (wm2.state['buttons'] & cwiid.BTN_1):
                singlePlayerGame(wm1,wm2)
                quit()

            elif (wm1.state['buttons'] & cwiid.BTN_MINUS) or (wm2.state['buttons'] & cwiid.BTN_MINUS):
                running = False
                quit()

def welcomeScreen(isScreen3, wm1):
    '''Displays a welcome screen for user to connect their wii remote(s) to, and select game mode.
    Takes in: A boolean that when, true, skips right to screen 3. When false, it starts at screen 1.'''
    #Wii remote objects
    wm1 = wm1
    wm2 = None

    #Screen flags
    screen1 = not isScreen3
    screen2 = not isScreen3
    screen3 = isScreen3
    
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
    medFont = pygame.font.Font(None, 30)

    titleTxt = "Welcome to Wiisnake!"
    text1 = font.render(titleTxt, True, [0,0,0])

    wlcTxtPos = 70
    wlcTxt = "To start, press 1 and 2 on your wii remote at the same time."
    text2 = smallFont.render(wlcTxt, True, [0,0,0])

    nxtTxt = "Press A to continue"
    text3 = smallFont.render(nxtTxt, True, [255,255,255])

    chooseTxt = "Press + to play single player"
    chooseTxt2 = "Press - to play multi player"
    text4 = medFont.render(chooseTxt, True, [0,0,0])
    text5 = medFont.render(chooseTxt2, True, [0,0,0])

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
            pygame.draw.rect(screen,[255,100,100],[(400 - medFont.size(chooseTxt)[0]) // 2 - 20,120,medFont.size(chooseTxt)[0] + 40,medFont.size(chooseTxt)[1] * 2])
            pygame.draw.rect(screen,[150,150,255],[(400 - medFont.size(chooseTxt2)[0]) // 2 - 20,240,medFont.size(chooseTxt2)[0] + 40,medFont.size(chooseTxt2)[1] * 2])

            screen.blit(text1, [(400 - font.size(titleTxt)[0]) // 2,10])
            screen.blit(text4, [(400 - medFont.size(chooseTxt)[0]) // 2,128])
            screen.blit(text5, [(400 - medFont.size(chooseTxt2)[0]) // 2,248])

            pygame.display.flip()

            #Interaction
            if wm1.state['buttons'] & cwiid.BTN_PLUS:
                singlePlayerGame(wm1,wm2)
                running = False

            elif wm1.state['buttons'] & cwiid.BTN_MINUS:
                screen.fill([250, 200, 150])
                screen2 = False
                screen3 = True

        elif screen3:
            #Display
            imgWiimote = wiimoteImgSetup("./wiimote_diagram_backup.png") #Make First wii remote blue 

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
                multiplayerGame(wm1,wm2)
                running =  False

def singlePlayerGame(wm, otherRemote):
    delay = 0.1

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
            isHighScore = calcHighScore(int(currentHighScore), snek1.length)
            gameOver1Player(isHighScore, snek1.length, wm, otherRemote)
            running = False

        #Snake hits itself
        if snek1.currentPos in snek1.prevPos[:-1]:
            isHighScore = calcHighScore(int(currentHighScore), snek1.length)
            gameOver1Player(isHighScore, snek1.length, wm, otherRemote)
            running = False

        #Snake eats food 
        if (snek1.currentPos[X] == currentFood.currentPos[X] and snek1.currentPos[Y] == currentFood.currentPos[Y]):
            snek1.eatFood()
            currentFood.move(snek1, None)

            #Speed up snake
            if delay >= 0.04:
                delay -= 0.003

        #Refresh
        pygame.display.flip()
        clock.tick(300)  

def multiplayerGame(wm1,wm2):
    '''This is the multiplayer version of wiisnake'''

    delay = 0.1

    #Set up pygame
    screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT - 50])
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wiisnake")

    #Initialize Snake objects and food
    snek1 = Snake()
    snek2 = Snake()
    snek2.colour = [0,255,0] #Change snake 2 colour to green
    snek1.currentPos = [int(WINDOW_WIDTH / 2) - 10, int((WINDOW_HEIGHT - 50) / 2)]
    snek2.currentPos = [int(WINDOW_WIDTH / 2) + 10, int((WINDOW_HEIGHT - 50) / 2)]
    
    currentFood1 = Food()
    currentFood2 = Food()
    
    #Simulation loop:
    running = True
    while running:

        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #Handle user input for snake 1  NOTE: Turn wiimote sideways
        #Down
        if ((wm1.state['buttons'] & cwiid.BTN_LEFT) and
                ((snek1.headDir != "U" and snek1.length > 1) or (snek1.length == 1))): #Snake cannot move on top of its tail
            snek1.headDir = "D"
            time.sleep(delay)         
        
        #Up
        elif ((wm1.state['buttons'] & cwiid.BTN_RIGHT) and 
                ((snek1.headDir != "D" and snek1.length > 1) or (snek1.length == 1))):
            snek1.headDir = "U"
            time.sleep(delay)          

        #Left
        elif ((wm1.state['buttons'] & cwiid.BTN_UP) and
                ((snek1.headDir != "R" and snek1.length > 1) or (snek1.length == 1))): 
            snek1.headDir = "L"
            time.sleep(delay)          
        
        #Right
        elif ((wm1.state['buttons'] & cwiid.BTN_DOWN) and 
                ((snek1.headDir != "L" and snek1.length > 1) or (snek1.length == 1))):
            snek1.headDir = "R"
            time.sleep(delay) 
        
        #Handle user input for snake 2
        #Down
        if ((wm2.state['buttons'] & cwiid.BTN_LEFT) and
                ((snek2.headDir != "U" and snek2.length > 1) or (snek2.length == 1))): #Snake cannot move on top of its tail
            snek2.headDir = "D"
            time.sleep(delay)         
        
        #Up
        elif ((wm2.state['buttons'] & cwiid.BTN_RIGHT) and 
                ((snek2.headDir != "D" and snek2.length > 1) or (snek2.length == 1))):
            snek2.headDir = "U"
            time.sleep(delay)          

        #Left
        elif ((wm2.state['buttons'] & cwiid.BTN_UP) and
                ((snek2.headDir != "R" and snek2.length > 1) or (snek2.length == 1))): 
            snek2.headDir = "L"
            time.sleep(delay)          
        
        #Right
        elif ((wm2.state['buttons'] & cwiid.BTN_DOWN) and 
                ((snek2.headDir != "L" and snek2.length > 1) or (snek2.length == 1))):
            snek2.headDir = "R"
            time.sleep(delay) 

        #Move Snake
        snek1.move(snek1.size)
        snek2.move(snek2.size)
        time.sleep(delay)

        #Draw background
        screen.fill([0,0,0])
        
        #Draw foreground
        currentFood1.draw(screen)
        currentFood2.draw(screen)
        snek1.draw(screen)
        snek2.draw(screen)

        #Check if snakes eat food
        #Snake 1 eats food 1 
        if (snek1.currentPos[X] == currentFood1.currentPos[X] and snek1.currentPos[Y] == currentFood1.currentPos[Y]):
            snek1.eatFood()
            currentFood1.move(snek1, snek2)

            #Speed up snake
            if delay >= 0.04:
                delay -= 0.003

        #Snake 1 eats food 2 
        if (snek1.currentPos[X] == currentFood2.currentPos[X] and snek1.currentPos[Y] == currentFood2.currentPos[Y]):
            snek1.eatFood()
            currentFood2.move(snek1, snek2)

            #Speed up snake
            if delay >= 0.04:
                delay -= 0.003

        #Snake 2 eats food 1
        if (snek2.currentPos[X] == currentFood1.currentPos[X] and snek2.currentPos[Y] == currentFood1.currentPos[Y]):
            snek2.eatFood()
            currentFood1.move(snek1, snek2)

            #Speed up snake
            if delay >= 0.04:
                delay -= 0.003

        #Snake 2 eats food 2 
        if (snek2.currentPos[X] == currentFood2.currentPos[X] and snek2.currentPos[Y] == currentFood2.currentPos[Y]):
            snek2.eatFood()
            currentFood2.move(snek1, snek2)

            #Speed up snake
            if delay >= 0.04:
                delay -= 0.003

        #Game over cases:
        #Snake 1 hits the edge
        if ((snek1.currentPos[X] < 0 or int(snek1.currentPos[X]) + int(snek1.size) > WINDOW_WIDTH) or 
                (snek1.currentPos[Y] < 0 or int(snek1.currentPos[Y]) + int(snek1.size) > WINDOW_HEIGHT - 50)):
            gameOver2Player("Player 2", wm1, wm2)
            running = False

        #Snake 1 hits itself
        if snek1.currentPos in snek1.prevPos[:-1]:
            gameOver2Player("Player 2", wm1, wm2)
            running = False

        #Snake 2 hits the edge
        if ((snek2.currentPos[X] < 0 or int(snek2.currentPos[X]) + int(snek2.size) > WINDOW_WIDTH) or 
                (snek2.currentPos[Y] < 0 or int(snek2.currentPos[Y]) + int(snek2.size) > WINDOW_HEIGHT - 50)):
            gameOver2Player("Player 1", wm1, wm2)
            running = False

        #Snake 2 hits itself
        if snek2.currentPos in snek2.prevPos[:-1]:
            gameOver2Player("Player 1", wm1, wm2)
            running = False

        #Snake 1 collides with snake 2
        if snek1.currentPos in snek2.prevPos[:-1]:
            gameOver2Player("Player 2", wm1, wm2)

        #Snake 2 collides with snake 1
        if snek2.currentPos in snek1.prevPos[:-1]:
            gameOver2Player("Player 1", wm1, wm2)

        #Head on collision
        if snek1.currentPos == snek2.currentPos:
            gameOver2Player("Tie", wm1, wm2)

        #Refresh
        pygame.display.flip()
        clock.tick(300)  
welcomeScreen(False, None)
