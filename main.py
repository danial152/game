import pygame
import sys
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLACK = (0,0,0)
colors = {
    "WHITE": (255, 255, 255),
    "GRAY": (100, 100, 100),
    "BLUE": (50, 50, 255),
    "GREEN": (50, 255, 50),
    "RED": (255, 50, 50)
}

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(colors["WHITE"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0
        self.speed = 5
        self.gravity = 0.7
        self.jump_power = -16
        self.is_grounded = False
        self.dash_frames = 0
        self.recovery_frames = 0
        # right or left
        self.dash_direction = "right"
    def update(self, platforms):
        if self.recovery_frames > 0:
            self.recovery_frames -= 1
        if self.dash_frames > 0:
            self.dash_frames -= 1
            if self.dash_direction == "right": self.change_x = 30
            elif self.dash_direction == "left": self.change_x = -30
            self.gravity = 0
        if self.dash_frames == 0:
            self.gravity = 0.7

        if self.recovery_frames == 0:
            self.image.fill(colors["RED"])
        else:
            self.image.fill(colors["WHITE"])
        self.change_y += self.gravity
        self.rect.x += self.change_x
        self.horizontal_collision(platforms)
        self.rect.y += self.change_y
        self.vertical_collision(platforms)
        for platform in platforms:
            if ((platform.rect.top - self.rect.bottom > -5) and (platform.rect.top - self.rect.bottom < 5) and self.is_grounded):
                self.rect.bottom = platform.rect.top
    def horizontal_collision(self, platforms):
        collide_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collide_list:
            if self.change_x > 0 and self.change_y == 0:
                self.rect.right = platform.rect.left
            elif self.change_x < 0 and self.change_y == 0:
                self.rect.left = platform.rect.right
    def vertical_collision(self, platforms):
        collide_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collide_list:
            if self.change_y > 0:  # Falling down
                self.rect.bottom = platform.rect.top
                self.change_y = 0
                self.is_grounded = True
    def jump(self):
        if self.is_grounded:
            self.is_grounded = False
            self.change_y = self.jump_power
    def dash(self):
        if self.change_x != 0:
            if self.change_x > 0:
                self.dash_direction = "right"
            else:
                self.dash_direction = "left"
            self.dash_frames = 5
            self.recovery_frames = 60
            self.gravity = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(random.choice(list(colors.values())))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_y = 3
    def update(self):
        self.rect.y += self.change_y
    def spawn():
        width = random.randint(30,200)
        x = random.randint(100,600-width)
        height = random.randint(10,50)
        return Platform(x, 0, width, height)

class Eye(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(random.choice(list(colors.values())))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target = target
        self.speed = 5
    def update(self):
        if self.target:
            vect = pygame.math.Vector2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
            vect.normalize()
            vect.scale_to_length(self.speed)
            self.rect.move_ip(vect)
            if pygame.sprite.collide_rect(self, self.target):
                if self.target.dash_frames > 0:
                    self.kill()
                    self.target = None
                    self.rect.x = -1000
                else:
                    self.target.kill()
                    self.target = None

# main game
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("my Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 24)
        # 'MENU', 'SETTINGS', 'PLAY'
        self.state = "MENU"
        self.running = True
        self.menu_index = 0
        self.player_score = 0

        #init
        self.player = Player(400, 0)
        self.eye = Eye(100,0, self.player)
        self.platforms = pygame.sprite.Group()
        self.platform = Platform(300, 100, 200, 10)
        self.platforms.add(self.platform)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.platform,self.eye)

        self.SPAWN_EVENT = pygame.USEREVENT + 1
        self.SPAWN_ENEMY_EVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWN_EVENT, 1000)
        pygame.time.set_timer(self.SPAWN_ENEMY_EVENT, 5000)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    self.handle_menu_events(event)
                elif self.state == "SETTINGS":
                    self.handle_settings_events(event)
                elif self.state == "PLAY":
                    self.handle_play_events(event)
            if event.type == self.SPAWN_EVENT and self.state == "PLAY":
                self.platform = Platform.spawn()
                self.platforms.add(self.platform)
                self.all_sprites.add(self.platform)
            if event.type == self.SPAWN_ENEMY_EVENT and self.state == "PLAY":
                self.eye = Eye(random.randint(0,800),-100, self.player)
                self.all_sprites.add(self.eye)

    def handle_menu_events(self, event):
        if event.key == pygame.K_UP:
            self.menu_index = (self.menu_index - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.menu_index = (self.menu_index + 1) % 2
        elif event.key == pygame.K_RETURN:
            if self.menu_index == 0:
                self.state = "PLAY"
            elif self.menu_index == 1:
                self.state = "SETTINGS"
    def handle_settings_events(self, event):
        if event.key == pygame.K_RETURN:
            self.state = "MENU"
    def handle_play_events(self, event):
        if event.key == pygame.K_w:
            self.player.jump()
        if event.key == pygame.K_LSHIFT:
            if self.player.recovery_frames == 0:
                self.player.dash()
        elif event.key == pygame.K_ESCAPE:
                self.state = "MENU"
    def update(self):
        self.screen.fill(BLACK)
        if self.state == "MENU":
            self.menu()
        elif self.state == "SETTINGS":
            self.settings()
        elif self.state == "PLAY":
            self.play()
        pygame.display.flip()
    def menu(self):
        title_text = self.font.render("MAIN MENU", True, colors["WHITE"])
        self.screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))
        start_color = colors["RED"] if self.menu_index == 0 else colors["WHITE"]
        settings_color = colors["RED"] if self.menu_index == 1 else colors["WHITE"]

        start_text = self.font.render("Start Game", True, start_color)
        self.screen.blit(start_text, (SCREEN_WIDTH / 2 - start_text.get_width() / 2, 230))

        settings_text = self.font.render("Settings", True, settings_color)
        self.screen.blit(settings_text, (SCREEN_WIDTH / 2 - settings_text.get_width() / 2, 310))
    def settings(self):
        title_text = self.font.render("SETTINGS", True, colors["WHITE"])
        self.screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))

        info_text = self.small_font.render("placeholder", True, colors["WHITE"])
        self.screen.blit(info_text, (SCREEN_WIDTH / 2 - info_text.get_width() / 2, 220))

        info_text2 = self.small_font.render("placeholder", True, colors["WHITE"])
        self.screen.blit(info_text2, (SCREEN_WIDTH / 2 - info_text2.get_width() / 2, 270))
    def play(self):
        # Render all entities
        self.player.update(self.platforms)
        self.platforms.update()
        self.eye.update()
        for platform in list(self.platforms):
            if platform.rect.top > SCREEN_HEIGHT:
                platform.kill()
                self.player_score += 1
        pressed = pygame.key.get_pressed()
        self.player.change_x = 0
        if pressed and self.player.dash_frames == 0:
            if pressed[pygame.K_a]:
                self.player.change_x = -self.player.speed
            elif pressed[pygame.K_d]:
                self.player.change_x = self.player.speed

        # Helper text overlay
        self.all_sprites.draw(self.screen)
        esc_text = self.small_font.render(f"Your score is {self.player_score}" , True, colors["WHITE"])
        self.screen.blit(esc_text, (10, 10))


Game().run()
