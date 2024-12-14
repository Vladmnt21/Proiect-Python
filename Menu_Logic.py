import pygame
import json
import sys

#cod

# Global variables
nGButton_x, nGButton_y, nGButton_width, nGButton_height = 250, 180, 140, 40
cGButton_x, cGButton_y, cGButton_width, cGButton_height = 220, 240, 200, 40
eButton_x, eButton_y, eButton_width, eButton_height = 270, 300, 100, 40
saveButton_x, saveButton_y, saveButton_width, saveButton_height = 350, 200, 100, 40
text_color = (255, 255, 255)
color_butHover = (170, 170, 170)
color_but = (100, 100, 100)

def new_game(data, filename):
    data["Player"] = filename
    with open(f'Saves/{filename}.json', 'w') as file:
        json.dump(data, file)

def draw_buttons(screen, mouse, gTitle, smallfont):
    draw_button(screen, nGButton_x, nGButton_y, nGButton_width, nGButton_height, 'New Game', mouse, smallfont)
    draw_button(screen, cGButton_x, cGButton_y, cGButton_width, cGButton_height, 'Continue Game', mouse, smallfont)
    draw_button(screen, eButton_x, eButton_y, eButton_width, eButton_height, 'Quit', mouse, smallfont)
    screen.blit(gTitle, (240, 50))

def draw_button(screen, x, y, width, height, text, mouse, smallfont):
    if x <= mouse[0] <= x + width and y <= mouse[1] <= y + height:
        pygame.draw.rect(screen, color_butHover, [x, y, width, height])
    else:
        pygame.draw.rect(screen, color_but, [x, y, width, height])
    
    text_surf = smallfont.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surf, text_rect)

def draw_newgame_menu(screen, user_text, input_rect, active, error_message, smallfont, gTitle):
    color = color_butHover if active else color_but
    
    pygame.draw.rect(screen, color, input_rect)
    
    text_surface = smallfont.render(user_text, True, text_color)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    
    pygame.draw.rect(screen, color_but, (saveButton_x, saveButton_y, saveButton_width, saveButton_height)) 
    save_text = smallfont.render("Start", True, text_color)
    save_text_rect = save_text.get_rect(center=(saveButton_x + saveButton_width / 2, saveButton_y + saveButton_height / 2))
    screen.blit(save_text, save_text_rect)
    screen.blit(gTitle, (240, 50))

    if error_message:
        error_surface = smallfont.render(error_message, True, (255, 255, 255))
        error_rect = error_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
        screen.blit(error_surface, error_rect)

def handle_events(nGButton_press, player_data, user_text, active, input_rect, error_message, screen, smallfont):
    game_state = "MENU"  # Default to MENU state
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if eButton_x <= mouse[0] <= eButton_x + eButton_width and eButton_y <= mouse[1] <= eButton_y + eButton_height and not nGButton_press:
                pygame.quit()
                sys.exit()
            if nGButton_x <= mouse[0] <= nGButton_x + nGButton_width and nGButton_y <= mouse[1] <= nGButton_y + nGButton_height and not nGButton_press:
                nGButton_press = True
                print("New Game!")
            if cGButton_x <= mouse[0] <= cGButton_x + cGButton_width and cGButton_y <= mouse[1] <= cGButton_y + cGButton_height and not nGButton_press:
                print("Continue game button pressed!")
            if nGButton_press:
                if input_rect.collidepoint(ev.pos):
                    active = True
                else:
                    active = False
            if saveButton_x <= mouse[0] <= saveButton_x + saveButton_width and saveButton_y <= mouse[1] <= saveButton_y + saveButton_height:
                if len(user_text) > 3:
                    new_game(player_data, user_text)
                    print(f"New save file {user_text}.json!")
                    error_message = None
                    game_state = "GAME"
                else:
                    error_message = "Minim 4 caractere la nume!" 
        if ev.type == pygame.KEYDOWN:
            if active:
                # Check for backspace
                if ev.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += ev.unicode

    return nGButton_press, user_text, active, error_message, game_state
