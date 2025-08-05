import pygame
from sys import exit
import random

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width,screen_height))
test_font = pygame.font.Font("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/font/Pixeltype.ttf", 50)
game_name = test_font.render("Witcher 5",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = test_font.render("Press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))
clock = pygame.time.Clock()

score = 0

sky_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Sky.png").convert()
ground_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/ground.png").convert()

player_surf = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0 
player_speed = 5

player_stand = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png")
player_stand = pygame.transform.rotozoom(player_stand,0,2) 
player_stand_rect = player_stand.get_rect(center = (400,200))

snail_surf = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600,300))

game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Salyongoza deyip öldükten sonra oyunu geri başlatma mekaniği.
                game_active = True
        
        def player_movement():
            keys = pygame.key.get_pressed()
            if keys [pygame.K_SPACE]:
                player_rect.y -= 20
            if keys [pygame.K_UP]:
                player_rect.y -= 10
            if keys [pygame.K_DOWN]:
                player_rect.y += 10
            if keys [pygame.K_RIGHT]:
                player_rect.x += player_speed
            if keys [pygame.K_LEFT]:
                player_rect.x -= player_speed

    player_movement()

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        
        # score_surf = test_font.render(f"Score: {score}", False, (64,64,64))
        # score_rect = score_surf.get_rect(center = (400, 50))
        
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # screen.blit(score_surf, score_rect)

        snail_rect.x -= 5
        if snail_rect.right < 0:
            snail_rect.left = screen_width
        screen.blit(snail_surf, snail_rect) 
        
        player_gravity += 1
        player_rect.y += player_gravity
        
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
            player_gravity = 0

        screen.blit(player_surf, player_rect) 

        if player_rect.colliderect(snail_rect):
            game_active = False
            snail_rect.left = screen_width + random.randint(100, 300) 

    else:              
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f"Your Score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60) 