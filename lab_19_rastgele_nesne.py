import pygame
from sys import exit
import random

WIDTH = 800
HEIGHT = 400

pygame.init()
game_name = pygame.display.set_caption("Rastgele Nesne Düşme Oyunu")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

enemy_surf = pygame.Surface((50,50))
enemy_surf.fill("Yellow") 

enemy_x_pos = random.randint(0,WIDTH-enemy_surf.get_width())
enemy_y_pos = -50
enemy_rect = enemy_surf.get_rect(center=(enemy_x_pos,enemy_y_pos))

enemy_speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    enemy_rect.y = enemy_speed # Karenin düşmesi için += yap

    if enemy_rect.top > HEIGHT:
        enemy_rect.x = random.randint(0, WIDTH - enemy_surf.get_width())
        enemy_rect.y = -50
    
    screen.fill("red")

    screen.blit(enemy_surf,enemy_rect)
    pygame.display.update()
    clock.tick(60)
