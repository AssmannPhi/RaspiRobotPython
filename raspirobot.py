# -*- coding: UTF-8 -*-

# Pygame-Modul importieren.
import pygame
import subprocess
from rrb3 import *
import time
import os
import sys


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

screen = pygame.display.set_mode((800, 600))

# Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.

pygame.display.set_caption("RASPIROBOTBOARD KONTROLLCENTER")

pygame.mouse.set_visible(1)

pygame.key.set_repeat(1, 30)


# Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.

clock = pygame.time.Clock()

Ausweichen=0
Stehenbleiben=1
Ultraschallmodus=0
# Die Schleife, und damit unser Spiel, läuft solange running == True.
down = False
running = True



	
while running:

        # Framerate auf 30 Frames pro Sekunde beschränken.

        # Pygame wartet, falls das Programm schneller läuft.

        clock.tick(30)


        # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.

        screen.fill((0, 0, 0))
        
        # Ultraschallwert abfragen
        i = rr.get_distance()
      
                
       
        switch= rr.sw1_closed()
	bumm = rr.sw2_closed()
	
        
        # Eine Viertelsekunde warten
        time.sleep(0.25)
        
        # Und wenn die Distanz zum Hindernis kleiner als 20 Zentimeter ist, anhalten
        if Ultraschallmodus == 1:
		if i < 40:
                        if i < 35:
                                rr.set_motors(0.25,1,0.25,1)
                                rr.set_led1(1)
                                rr.set_led2(1)
                                time.sleep(0.05)
                                rr.set_led1(0)
                                rr.set_led2(0)
                        
			
			
                        else:
                                if Ausweichen == 1:
                                        rr.set_motors(0.25,0,0.25,1)
                                        time.sleep(0.5)

                                if Stehenbleiben == 1:
                                        rr.set_motors(0,0,0,0)
                                        rr.set_led1(1)
                                        rr.set_led2(1)
                                        time.sleep(0.5)
                                        rr.set_led1(0)
                                        rr.set_led2(0)
                                
		else:
                        
			rr.set_motors(0.25,0,0.25,0)
                      

	if bumm == True:
			
		rr.set_motors(0.25,1,0.25,1)
		rr.set_led1(1)
		rr.set_led2(1)
		time.sleep(0.05)
		rr.set_led1(0)
		rr.set_led2(0)
		time.sleep(1)
		rr.set_motors(0.25,0,0.25,0)
			
               
        
        	
        
        if switch == True:
                subprocess.Popen('sudo bash /home/pi/openFlask.sh', shell=True)
             
                
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
                                rr.set_motors(0.25,0,0.25,0)
                                
                        
                        # Bei links links abbiegen
                        
                        elif event.key == pygame.K_LEFT:
                                rr.set_motors(0.25,0,0.05,0)
                                rr.set_led2(0)
                        
                        # Und bei rechts dann rechts
                        
                        elif event.key == pygame.K_RIGHT:

                                rr.set_motors(0.05,0,0.25,0)
                                rr.set_led1(0)
                        
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
                        
                                
                        
                        if event.key == pygame.K_DOWN:
                                if Ultraschallmodus == 1:       
                                        
                                        down = True
                                        while down:

                                                for event in pygame.event.get():

                                                        if event.type == pygame.KEYDOWN:

                                                                if event.key == pygame.K_UP:
                                                                        down = False

                                                rr.set_motors(0,0,0,0)
                                                rr.set_led1(0)
                                                rr.set_led2(0)
                                 
                                else:
                                        rr.set_motors(0.25,1,0.25,1)
                                        
                else:
                        if Ultraschallmodus == 1:
                                rr.set_motors(0.25,0,0.25,0)
                                rr.set_led1(1)
                                rr.set_led2(1)
                        else:
                                rr.set_motors(0,0,0,0)
                        

                
        # Inhalt von screen anzeigen.

        pygame.display.flip()
