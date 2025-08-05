import pygame
from sys import exit
import random

WIDTH = 800
HEIGHT = 400

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_walk_1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.speed = 5
        self.gravity = 10

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        
    def update(self):
        self.player_input()
        self.apply_gravity() 


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Fly/Fly1.png").convert_alpha(),
            pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Fly/Fly2.png").convert_alpha()
        ]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.speed = 4 
        
        random_y_pos = random.randint(150, 275) 
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH + 50, WIDTH + 200), random_y_pos))
        self.passed_player = False

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.right <= 0:
            self.kill()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("3 Menülü Oyun")

test_font = pygame.font.Font("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/font/Pixeltype.ttf", 50)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Sky.png").convert()
ground_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/ground.png").convert()

player_stand = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) 
player_stand_rect = player_stand.get_rect(center = (WIDTH / 2, HEIGHT / 2)) 

game_title_text = test_font.render("Witcher 5",False,(111,196,169))
game_title_rect = game_title_text.get_rect(center = (WIDTH / 2, 80)) 

start_message_1 = test_font.render("Ziplamak icin SPACE, YON tuslari ile hareket!", False, (111,196,169))
start_message_1_rect = start_message_1.get_rect(center = (WIDTH / 2, 300)) 

start_message_2 = test_font.render("Baslamak icin SPACE'e bas", False, (111,196,169))
start_message_2_rect = start_message_2.get_rect(center = (WIDTH / 2, 350)) 

game_active = False 
score = 0 

OBSTACLE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_TIMER, 1500) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == OBSTACLE_TIMER:
                obstacle_group.add(Obstacle())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player.sprite.rect.midbottom = (100, 300) 
                score = 0 
                obstacle_group.empty() 

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface,(0,300))

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        for obstacle in obstacle_group:
            if obstacle.rect.right < player.sprite.rect.left and not obstacle.passed_player:
                score += 1
                obstacle.passed_player = True
        
        score_surf = test_font.render(f"Skor: {score}", True, "Red")
        score_rect = score_surf.get_rect(center=(WIDTH / 2, 50)) 
        screen.blit(score_surf, score_rect)

        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): 
            game_active = False
            
    else: 
        screen.fill((94,129,162)) 

        player_stand_rect.center = (WIDTH / 2, HEIGHT / 2 - 50) 
        screen.blit(player_stand, player_stand_rect)
       
        game_title_rect.center = (WIDTH / 2, 40) 
        screen.blit(game_title_text, game_title_rect)
        
        if score > 0: 
            game_over_text = test_font.render("OYUN BITTI!", False, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, player_stand_rect.bottom + 30))
            screen.blit(game_over_text, game_over_rect)

            final_score_text = test_font.render(f"Skorun: {score}", False, (111, 196, 169))
            final_score_rect = final_score_text.get_rect(center=(WIDTH / 2, game_over_rect.bottom + 20)) 
            screen.blit(final_score_text, final_score_rect)
            
            restart_message_text = test_font.render("Yeniden Baslamak icin SPACE'e bas", False, (111, 196, 169))
            restart_message_rect = restart_message_text.get_rect(center=(WIDTH / 2, final_score_rect.bottom + 20)) 
            screen.blit(restart_message_text, restart_message_rect)

        else: 
            screen.blit(start_message_1, start_message_1_rect)
            screen.blit(start_message_2, start_message_2_rect)

    pygame.display.update()
    clock.tick(60)