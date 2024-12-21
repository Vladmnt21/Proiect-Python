import pygame
import json
import sys
import os

# Global variables
nGButton_x, nGButton_y, nGButton_width, nGButton_height = 330, 240, 140, 40
cGButton_x, cGButton_y, cGButton_width, cGButton_height = 300, 320, 200, 40
eButton_x, eButton_y, eButton_width, eButton_height = 350, 400, 100, 40
saveButton_x, saveButton_y, saveButton_width, saveButton_height = 420, 320, 100, 40
fileButton_x, fileButton_y, fileButton_width, fileButton_height = 300, 240, 200, 40
eol = False
nr_sav = 0
# fileButton = (300, 240, 200, 40)
text_color = (255, 255, 255)
color_butHover = (170, 170, 170)
color_but = (100, 100, 100)

def new_game(data, filename):
    data["Player"] = filename
    with open(f'Saves/{filename}.json', 'w') as file:
        json.dump(data, file)
        
def continue_game(data):
    pass
    
def draw_buttons(screen, mouse, gTitle, smallfont):
    draw_button(screen, nGButton_x, nGButton_y, nGButton_width, nGButton_height, 'New Game', mouse, smallfont)
    draw_button(screen, cGButton_x, cGButton_y, cGButton_width, cGButton_height, 'Continue Game', mouse, smallfont)
    draw_button(screen, eButton_x, eButton_y, eButton_width, eButton_height, 'Quit', mouse, smallfont)
    screen.blit(gTitle, (330, 50))

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
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y))
    
    pygame.draw.rect(screen, color_but, (saveButton_x, saveButton_y, saveButton_width, saveButton_height)) 
    save_text = smallfont.render("Start", True, text_color)
    save_text_rect = save_text.get_rect(center=(saveButton_x + saveButton_width / 2, saveButton_y + saveButton_height / 2))
    screen.blit(save_text, save_text_rect)
    screen.blit(gTitle, (330, 50))

    if error_message:
        error_surface = smallfont.render(error_message, True, (255, 255, 255))
        error_rect = error_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
        screen.blit(error_surface, error_rect)

def draw_continuegame_menu(screen, gTitle, fileButton_x, fileButton_y, fileButton_width, fileButton_height, mouse, smallfont, nrOfSaves):
    saves_path = "Saves/"
    save_list = []
    
    for saveName in os.listdir(saves_path):
        if saveName.endswith(".json"):
            save_path = os.path.join(saves_path, saveName)
            
            with open(save_path, 'r') as file:
                save = json.load(file)
                save_list.append(save)

    global eol
    global nr_sav

    for save in save_list:
        if not eol:
            nr_sav += 1
        draw_button(screen, fileButton_x, fileButton_y, fileButton_width, fileButton_height, save["Player"], mouse, smallfont)
        fileButton_y += 70
    
    eol = True
    
    screen.blit(gTitle, (330, 50))
    return nr_sav


def handle_events(nGButton_press, cGbutton_press, player_data, user_text, active, input_rect, error_message, screen, smallfont, nrOfSaves, gTitle):
    game_state = "MENU"  # Default to MENU state
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if not nGButton_press and not cGbutton_press:
                if eButton_x <= mouse[0] <= eButton_x + eButton_width and eButton_y <= mouse[1] <= eButton_y + eButton_height:
                    pygame.quit()
                    sys.exit()
                if nGButton_x <= mouse[0] <= nGButton_x + nGButton_width and nGButton_y <= mouse[1] <= nGButton_y + nGButton_height:
                    nGButton_press = True
                    print("New Game!")
                if cGButton_x <= mouse[0] <= cGButton_x + cGButton_width and cGButton_y <= mouse[1] <= cGButton_y + cGButton_height:
                    cGbutton_press = True
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
            if cGbutton_press:
                nrOfSaves = draw_continuegame_menu(screen, gTitle, fileButton_x, fileButton_y, fileButton_width, fileButton_height, mouse, smallfont, nrOfSaves)
                print(nrOfSaves)
        if ev.type == pygame.KEYDOWN:
            if active:
                # Check for backspace
                if ev.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += ev.unicode

    return nGButton_press, cGbutton_press, user_text, active, error_message, game_state, player_data
