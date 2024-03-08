import pygame
from pygame.locals import *
import random
import os
import sys

options = ["Rock", "Paper", "Scissors"]


def player_choice(x):
    random_num = random.randint(0, 2)
    comp_choice = options[random_num]

    user_label.fill((0, 0, 0, 0))
    comp_label.fill((0, 0, 0, 0))

    if comp_choice == "Rock":
        comp_label.blit(comp_rock, (0, 0))
    elif comp_choice == "Paper":
        comp_label.blit(comp_paper, (0, 0))
    else:
        comp_label.blit(comp_scissors, (0, 0))

    if x == "Rock":
        user_label.blit(user_rock, (0, 0))
    elif x == "Paper":
        user_label.blit(user_paper, (0, 0))
    else:
        user_label.blit(user_scissors, (0, 0))
        
    countdown_time = 3
    i = 0
    while countdown_time > 0:
        # Clear the screen during the countdown
        screen.fill((255, 255, 255)) 

        # Redraw the player and computer choices
        pic_options = [user_rock, user_paper, user_scissors] 

        # Display the countdown message
        update_message(options[i])
        screen.blit(message, ((screen.get_width() - message.get_width()) // 2, ((screen.get_height() - message.get_height()) // 2) - 150))
        
        screen.blit(pic_options[i], ((screen.get_width() - pic_options[i].get_width()) // 2, (screen.get_height() - pic_options[i].get_height()) // 2))
        

        pygame.display.update()

        # Countdown speed
        pygame.time.delay(1000)
        i = (i + 1) % len(pic_options)
        countdown_time -= 1
        
    check_winner(x, comp_choice)

def update_message(x):
    message.fill((0, 0, 0, 0))
    message_text = font.render(x, True, (0, 0, 0))
    text_x = (message.get_width() - message_text.get_width()) // 2
    text_y = (message.get_height() - message_text.get_height()) // 2

    message.blit(message_text, (text_x, text_y))

def update_player_score():
    player_score.fill((0, 0, 0, 0))
    global player_score_text
    score = int(player_score_text)
    score += 1
    player_score_text = str(score)
    player_score_surf = font.render(player_score_text, True, (0, 0, 0))
    player_score.blit(player_score_surf, (0, 0))

def update_computer_score():
    comp_score.fill((0, 0, 0, 0))
    global comp_score_text
    score = int(comp_score_text)
    score += 1
    comp_score_text = str(score)
    comp_score_surf = font.render(comp_score_text, True, (0, 0, 0))
    comp_score.blit(comp_score_surf, (0, 0))

def check_winner(player, computer):
    if player == computer:
        update_message("Draw!")
    elif player == "Rock" and computer == "Scissors":
        update_message("Player Won!")
        update_player_score()
    elif player == "Paper" and computer == "Rock":
        update_message("Player Won!")
        update_player_score()
    elif player == "Scissors" and computer == "Paper":
        update_message("Player Won!")
        update_player_score()
    else:
        update_message("Computer Won!")
        update_computer_score()
    
    

pygame.init()

# Screen
screen = pygame.display.set_mode((900, 550))
pygame.display.set_caption("Rock Paper Scissors - PvE")

# Fonts
font = pygame.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__),"Retro Gaming.ttf")), 25)
text_font = pygame.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__),"Retro Gaming.ttf")), 20)

# Load images
user_rock = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "user_rock.png")))
user_paper = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "user_paper.png")))
user_scissors = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "user_scissors.png")))

comp_rock = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "comp_rock.png")))
comp_paper = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "comp_paper.png")))
comp_scissors = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "comp_scissors.png")))

# Set width and height as desired
user_rock = pygame.transform.scale(user_rock, (200, 200)) 
user_paper = pygame.transform.scale(user_paper, (200, 200))
user_scissors = pygame.transform.scale(user_scissors, (200, 200))

comp_rock = pygame.transform.scale(comp_rock, (200, 200))
comp_paper = pygame.transform.scale(comp_paper, (200, 200))
comp_scissors = pygame.transform.scale(comp_scissors, (200, 200))

