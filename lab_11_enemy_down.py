import pygame
from sys import exit
import random

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Düşen kare projesi")
clock = pygame.time.Clock()

enemy_surf = pygame.Surface((50,50))
enemy_surf.fill("Red")

enemy_x_pos = random.randint(0, screen_width - enemy_surf.get_width())
enemy_y_pos = -50
enemy_rect = enemy_surf.get_rect(center=(enemy_x_pos, enemy_y_pos))

enemy_speed = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    enemy_rect.y += enemy_speed

    if enemy_rect.top > screen_height:
        enemy_rect.x = random.randint(0, screen_width - enemy_surf.get_width())
        enemy_rect.y = -50

    screen.fill("lightblue")

    screen.blit(enemy_surf,enemy_rect)

    pygame.display.update()

    clock.tick(60)