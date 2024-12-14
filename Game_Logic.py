import pygame
import sys

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

def run_game(screen, player_data):
    x, y = 200, 200
    width, height = 20, 20
    vel = 2
    run = True
    name = player_data["Player"]
    
    walls = [
        #Wall(785, 10, 5, 620),
        Wall(10, 625, 780, 5),
        Wall(10, 10, 5, 620),
        Wall(10, 10, 780, 5)
    ]
    
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans', 20)

    while run:
        pygame.time.delay(10)

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

        screen.fill((0, 0, 0))
        if player_data["Player"] == "Nibber":
            pygame.draw.rect(screen, (20, 55, 0), (x, y, width, height))
        else:
            pygame.draw.rect(screen,(255, 255, 0), (x, y, width, height))

        for wall in walls:
            wall.draw(screen)

        name_surface = font.render(name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(x + width // 2, y - 25))
        screen.blit(name_surface, name_rect.topleft)

        pygame.display.update()

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 640))
    player_data = {"Player": "Nibber"}
    run_game(screen, player_data)
