import pygame
from pygame.locals import *
import sys
import os
import random
from network import Network
import main_game
import csv

options = ["Rock", "Paper", "Scissors"]

base_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "stats/mp/stats_mp.csv"))
new_file_path = ""

if not os.path.exists(base_file_path):
    # File doesn't exist, so create it
    os.makedirs(os.path.dirname(base_file_path), exist_ok=True)
    
    def initialize_csv():
        with open(base_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Round", "Player Choice", "Computer Choice", "Player Score", "Computer Score", "Winner"])
    
else:

    i = 1
    new_file_path = os.path.splitext(base_file_path)[0] + f"_{i}" + os.path.splitext(base_file_path)[1]

    while os.path.exists(new_file_path):
        i += 1
        new_file_path = os.path.splitext(base_file_path)[0] + f"_{i}" + os.path.splitext(base_file_path)[1]
    
    
    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
    

    def initialize_csv():
        with open(new_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Round", "Player Choice", "Computer Choice", "Player Score", "Computer Score", "Winner"])
    

def record_game_outcome(round_number, player_choice, computer_choice, player_score, computer_score, winner):
    file_path_to_use = new_file_path if os.path.exists(new_file_path) else base_file_path
    
    with open(file_path_to_use, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([round_number, player_choice, computer_choice, player_score, computer_score, winner])


def reset_game_state():
    global rounds_played, player_score_text, comp_score_text, user_label, comp_label, message

    # Reset scores
    rounds_played = 0
    player_score_text = "0"
    comp_score_text = "0"

   
    user_label.fill((0, 0, 0, 0)) 
    comp_label.fill((0, 0, 0, 0))  
    player_score.fill((0, 0, 0, 0))
    comp_score.fill((0, 0, 0, 0))
    
    message.fill((0, 0, 0, 0))  
    update_message("") 


def reveal_count_down(): 
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


    
    

pygame.init()


# server address
server = ""

# name
name = ""

WIDTH = 900
HEIGHT = 550

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors - PvP")

pygame.scrap.init()

# Fonts
font = pygame.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__),"assets/Retro Gaming.ttf")), 25)
text_font = pygame.font.Font(os.path.abspath(os.path.join(os.path.dirname(__file__),"assets/Retro Gaming.ttf")), 20)

# Load images
back_image = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/back_image.png")))

user_rock = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/user_rock.png")))
user_paper = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/user_paper.png")))
user_scissors = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/user_scissors.png")))

comp_rock = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/comp_rock.png")))
comp_paper = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/comp_paper.png")))
comp_scissors = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/comp_scissors.png")))

# Set width and height as desired
back_image = pygame.transform.scale(back_image, (50, 50))

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



rounds_played = 0
player_score_text = "0"
comp_score_text = "0"

# Message
message = pygame.Surface((450, 50), pygame.SRCALPHA)

# Back Button
back_btn_surface = pygame.Surface((50,50), pygame.SRCALPHA)
back_btn_surface.blit(back_image, (0 , 0))

back_btn = pygame.Rect(0, 0, 50, 50)


rect_width = 200
rect_height = 50

# Calculate the starting x-coordinate to center the rectangles
start_x = (screen.get_width() - (3 * rect_width + 20)) // 2
start_y = screen.get_height() - 100

border_width = 2

rock_border_rect = pygame.Rect(start_x, start_y, rect_width, rect_height)
paper_border_rect = pygame.Rect(start_x + rect_width + 10, start_y, rect_width, rect_height)
scissors_border_rect = pygame.Rect(start_x + 2 * (rect_width + 10), start_y, rect_width, rect_height)

# White fill
rock_option_rect = pygame.Rect(start_x + border_width, start_y + border_width, rect_width - 2 * border_width, rect_height - 2 * border_width)
paper_option_rect = pygame.Rect(start_x + rect_width + 10 + border_width, start_y + border_width, rect_width - 2 * border_width, rect_height - 2 * border_width)
scissors_option_rect = pygame.Rect(start_x + 2 * (rect_width + 10) + border_width, start_y + border_width, rect_width - 2 * border_width, rect_height - 2 * border_width)

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


