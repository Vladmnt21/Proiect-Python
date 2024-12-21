import pygame
import sys

class Wall:
    def __init__(wall, x, y, width, height):
        wall.x = x
        wall.y = y
        wall.width = width
        wall.height = height

    def draw(wall, screen):
        pygame.draw.rect(screen, (0, 0, 255), (wall.x, wall.y, wall.width, wall.height))

def run_game(screen, player_data):
    x, y = 200, 200
    width, height = 20, 20
    vel = 2
    run = True
    
    walls = [
        Wall(785, 10, 5, 620),
        Wall(10, 625, 780, 5),
        Wall(10, 10, 5, 620),
        Wall(10, 10, 780, 5)
    ]
    
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans', 12)

    while run:
        pygame.time.delay(10)
        name = f"{player_data["Player"]} ({x},{y})"
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        next_x, next_y = x, y
        if keys[pygame.K_LEFT] and x > 0:
            next_x -= vel
        if keys[pygame.K_RIGHT] and x < screen.get_width() - width:
            next_x += vel
        if keys[pygame.K_UP] and y > 0:
            next_y -= vel
        if keys[pygame.K_DOWN] and y < screen.get_height() - height:
            next_y += vel

        collision = False
        for wall in walls:
            if next_x < wall.x + wall.width and next_x + width > wall.x and next_y < wall.y + wall.height and next_y + height > wall.y:
                collision = True
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    if keys[pygame.K_LEFT]:
                        next_x = wall.x + wall.width
                    if keys[pygame.K_RIGHT]:
                        next_x = wall.x - width

                    if keys[pygame.K_UP] and y > wall.y + wall.height:
                        next_y -= vel
                    if keys[pygame.K_DOWN] and y < wall.y - height:
                        next_y += vel
                if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    if keys[pygame.K_UP]:
                        next_y = wall.y + wall.height
                    if keys[pygame.K_DOWN]:
                        next_y = wall.y - height

                    if keys[pygame.K_LEFT] and x > wall.x + wall.width:
                        next_x -= vel
                    if keys[pygame.K_RIGHT] and x < wall.x - width:
                        next_x += vel
                break

        if not collision:
            x, y = next_x, next_y

        coords = f"{x},{y}"
        screen.fill((0, 0, 0))
        if player_data["Player"] == "Nibber":
            pygame.draw.rect(screen, (20, 55, 0), (x, y, width, height))
        else:
            pygame.draw.rect(screen,(255, 255, 0), (x, y, width, height))

        for wall in walls:
            wall.draw(screen)

        name_surface = font.render(name, True, (255, 255, 255))
        screen_width = 800
        screen_height = 640
        name_width, name_height = name_surface.get_size()
        
        if x + width // 2 + name_width // 2 > screen_width:
            name_x = screen_width - name_width // 2
        elif x + width // 2 - name_width // 2 < 0:
            name_x = name_width // 2
        else:
            name_x = x + width // 2
            
            
        name_y = y - 10
        
        name_rect = name_surface.get_rect(center=(name_x, name_y))
        screen.blit(name_surface, name_rect.topleft)
        
        pygame.display.update()

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 640))
    player_data = {"Player": "Nibber"}
    run_game(screen, player_data)
