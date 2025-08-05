import pygame
from sys import exit

pygame.init

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("İlk oyun ekran demosu ")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    


