import sys
import random
import gameMenu

# import ui_controls  # ui_controls.Button(...)
# or
from ui_controls import *  # Button(...)
from titleScreenScene import *


class PlayerInputScene:
    def __init__(self, screen, clock, game_state):
        self.screen = screen
        self.clock = clock
        self.game_state = game_state
        self.player_name_box = InputBox(350, 100, text="Kibbles Arcanus", is_active=True)
        self.wizard_name_box = InputBox(350, 350, text="Adam Eldritch")
        self.name_q = Label(200, 100, 300, 200, "What is your name?", image=UIResources.textbox)
        self.wiz_name_q = Label(200, 350, 400, 200, "What is your wizard's name?", image=UIResources.textbox)
        self.r_info = Label(300, 600, 300, 200, "Press Return when done", image=UIResources.textbox)

        self.labels = pygame.sprite.Group()
        self.labels.add(self.name_q)
        self.labels.add(self.r_info)

        self.inputs = pygame.sprite.Group()
        self.inputs.add(self.player_name_box)
        self.inputs.add(self.wizard_name_box)

        # enable input boxes to disable each other on click
        self.player_name_box.set_group_list(self.inputs)
        self.wizard_name_box.set_group_list(self.inputs)

    def loop(self):

        while True:
            self.screen.fill((255, 255, 255))

            # temporary bg
            self.screen.blit(UIResources.backgrounds["paper"], (0, 0))

            for event in pygame.event.get():
                for box in self.inputs:
                    box.handle_input(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_RETURN]:
                        self.game_state.player_name = self.player_name_box.get_text()
                        self.game_state.wizard_name = self.wizard_name_box.get_text()
                        return

            self.inputs.draw(self.screen)
            self.labels.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(40)