# Labels
user_label = pygame.Surface((200, 200), pygame.SRCALPHA)
comp_label = pygame.Surface((200, 200), pygame.SRCALPHA)


# Scores
player_score = pygame.Surface((50, 50), pygame.SRCALPHA)
comp_score = pygame.Surface((50, 50), pygame.SRCALPHA)

#Indicator
is_user = font.render("Player", True, (0, 0, 0))
is_comp = font.render("Computer", True, (0, 0, 0))


player_score_text = "0"
comp_score_text = "0"

# Message
message = pygame.Surface((450, 50), pygame.SRCALPHA)

# Game loop
def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                update_message("")
                mouse_pos = pygame.mouse.get_pos()
                if rock_option_rect.collidepoint(mouse_pos):
                    player_choice("Rock")
                elif paper_option_rect.collidepoint(mouse_pos):
                    player_choice("Paper")
                elif scissors_option_rect.collidepoint(mouse_pos):
                    player_choice("Scissors")

        # Draw everything
        screen.fill((255, 255, 255))

        screen.blit(user_label, (100, 200))
        screen.blit(comp_label, (600, 200))
        screen.blit(is_user, (163, 80))
        screen.blit(player_score, (350, 200))  
        screen.blit(is_comp, (641, 80))
        screen.blit(comp_score, (500, 200))
        
        message_rect = message.get_rect(center=(screen.get_width() // 2, 30))
        screen.blit(message, message_rect)
        

    
        rect_width = 200
        rect_height = 50

        # Calculate the starting x-coordinate to center the rectangles
        start_x = (screen.get_width() - (3 * rect_width + 20)) // 2
        start_y = screen.get_height() - 100

        border_width = 2
        
        # Black border
        rock_option_rect = pygame.draw.rect(screen, (0, 0, 0), (start_x, start_y, rect_width, rect_height), border_width)
        # White fill
        rock_option_rect = pygame.draw.rect(screen, (255, 255, 255), (start_x + border_width, start_y + border_width, rect_width - 2 * border_width, rect_height - 2 * border_width))

        # Black border
        paper_option_rect = pygame.draw.rect(screen, (0, 0, 0), (start_x + rect_width + 10, start_y, rect_width, rect_height), border_width)
        # White fill
        paper_option_rect = pygame.draw.rect(screen, (255, 255, 255), (start_x + rect_width + 10 + border_width, start_y + border_width, rect_width - 2 * border_width, rect_height - 2 * border_width))

        # Black border
        scissors_option_rect = pygame.draw.rect(screen, (0, 0, 0), (start_x + 2 * (rect_width + 10), start_y, rect_width, rect_height), border_width)
        # White fill
        scissors_option_rect = pygame.draw.rect(screen, (255, 255, 255), (start_x + 2 * (rect_width + 10) + border_width, start_y + border_width, rect_width - 2 * border_width, rect_height - 2 * border_width))

        rock_text = text_font.render("Rock", True, (0, 0, 0))
        paper_text = text_font.render("Paper", True, (0, 0, 0))
        scissors_text = text_font.render("Scissors", True, (0, 0, 0))

        # Calculate text positions to center them within rectangles
        rock_text_pos = ((rock_option_rect.width - rock_text.get_width()) // 2 + rock_option_rect.x,
                    (rock_option_rect.height - rock_text.get_height()) // 2 + rock_option_rect.y)

        paper_text_pos = ((paper_option_rect.width - paper_text.get_width()) // 2 + paper_option_rect.x,
                    (paper_option_rect.height - paper_text.get_height()) // 2 + paper_option_rect.y)

        scissors_text_pos = ((scissors_option_rect.width - scissors_text.get_width()) // 2 + scissors_option_rect.x,
                        (scissors_option_rect.height - scissors_text.get_height()) // 2 + scissors_option_rect.y)

        # Blit text onto the screen
        screen.blit(rock_text, rock_text_pos)
        screen.blit(paper_text, paper_text_pos)
        screen.blit(scissors_text, scissors_text_pos)
        

        pygame.display.update()


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

