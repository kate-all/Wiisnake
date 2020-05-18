#Kate Allsebrook
#Welcome to the classic game of snake, but with a wii remote!

import pygame
import cwiid
import time

#Some system parameters
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

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
    
    #Simulation loop:
    running = True
    while running:

        #Quit
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        #Handle user input
        if (wm.state['buttons'] & cwiid.BTN_LEFT):
            print('Left pressed')
            time.sleep(0.2)         

        if(wm.state['buttons'] & cwiid.BTN_RIGHT):
            print('Right pressed')
            time.sleep(0.2)          

        if (wm.state['buttons'] & cwiid.BTN_UP):
            print('Up pressed')        
            time.sleep(0.2)          
    
        if (wm.state['buttons'] & cwiid.BTN_DOWN):
            print('Down pressed')      
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
        
        
        #draw foreground
        
        
        #move objects
        
            
        #refresh
        pygame.display.flip()
        clock.tick(300)  

main()
