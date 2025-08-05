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
        self.player_jump = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/jump.png").convert_alpha() 

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.speed = 7.5

        self.jump_sound = pygame.mixer.Sound("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/audio/jump.mp3")
        self.jump_sound.set_volume(0.1)

    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0    

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


    def animation_state(self):
        if self.rect.bottom < 300: 
            self.image = self.player_jump
        else: 
            self.player_index += 0.1 
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.player_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,level):
        super().__init__()
        fly_1 = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Fly/Fly1.png").convert_alpha()
        fly_2 = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Fly/Fly2.png").convert_alpha()
        self.frames = [fly_1,fly_2]
        random_y_pos = random.randint(150,275)
        self.animation_index = 0
        self.passed_player = False
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(WIDTH+50,WIDTH+175),random_y_pos))

        min_speed = 3 +(level - 1)*1
        max_speed = 7 +(level - 1)*1
        self.speed = random.randint(min_speed,max_speed)

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
    score_surf = test_font.render(f"Score: {int(score)}",True,(255,255,128))
    score_rect = score_surf.get_rect(center = (WIDTH/2, 50))
    screen.blit(score_surf,score_rect)

def display_level():
    global current_level
    level_surf = test_font.render(f"Level: {int(current_level)}",True,(255,0,0))
    level_rect = level_surf.get_rect(center = (WIDTH/2, 375))
    screen.blit(level_surf,level_rect)


pygame.init()
oyun_ismi = pygame.display.set_caption("Seviye Atlama")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sky_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Sky.png").convert()
ground_surface = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/ground.png").convert()
test_font = pygame.font.Font("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/font/Pixeltype.ttf", 50)
player_stand = pygame.image.load("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/graphics/Player/player_stand.png")
player_stand = pygame.transform.rotozoom(player_stand,0,2) 
player_stand_rect = player_stand.get_rect(center = (400,200))

bg_Music = pygame.mixer.Sound("C:/Kodlama/witcher5_demo/UltimatePygameIntro-main/audio/music.wav")
bg_Music.play(loops = -1)
bg_Music.set_volume(0.1)

game_name = test_font.render("Witcher 5",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render("Press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

game_active = False
score = 0
current_level = 1
current_enemy_spawn_interval = 1500
level_up_scores = {
    1: 5,
    2: 15,
    3: 30,
    4: 50,
}

player = pygame.sprite.GroupSingle()
player.add(Player())

enemy = pygame.sprite.Group()

enemy_timer = pygame.USEREVENT + 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:          
            if event.type == enemy_timer: 
                enemy.add(Enemy(current_level))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score = 0
                current_level = 1 
                current_enemy_spawn_interval = 1500
                enemy.empty() 
                pygame.time.set_timer(enemy_timer, current_enemy_spawn_interval) 
    
    if game_active:
        collided_enemies = pygame.sprite.spritecollide(player.sprite,enemy,True)
        if collided_enemies:
            game_active = False
            pygame.time.set_timer(enemy_timer,0)

        for current_enemy in enemy:
            if current_enemy.rect.right < player.sprite.rect.left and not current_enemy.passed_player:
                score += 1
                current_enemy.passed_player = True

        if current_level in level_up_scores:
            next_level_score_target = level_up_scores[current_level]

            if score >= next_level_score_target:
                current_level += 1 
                print(f"TEBRİKLER! {current_level} Seviye Oldun!") 
                current_enemy_spawn_interval = max(500, current_enemy_spawn_interval - 100) 
                pygame.time.set_timer(enemy_timer, current_enemy_spawn_interval)
                print(f"Yeni düşman oluşum aralığı: {current_enemy_spawn_interval}ms")

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        player.draw(screen)
        player.update()

        enemy.draw(screen)
        enemy.update()

        display_level()
        display_score()

    else: 
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)

        else:
            # time_up_message = test_font.render(f"Time Up!", False, (111, 196, 169))
            # time_up_message_rect = time_up_message.get_rect(center=(400,330))
            # screen.blit(time_up_message, time_up_message_rect)

            score_message = test_font.render(f"Your Score: {score}", False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 380))
            screen.blit(score_message,score_message_rect)

            final_score_message = test_font.render(f"Your Level: {current_level}", False, (111, 196, 169))
            final_score_message_rect = final_score_message.get_rect(center=(400, 330))
            screen.blit(final_score_message,final_score_message_rect)

    pygame.display.update()
    clock.tick(60)
