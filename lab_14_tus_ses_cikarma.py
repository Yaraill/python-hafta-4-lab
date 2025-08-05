import pygame
from sys import exit

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Tuşa Basınca Ses Çıkarma")
clock = pygame.time.Clock()
test_font = pygame.font.Font("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/font/Pixeltype.ttf", 50)

score = 0 

sky_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Sky.png").convert()
ground_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/ground.png").convert()

player_surf = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_speed = 10

key_sound = pygame.mixer.Sound("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/audio/jump.mp3")
key_sound.set_volume(0.2) 

# snail_surf = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/snail/snail1.png").convert_alpha()
# snail_rect = snail_surf.get_rect(midbottom = (600,300))

game_active = True

def player_movement():
    global player_rect, player_speed 

    keys = pygame.key.get_pressed()
    
    if keys [pygame.K_SPACE]:
        player_rect.y -= player_speed
    if keys [pygame.K_UP]:
        player_rect.y -= player_speed
    if keys [pygame.K_DOWN]:
        player_rect.y += player_speed
    if keys [pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys [pygame.K_LEFT]:
        player_rect.x -= player_speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
                key_sound.play() 

    player_movement()

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        # score_surf = test_font.render(f"Score: {score}", False, (64,64,64))
        # score_rect = score_surf.get_rect(center = (400, 50))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # screen.blit(score_surf, score_rect)
        
        # snail_rect.x -= 5
        # if snail_rect.right < 0:
        #    snail_rect.left = screen_width
        # screen.blit(snail_surf, snail_rect) 
        
        if player_rect.bottom >= screen_height: 
            player_rect.bottom = screen_height
        if player_rect.top <= 0: 
            player_rect.top = 0
        if player_rect.left <= 0: 
            player_rect.left = 0
        if player_rect.right >= screen_width: 
            player_rect.right = screen_width

        screen.blit(player_surf, player_rect) 
        
        # if player_rect.colliderect(snail_rect):
        #    print("Düşmana Çarpıldı")
        #    score += 1 
        #    snail_rect.left = screen_width + 100 

    pygame.display.update()
    clock.tick(60)