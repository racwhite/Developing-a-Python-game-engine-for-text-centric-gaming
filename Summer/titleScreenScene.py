from ui_controls import *
import sys


class TitleScreenScene:
    def __init__(self, screen, clock, game_state):
        self.screen = screen
        self.clock = clock
        self.game_state = game_state
        self.buttons = pygame.sprite.Group()
        self.f_new_game = False
        self.f_quit_game = False
        self.f_load_game = False
        # self.test_input = InputBox()

        self.newGameButton = Button(500, 100, 70, 70, self.new_game, text="new game")
        self.quitButton = Button(500, 200, 70, 70, self.quit_game, text="quit")
        self.loadButton = Button(500, 300, 70, 70, self.load_game, text="load")

        self.buttons.add(self.newGameButton)
        self.buttons.add(self.quitButton)
        self.buttons.add(self.loadButton)

    def new_game(self):
        self.f_new_game = True

    def quit_game(self):
        self.f_quit_game = True

    def load_game(self):
        self.f_load_game = True

    def loop(self):
        self.f_new_game = False
        self.f_quit_game = False
        self.f_load_game = False
        while True:
            self.screen.fill((255, 255, 255))

            # temporary bg
            self.screen.blit(UIResources.backgrounds["city_background"], (0, 0))

            for event in pygame.event.get():
                for button in self.buttons:
                    button.handle_event(event)

                # self.test_input.handle_input(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.buttons.draw(self.screen)
            # self.screen.blit(self.test_input.get_surface(), (100, 100))

            if self.f_new_game or self.f_quit_game or self.f_load_game:
                self.buttons.clear(self.screen, UIResources.backgrounds["city_background"])
                if self.f_new_game:
                    return "new_game", "", ""
                elif self.f_quit_game:
                    return "quit", "", ""
                elif self.f_load_game:
                    return "load", "", ""

            pygame.display.flip()
            self.clock.tick(40)