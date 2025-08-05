import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Hareket oyun demosu")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Sky.png").convert()
ground_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/ground.png").convert()

player_surf = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_speed = 5

game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    def player_movement():
        keys = pygame.key.get_pressed()
        if keys [pygame.K_SPACE]:
            player_rect.y -= 10
        if keys [pygame.K_UP]:
            player_rect.y -= 10
        if keys [pygame.K_DOWN]:
            player_rect.y += 10
        if keys [pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys [pygame.K_LEFT]:
            player_rect.x -= player_speed

    player_movement()
    
    screen_width = 800
    if player_rect.left < 0:
        player_rect.left = 0

    if player_rect.right > screen_width:
        player_rect.right = screen_width
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

    screen.blit(player_surf,player_rect)

    pygame.display.update()
    clock.tick(60)