def redrawWindow(screen, game, player):

    def player_choice():
    
        p1 = game.get_player_move(0)
        p2 = game.get_player_move(1)
        
        user_label.fill((0, 0, 0, 0))
        comp_label.fill((0, 0, 0, 0))
        

        if p2 == "Rock" and player == 1:
            user_label.blit(user_rock, (0, 0))
        elif p2 == "Rock" and player == 0:
            comp_label.blit(comp_rock, (0, 0))
        elif p2 == "Paper" and player == 1:
            user_label.blit(user_paper, (0, 0))
        elif p2 == "Paper" and player == 0:
            comp_label.blit(comp_paper, (0, 0))
        elif p2 == "Scissors" and player == 1:
            user_label.blit(user_scissors, (0, 0))
        elif p2 == "Scissors" and player == 0:
            comp_label.blit(comp_scissors, (0, 0))

        if p1 == "Rock" and player == 0:
            user_label.blit(user_rock, (0, 0))
        elif p1 == "Rock" and player == 1:
            comp_label.blit(comp_rock, (0, 0))
        elif p1 == "Paper" and player == 0:
            user_label.blit(user_paper, (0, 0))
        elif p1 == "Paper" and player == 1:
            comp_label.blit(comp_paper, (0, 0))
        elif p1 == "Scissors" and player == 0:
            user_label.blit(user_scissors, (0, 0))
        elif p1 == "Scissors" and player == 1:
            comp_label.blit(comp_scissors, (0, 0))

    def check_winner():
        p1name = game.get_player_name(0)
        p2name = game.get_player_name(1)
        p1_response_time = game.get_player_response_times(0)
        p2_response_time = game.get_player_response_times(1)
        p1_choice = game.get_player_move(0)
        p2_choice = game.get_player_move(1)

        global comp_score_text
        global player_score_text
        global rounds_played
        rounds_played += 1

        p1_choice_index = options.index(p1_choice)
        p2_choice_index = options.index(p2_choice)


        if game.winner() == -1:
            update_message("Draw!")
            if player == 0:
                record_game_outcome(rounds_played, p1name, p2name, p1_choice_index, p2_choice_index, player_score_text, comp_score_text, p1_response_time, p2_response_time, "Draw")
            
        elif (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
            update_message("You Won!")
            update_player_score()
           
        elif game.winner() == 0 and player == 1:
            update_message(f"{p1name} Won!")
            update_computer_score()
            record_game_outcome(rounds_played, p1name, p2name, p1_choice_index, p2_choice_index, comp_score_text, player_score_text, p1_response_time, p2_response_time, p1name)
        elif game.winner() == 1 and player == 0:
            update_message(f"{p2name} Won!")
            update_computer_score()
            record_game_outcome(rounds_played, p1name, p2name, p1_choice_index, p2_choice_index, player_score_text, comp_score_text, p1_response_time, p2_response_time, p2name)

        


    screen.fill((255, 255, 255))

    if not(game.connected()):
        
        text = font.render("Waiting for Player...", True, (0, 0, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
        pygame.draw.rect(screen, (255, 255, 255), back_btn)
        screen.blit(back_btn_surface, (0, 0))
        
        
    else:

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        p1name = game.get_player_name(0)
        p2name = game.get_player_name(1)
        count = game.get_countdown()
        update_message("")
        if game.bothWent():
             player_choice()
             text1 = font.render("", 1, (0,0,0))
             text2 = font.render("", 1, (0, 0, 0))
             option_countdown = font.render("", 1, (0,0,0))
             screen.blit(user_label, (100, 200))
             screen.blit(comp_label, (600, 200))
             check_winner()
        else:
            option_countdown = font.render(str(count), 1, (0,0,0))

            if game.p1Went and player == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Ready", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and player == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Ready", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if player == 1:
            screen.blit(text2, (155, 250))
            screen.blit(text1, (645, 250))
        else:
            screen.blit(text1, (155, 250))
            screen.blit(text2, (645, 250))

        #Indicator
        if player == 0:
            is_user = font.render(p1name, True, (0, 0, 0))
            is_comp = font.render(p2name, True, (0, 0, 0))
        else:
            is_user = font.render(p2name, True, (0, 0, 0))
            is_comp = font.render(p1name, True, (0, 0, 0))

        
        pygame.draw.rect(screen, (255, 255, 255), back_btn)

        screen.blit(back_btn_surface, (0, 0))
        screen.blit(is_user, (163, 80))
        screen.blit(player_score, (350, 200))  
        screen.blit(is_comp, (641, 80))
        screen.blit(comp_score, (500, 200))       
        screen.blit(option_countdown, (screen.get_width()//2 - option_countdown.get_width()//2, 30))
        
        message_rect = message.get_rect(center=(screen.get_width() // 2, 30))
        screen.blit(message, message_rect)
        

        # Draw black borders
        pygame.draw.rect(screen, (0, 0, 0), rock_border_rect, border_width)
        pygame.draw.rect(screen, (0, 0, 0), paper_border_rect, border_width)
        pygame.draw.rect(screen, (0, 0, 0), scissors_border_rect, border_width)

        # Draw white-filled rectangles
        pygame.draw.rect(screen, (255, 255, 255), rock_option_rect)
        pygame.draw.rect(screen, (255, 255, 255), paper_option_rect)
        pygame.draw.rect(screen, (255, 255, 255), scissors_option_rect)
        # Blit text onto the screen
        screen.blit(rock_text, rock_text_pos)
        screen.blit(paper_text, paper_text_pos)
        screen.blit(scissors_text, scissors_text_pos)
        

    pygame.display.update()




def input_screen():
    running = True
    clock = pygame.time.Clock()
    input_box = pygame.Rect(screen.get_width()//2 - 350//2, screen.get_height()//2 - 40//2, 350, 40)
    color = pygame.Color((0, 0, 0))
    input_text = ''
    n = Network()

    # Start with entering the server address
    phase = 'enter_server'  

    # Blinking animation variables
    cursor_visible = True
    cursor_blink_interval = 500 
    last_blink_time = 0
    cursor_delay = 1000 
    last_key_press_time = 0

    while running:
        clock.tick(60)
        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (255, 255, 255), back_btn)
        screen.blit(back_btn_surface, (0, 0))

        # Draw the input box and text
        txt_surface = font.render(input_text, True, color)
        txt_width, txt_height = txt_surface.get_size()
        text_x = input_box.x + (input_box.width - txt_width) // 2
        text_y = input_box.y + (input_box.height - txt_height) // 2
        screen.blit(txt_surface, (text_x, text_y))

        # Calculate cursor position
        cursor_x = text_x + txt_width  # X-coordinate for the cursor
        cursor_y = input_box.y + 10
        cursor_end_y = input_box.y + input_box.height - 10

        # Draw the input box
        pygame.draw.rect(screen, color, input_box, 2)

        # Blinking animation for the cursor
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time >= cursor_blink_interval and current_time - last_key_press_time >= cursor_delay:
            cursor_visible = not cursor_visible
            last_blink_time = current_time

        # Draw the cursor if it's visible
        if cursor_visible:
            pygame.draw.line(screen, color, (cursor_x, cursor_y), (cursor_x, cursor_end_y), 2)

        if phase == 'enter_server':
            prompt_text = "Please enter server address"
        elif phase == 'enter_name':
            prompt_text = "Please enter your name"
        
        text = font.render(prompt_text, True, (0, 0, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, (screen.get_height()//2 - text.get_height()//2) - 80))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_btn.collidepoint(mouse_pos):
                        running = False
                        main_game.main_menu()
            
            elif event.type == KEYDOWN:
                cursor_visible = True  # Show cursor when typing
                last_key_press_time = current_time  # Update last key press time
                if event.key == K_RETURN:
                    global server
                    global name
                    if phase == 'enter_server':

                        if input_text == "":
                            server = n.server
                        else:
                            server = input_text
                        print(server)
                        input_text = ""
                        phase = "enter_name"

                    elif phase == "enter_name":
                        name = input_text
                        
                        print("Name: ", name)
                        running = False
                        
                    
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                    
                elif event.key == K_v and (pygame.key.get_mods() & KMOD_CTRL or pygame.key.get_mods() & KMOD_META):
                    # Check for paste event (Ctrl+V or Command+V)
                    clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if clipboard_text:
                        input_text += clipboard_text.decode('utf-8', 'ignore').replace('\0', '')
                
                elif event.key == K_d and (pygame.key.get_mods() & KMOD_CTRL or pygame.key.get_mods() & KMOD_META):
                    input_text = ''

                else:
                    input_text += event.unicode


# Game loop
def main():

    while True:
    
        input_screen()

        running = True
        clock = pygame.time.Clock()
        n = Network(server)
        

        try:
            player = int(n.getP())
            n.send(f"player: {name}")
        except Exception as e:
            screen.fill((255, 255, 255))
            text = font.render("Server not found. Please try again", True, (0, 0, 0))
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
            print(e)
            pygame.display.update()
            pygame.time.delay(2000)
            continue

        while running:
            clock.tick(60)
            

            try:
                game = n.send("get")
            except:
                running = False
                print("Couldn't get game")
                break
 

            if game.bothWent():
                reveal_count_down()
                redrawWindow(screen, game, player)
                pygame.time.delay(2500)
                try:
                    game = n.send("reset")
                except:
                    running = False
                    print("Couldn't get game")
                    break
               
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    update_message("")
                    mouse_pos = pygame.mouse.get_pos()
                    if rock_option_rect.collidepoint(mouse_pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send("Rock")
                                
                        else:
                            if not game.p2Went:
                                n.send("Rock")
                
                    elif paper_option_rect.collidepoint(mouse_pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send("Paper")
                                
                        else:
                            if not game.p2Went:
                                n.send("Paper")
                                

                    elif scissors_option_rect.collidepoint(mouse_pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send("Scissors")
                                
                        else:
                            if not game.p2Went:
                                n.send("Scissors")


                    elif back_btn.collidepoint(mouse_pos):
                        running = False
                        reset_game_state()
                        n.close_connection()
                       

        
                                

            
            redrawWindow(screen, game, player)

        

    

           




if __name__ == "__main__":
    initialize_csv()
    main()
    pygame.quit()
    



    

