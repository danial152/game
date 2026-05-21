import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)

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
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
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

    def render(self):
        self.screen.fill(BLACK)
        if self.state == "MENU":
            self.render_menu()
        elif self.state == "SETTINGS":
            self.render_settings()
        pygame.display.flip()
    def render_menu(self):
        title_text = self.font.render("MAIN MENU", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))
        start_color = RED if self.menu_index == 0 else WHITE
        settings_color = RED if self.menu_index == 1 else WHITE

        start_text = self.font.render("Start Game", True, start_color)
        self.screen.blit(start_text, (SCREEN_WIDTH / 2 - start_text.get_width() / 2, 230))

        settings_text = self.font.render("Settings", True, settings_color)
        self.screen.blit(settings_text, (SCREEN_WIDTH / 2 - settings_text.get_width() / 2, 310))
    def render_settings(self):
        title_text = self.font.render("SETTINGS", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 100))

        info_text = self.small_font.render("placeholder", True, WHITE)
        self.screen.blit(info_text, (SCREEN_WIDTH / 2 - info_text.get_width() / 2, 220))

        info_text2 = self.small_font.render("placeholder", True, WHITE)
        self.screen.blit(info_text2, (SCREEN_WIDTH / 2 - info_text2.get_width() / 2, 270))



Game().run()
