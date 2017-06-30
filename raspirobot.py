# -*- coding: UTF-8 -*-

# Pygame-Modul importieren.
import pygame
import subprocess
from rrb3 import *
import time
import os
import sys
import unicornleds as leds

import DistanceSocket.mod as mod
# Roboter-Module initialisieren
rr=RRB3(9,6)
rr.set_led1(1)
rr.set_led1(0)
rr.set_led2(1)
rr.set_led2(0)
rr.sw1_closed()
rr.stop()

# Integer für Ultraschellsensor definieren
i=0
f= open("raspirobot.log", "w")
sys.stdout = f

# Initialisieren aller Pygame-Module und    
# Fenster erstellen (wir bekommen eine Surface, die den Bildschirm repräsentiert).

pygame.init()

screen = pygame.display.set_mode((100, 100))

# Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.

pygame.display.set_caption("RapiRobot")

pygame.mouse.set_visible(1)

pygame.key.set_repeat(1, 30)


# Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.

clock = pygame.time.Clock()

Ausweichen=0
Stehenbleiben=1
Ultraschallmodus=0
Putzmodus=0
# Die Schleife, und damit unser Spiel, läuft solange running == True.
down = False
running = True


Speed=0.55
sp=Speed
SlowSpeed=0.05
leds.ok()
subprocess.Popen('sudo bash /home/pi/openFlask.sh', shell=True)	
while running:

        # Framerate auf 30 Frames pro Sekunde beschränken.

        # Pygame wartet, falls das Programm schneller läuft.

        clock.tick(30)


        # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.

        screen.fill((255, 255, 255))
        
        # Ultraschallwert abfragen
        i = rr.get_distance()
      
                
       
        switch= rr.sw1_closed()
	bumm = rr.sw2_closed()
	
        
        # Eine Viertelsekunde warten
        time.sleep(0.05)
        
        # Und wenn die Distanz zum Hindernis kleiner als 20 Zentimeter ist, anhalten
        if Ultraschallmodus == 1:
		if i < 30:
			leds.warn()
                        if i < 20:
				leds.warnhard()
				if Putzmodus == 0:
					rr.set_motors(sp,1,sp,1)
					rr.set_led1(1)
					rr.set_led2(1)
					time.sleep(0.05)
					rr.set_led1(0)
					rr.set_led2(0)
                        	if Putzmodus == 1:
					if Ausweichen == 1:
						rr.set_motors(0.20,0,0.20,1)
						time.sleep(0.5)

					if Stehenbleiben == 1:
						rr.set_motors(0,0,0,0)
						rr.set_led1(1)
						rr.set_led2(1)
						time.sleep(0.5)
						rr.set_led1(0)
						rr.set_led2(0)
                        else:
				if Putzmodus == 1:
					if Ausweichen == 1:
						rr.set_motors(0.20,0,0.20,1)
						time.sleep(0.5)

					if Stehenbleiben == 1:
						rr.set_motors(0,0,0,0)
						rr.set_led1(1)
						rr.set_led2(1)
						time.sleep(0.5)
						rr.set_led1(0)
						rr.set_led2(0)
				else:
					
					if Ausweichen == 1:
						rr.set_motors(sp,0,sp,1)
						time.sleep(0.5)

					if Stehenbleiben == 1:
						rr.set_motors(0,0,0,0)
						rr.set_led1(1)
						rr.set_led2(1)
						time.sleep(0.5)
						rr.set_led1(0)
						rr.set_led2(0)
                                
		else:
                        leds.forward()
			rr.set_motors(sp,0,sp,0)
                      


               
        
        	
        
        if switch == True:
	     	leds.c3()
	     	time.sleep(1)
	     	leds.c2()
	     	time.sleep(1)
	     	leds.c1()
	     	time.sleep(1)
	     	leds.c0()
	     	time.sleep(1)
             	os.system("sudo shutdown now -h")
                
                # Alle aufgelaufenen Events holen und abarbeiten.

        for event in pygame.event.get():

                # Spiel beenden, wenn wir ein QUIT-Event finden.

                if event.type == pygame.QUIT:

                        running = False

                

                # Wir interessieren uns auch für "Taste gedrückt"-Events.

                if event.type == pygame.KEYDOWN:
                        

                        # Wenn Escape gedrückt wird, posten wir ein QUIT-Event #in Pygames Event-Warteschlange.

                        if event.key == pygame.K_ESCAPE:
                                pygame.event.post(pygame.event.Event(pygame.QUIT))
				f.close()
 
        # Wenn vorwärts gedrückt wird, vorwärts fahren
                        
                        elif event.key == pygame.K_UP:    
                                rr.set_motors(sp,0,sp,0)
                                leds.forward()
                        
                        # Bei links links abbiegen
                        
                        elif event.key == pygame.K_LEFT:
                                rr.set_motors(sp,0,SlowSpeed,0)
                                rr.set_led2(0)
				leds.left()
                        
                        # Und bei rechts dann rechts
                        
                        elif event.key == pygame.K_RIGHT:

                                rr.set_motors(SlowSpeed,0,sp,0)
                                rr.set_led1(0)
				leds.right()
                        
                        # Wenn man nach unten drückt, dann stehenbleiben

                        elif event.key == pygame.K_1:

                                Ausweichen=1
                                Stehenbleiben=0

                        elif event.key == pygame.K_2:

                                Ausweichen=0
                                Stehenbleiben=1
                        elif event.key == pygame.K_4:
                                Ultraschallmodus=1
                                
                        elif event.key == pygame.K_3:
                                Ultraschallmodus=0
                        elif event.key == pygame.K_5:
                                subprocess.Popen('/home/pi/sync.sh', shell=True)
                                
                                running = False
                        
                        elif event.key == pygame.K_6:
				sp=0.35
				Putzmodus=1
                        
                        if event.key == pygame.K_DOWN:
                                if Ultraschallmodus == 1:
					leds.stop()
                                        
                                        down = True
                                        while down:

                                                for event in pygame.event.get():

                                                        if event.type == pygame.KEYDOWN:

                                                                if event.key == pygame.K_UP:
                                                                        down = False

                                                rr.set_motors(0,0,0,0)
                                                rr.set_led1(0)
                                                rr.set_led2(0)
					leds.forward()
                                 
                                else:
					leds.back()
                                        rr.set_motors(sp,1,sp,1)
                                        
                else:
                        if Ultraschallmodus == 1:
                                rr.set_motors(sp,0,sp,0)
                                rr.set_led1(1)
                                rr.set_led2(1)
				leds.forward()
                        else:
				leds.ok()
                                rr.set_motors(0,0,0,0)
                        

                
        # Inhalt von screen anzeigen.

        pygame.display.flip()
