import pygame
from sys import exit
import random

WIDTH = 800
HEIGHT = 400

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        # self.passed_player = False
        self.player_jump = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/jump.png").convert_alpha() 

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/audio/jump.mp3")
        self.jump_sound.set_volume(0.2)

    def player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_UP] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_DOWN]:
            self.rect.y += 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_movement()
        self.player_gravity()
        self.player_animation()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fly_1 = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Fly/Fly1.png").convert_alpha()
        fly_2 = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Fly/Fly2.png").convert_alpha()
        self.frames = [fly_1,fly_2]
        random_y_pos = random.randint(150,275)
        self.animation_index = 0
        self.passed_player = False
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(WIDTH+50,WIDTH+200),random_y_pos))
        self.speed = random.randint(4,8)

    def enemy_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.right <= 0:
            self.kill()

    def update(self):
        self.enemy_animation()
        self.rect.x -= self.speed
        self.destroy()

def display_score():
    global score
    score_surf = test_font.render(f"Score: {score}", True, (128,128,128))
    score_rect = score_surf.get_rect(center = (100, 50))
    screen.blit(score_surf, score_rect)

def display_timer():
    global game_time_left
    timer_surf = test_font.render(f"Time: {int(game_time_left)}", True, (128,128,128))
    timer_rect = timer_surf.get_rect(center = (700, 50))
    screen.blit(timer_surf, timer_rect)

pygame.init()
game_name = pygame.display.set_caption("Zaman Geri Sayımı")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
test_font = pygame.font.Font("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/font/Pixeltype.ttf", 50)

score = 0
game_time_left = 60
game_active = False

sky_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Sky.png").convert()
ground_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/ground.png").convert()

bg_Music = pygame.mixer.Sound("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/audio/music.wav")
bg_Music.play(loops = -1)
bg_Music.set_volume(0.1)

player = pygame.sprite.GroupSingle()
player.add(Player())

enemy = pygame.sprite.Group()

player_stand = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png")
player_stand = pygame.transform.rotozoom(player_stand,0,2) 
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render("Witcher 5",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render("Press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

obstacle_timer = pygame.USEREVENT + 1
GAME_OVER_TIME = pygame.USEREVENT + 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == GAME_OVER_TIME:
            game_active = False
            pygame.time.set_timer(obstacle_timer, 0)
            
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.rect.bottom >= 300:
                    player.sprite.gravity = -20
            
            if event.type == obstacle_timer: 
                enemy.add(Enemy()) 

        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score = 0
                start_time = int(pygame.time.get_ticks() / 1000)
                pygame.time.set_timer(obstacle_timer,1500)
                # pygame.time.set_timer(GAME_OVER_TIME,60000)
                enemy.empty()

    if game_active:
        current_time_in_seconds = (pygame.time.get_ticks()/1000) - start_time

        game_time_left = 60 - int(current_time_in_seconds)

        if game_time_left <= 0:
            game_time_left = 0
            pygame.event.post(pygame.event.Event(GAME_OVER_TIME))

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300)) 

        player.draw(screen)
        player.update() 

        enemy.draw(screen)
        enemy.update() 

        collided_enemies = pygame.sprite.spritecollide(player.sprite, enemy, True) 
        if collided_enemies: 
            score -= 1

        for current_enemy in enemy:
            if current_enemy.rect.right < player.sprite.rect.left and not current_enemy.passed_player:
                score += 1
                current_enemy.passed_player = True
        
        display_score() 
        display_timer()
    else: 
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)

        elif game_time_left <= 0:
            time_up_message = test_font.render(f"Time Up!", False, (111, 196, 169))
            time_up_message_rect = time_up_message.get_rect(center=(400,330))
            screen.blit(time_up_message, time_up_message_rect)

            score_message = test_font.render(f"Your Score: {score}", False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 380))
            screen.blit(score_message,score_message_rect)

        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)