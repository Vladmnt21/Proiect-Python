import pygame
import sys
from Menu_Logic import handle_events, draw_buttons, draw_newgame_menu, new_game, draw_continuegame_menu, continue_game
from Game_Logic import run_game

def main():
    pygame.init()
    clock = pygame.time.Clock()
    res = (800, 640)
    screen = pygame.display.set_mode(res)

    smallfont = pygame.font.SysFont('Comic Sans', 25)
    titlefont = pygame.font.SysFont('Comic Sans', 36)

    gTitle = titlefont.render('Titlu Joc', True, (255, 255, 255))

    fileButton_x, fileButton_y, fileButton_width, fileButton_height = 80, 170, 200, 40
    nGButton_press = False
    cGbutton_press = False
    user_text = ''
    active = False
    input_rect = pygame.Rect(250, 320, 160, 40)
    error_message = None
    player_data = {
        "Player": "",
        "Lvl": 1,
        "Xp": 0,
        "HP": 100,
        "MaxHP": 100
    }
    
    game_state = "MENU"  # Start with MENU state
    nrOfSaves = 0
    
    while True:
        if game_state == "MENU":
            nGButton_press, cGbutton_press, user_text, active, error_message, game_state, player_data = handle_events(
                nGButton_press, cGbutton_press, player_data, user_text, active, input_rect, error_message, screen, smallfont, nrOfSaves, gTitle
            )
            mouse = pygame.mouse.get_pos()
            screen.fill((0,0,0))
            if not nGButton_press and not cGbutton_press:
                draw_buttons(screen, mouse, gTitle, smallfont)
            elif nGButton_press:
                draw_newgame_menu(screen, user_text, input_rect, active, error_message, smallfont, gTitle)
                
                if game_state == "GAME":  # Transition to GAME state
                    new_game(player_data, user_text)
                    
            elif cGbutton_press:
                draw_continuegame_menu(screen, gTitle, fileButton_x, fileButton_y, fileButton_width, fileButton_height, mouse, smallfont)
                
                if game_state == "GAME":
                    run_game(screen, player_data)
                    
        elif game_state == "GAME":
            run_game(screen, player_data)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
