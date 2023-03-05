from settings import *
import sys
import pygame


class App:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.state = 'start'
        self.running = True
        pygame.init()
        self.size = (800, 600)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Prisoners")

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
        pygame.quit()
        sys.exit()

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def start_draw(self):
        self.screen.fill(GREEN)
        pygame.display.update()
