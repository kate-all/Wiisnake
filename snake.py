#Kate Allsebrook
#Welcome to the classic game of snake, but with a wii remote!

import pygame
import cwiid
import time
import random

#Some system parameters
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
X = 0
Y = 1

#Snake class
class Snake:
    def __init__ (self):
        self.length = 1
        self.currentPos = [int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2)]
        #self.prevPos = [currentPos] --> A list of size length previous positions for the snake's tail
        self.colour = [255, 0, 0]
        self.size = 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.currentPos[X], self.currentPos[Y], self.size, self.size])
    
    def moveX(self, xInc):
        self.currentPos = [self.currentPos[X] + int(xInc), self.currentPos[Y]]

    def moveY(self, yInc):
        self.currentPos = [self.currentPos[X], self.currentPos[Y] + int(yInc)]

#Food class
class Food:
    def __init__(self):
        self.colour = [255, 255, 0]
        self.size = 5
        self.currentPos = [random.randint(0, WINDOW_WIDTH - self.size), random.randint(0, WINDOW_HEIGHT - self.size)]

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [self.currentPos[X], self.currentPos[Y], self.size, self.size])

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
            time.sleep(0.2)         
        
        #Up
        if(wm.state['buttons'] & cwiid.BTN_RIGHT):
            snek1.moveY(-snek1.size)
            time.sleep(0.2)          

        #Left
        if (wm.state['buttons'] & cwiid.BTN_UP):
            snek1.moveX(-snek1.size)
            time.sleep(0.2)          
        
        #Right
        if (wm.state['buttons'] & cwiid.BTN_DOWN):
            snek1.moveX(snek1.size)
            time.sleep(0.2)  
    
        if (wm.state['buttons'] & cwiid.BTN_1):
            print('Button 1 pressed')
            time.sleep(0.2)          

        if (wm.state['buttons'] & cwiid.BTN_2):
            print('Button 2 pressed')
            time.sleep(0.2)          

        if (wm.state['buttons'] & cwiid.BTN_A):
            print('Button A pressed')
            time.sleep(0.2)          

        if (wm.state['buttons'] & cwiid.BTN_B):
            print('Button B pressed')
            time.sleep(0.2)          

        if (wm.state['buttons'] & cwiid.BTN_HOME):
            print('Home Button pressed')        
            time.sleep(0.2)   
    
        if (wm.state['buttons'] & cwiid.BTN_MINUS):
            print('Minus Button pressed')
            time.sleep(0.2)   
    
        if (wm.state['buttons'] & cwiid.BTN_PLUS):
            print('Plus Button pressed')
            time.sleep(0.2)
        
        #draw background
        screen.fill([0,0,0])
        
        #draw foreground
        currentFood.draw(screen)
        snek1.draw(screen)
        
        #Check if...
        #Snake Dies

        #Snake eats food
            
        #refresh
        pygame.display.flip()
        clock.tick(300)  

main()
