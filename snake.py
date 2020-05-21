#Kate Allsebrook
#Welcome to the classic game of snake, but with a wii remote!

import pygame
import cwiid
import time
import random

#Some system parameters
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
delay = 0.1
X = 0
Y = 1

#Snake class
class Snake:
    def __init__ (self):
        self.length = 1
        self.currentPos = [int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2)]
        self.prevPos = [self.currentPos] #--> A list of size length previous positions for the snake's tail
        self.colour = [255, 0, 0]
        self.size = 10

    def draw(self, screen):
        for pos in self.prevPos:
            pygame.draw.rect(screen, self.colour, [pos[X], pos[Y], self.size, self.size])
    
    def moveX(self, xInc):
        self.currentPos = [self.currentPos[X] + int(xInc), self.currentPos[Y]]
        self.updateTail()

    def moveY(self, yInc):
        self.currentPos = [self.currentPos[X], self.currentPos[Y] + int(yInc)]
        self.updateTail()

    def updateTail(self):
        '''Updates the position of each of the tail segments'''
        self.prevPos.append(self.currentPos)
        self.prevPos.pop(0)

    def eatFood(self):
        '''Grows when food is eaten'''
        self.length += 1
        self.prevPos.append(self.currentPos)
        self.prevPos[0] = self.currentPos

#Food class
class Food:
    def __init__(self):
        self.colour = [255, 255, 0]
        self.size = 10
        self.currentPos = [random.randint(0, WINDOW_WIDTH - self.size), random.randint(0, WINDOW_HEIGHT - self.size)]
        self.currentPos = [self.currentPos[X] - (self.currentPos[X] % 10), self.currentPos[Y] - (self.currentPos[Y] % 10)]

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.currentPos[X], self.currentPos[Y], self.size, self.size])

    def move(self):
        self.currentPos = [random.randint(0, WINDOW_WIDTH - self.size), random.randint(0, WINDOW_HEIGHT - self.size)]
        self.currentPos = [self.currentPos[X] - (self.currentPos[X] % 10), self.currentPos[Y] - (self.currentPos[Y] % 10)]


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

def main():
    #Set up wii remote
    wm = wiimoteSetup()

    #Set up pygame
    screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    clock = pygame.time.Clock()

    #Initialize Snake object and first food
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
        if (wm.state['buttons'] & cwiid.BTN_LEFT):
            snek1.moveY(snek1.size)
            time.sleep(delay)         
        
        #Up
        elif(wm.state['buttons'] & cwiid.BTN_RIGHT):
            snek1.moveY(-snek1.size)
            time.sleep(delay)          

        #Left
        elif (wm.state['buttons'] & cwiid.BTN_UP):
            snek1.moveX(-snek1.size)
            time.sleep(delay)          
        
        #Right
        elif (wm.state['buttons'] & cwiid.BTN_DOWN):
            snek1.moveX(snek1.size)
            time.sleep(delay)  

        #if (wm.state['buttons'] & cwiid.BTN_A):
        #    print('Button A pressed')
        #    time.sleep(delay)          

        #Draw background
        screen.fill([0,0,0])
        
        #Draw foreground
        currentFood.draw(screen)
        snek1.draw(screen)

        #Check if...
        #Snake hits the edge
        if ((snek1.currentPos[X] < 0 or int(snek1.currentPos[X]) + int(snek1.size) > WINDOW_WIDTH) or 
                (snek1.currentPos[Y] < 0 or int(snek1.currentPos[Y]) + int(snek1.size) > WINDOW_HEIGHT)):
            print("Game over")
            running = False

        #Snake hits itself
        #if snek1.currentPos in snek1.prevPos:
        #    print("Game over 2")
        #    running = False

        #Snake eats food 
        if (snek1.currentPos[X] == currentFood.currentPos[X] and snek1.currentPos[Y] == currentFood.currentPos[Y]):
            snek1.eatFood()
            currentFood.move()

        #Refresh
        pygame.display.flip()
        clock.tick(300)  

main()
