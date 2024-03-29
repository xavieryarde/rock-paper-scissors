import pygame
from pygame.locals import *
import sys
import os
import random
import rock_paper_scissors_sp
import rock_paper_scissors_mp



pygame.init()


WIDTH = 900
HEIGHT = 550

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

font = pygame.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__),"Retro Gaming.ttf")), 25)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    running = True
    clock = pygame.time.Clock()
    click = False
    
    while running:
        clock.tick(60)
        screen.fill((255, 255, 255))
        text_width_1, text_height_1 = font.size("Main Menu")
        draw_text("Main Menu", font, (0, 0, 0), screen, screen.get_width() // 2 - text_width_1 // 2, 50)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(325, 200, 250, 50)
        button_2 = pygame.Rect(260, 300, 385, 50)
        button_3 = pygame.Rect(400, 400, 100, 50)

        pygame.draw.rect(screen, (200, 200, 200), button_1)
        pygame.draw.rect(screen, (200, 200, 200), button_2)
        pygame.draw.rect(screen, (200, 200, 200), button_3)

        if button_1.collidepoint((mx, my)):
            if click:
                rock_paper_scissors_sp.initialize_csv()
                rock_paper_scissors_sp.main()
                
                
        if button_2.collidepoint((mx, my)):
            if click:
                rock_paper_scissors_mp.initialize_csv()
                rock_paper_scissors_mp.main()
                
        if button_3.collidepoint((mx, my)):
            if click:
                sys.exit()


        text_width_2, text_height_2 = font.size("Player vs CPU")
        draw_text('Player vs CPU', font, (0, 0, 0), screen, screen.get_width() // 2 - text_width_2 // 2, 210)
        text_width_3, text_height_3 = font.size("Online Multiplayer - PvP")
        draw_text('Online Multiplayer - PvP', font, (0, 0, 0), screen, screen.get_width() // 2 - text_width_3 // 2, 310)
        text_width_4, text_height_4 = font.size("Quit")
        draw_text('Quit', font, (0, 0, 0), screen, screen.get_width() // 2 - text_width_4 // 2, 410)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

    



if __name__ == "__main__":
    main_menu()
    pygame.quit()
   



    

