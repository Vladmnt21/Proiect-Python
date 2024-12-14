import pygame
import sys
from Menu_Logic import handle_events, draw_buttons, draw_newgame_menu, new_game
from Game_Logic import run_game

def main():
    pygame.init()
    clock = pygame.time.Clock()
    res = (800, 640)
    screen = pygame.display.set_mode(res)

    smallfont = pygame.font.SysFont('Comic Sans', 25)
    titlefont = pygame.font.SysFont('Comic Sans', 36)
    background = pygame.image.load('Sprites/Background/Background.png')

    gTitle = titlefont.render('Titlu Joc', True, (255, 255, 255))

    nGButton_press = False
    user_text = ''
    active = False
    input_rect = pygame.Rect(200, 200, 140, 40)
    error_message = None
    player_data = {
        "Player": "",
        "Lvl": 1,
        "Xp": 0,
        "HP": 100,
        "MaxHP": 100
    }
    
    game_state = "MENU"  # Start with MENU state
    
    while True:
        if game_state == "MENU":
            nGButton_press, user_text, active, error_message, game_state = handle_events(
                nGButton_press, player_data, user_text, active, input_rect, error_message, screen, smallfont
            )
            mouse = pygame.mouse.get_pos()
            screen.blit(background, (0, 0))
            if not nGButton_press:
                draw_buttons(screen, mouse, gTitle, smallfont)
            else:
                draw_newgame_menu(screen, user_text, input_rect, active, error_message, smallfont, gTitle)
                
                if game_state == "GAME":  # Transition to GAME state
                    new_game(player_data, user_text)
        elif game_state == "GAME":
            run_game(screen, player_data)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
