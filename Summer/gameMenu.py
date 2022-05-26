from ui_controls import *
import sys
import pygame


class GameMenu:
    def __init__(self, screen, clock, _game_state):
        self.screen = screen
        self.game_state = _game_state
        self.clock = clock
        self.resume_button = None
        self.save_button = None
        self.load_button = None
        self.quit_button = None
        self.return_button = None
        self.title_button = None
        self.quit_yes = None
        self.quit_no = None
        self.load_yes = None
        self.load_no = None
        self.title_yes = None
        self.title_no = None
        self.save_yes = None
        self.save_no = None
        self.quit_confirm_label = Label(300, 200, 250, 100, text="Are you sure you want to quit?")
        self.load_confirm_label = Label(300, 200, 200, 100, text="Load game?")
        self.title_confirm_label = Label(300, 200, 200, 100, text="Return to title?")
        self.save_confirm_label = Label(300, 200, 200, 100, text="Save the game?")
        self.menu_on = False
        self.saveButton = None
        self.buttons = pygame.sprite.Group()
        self.confirm_buttons = pygame.sprite.Group()
        self.labels = pygame.sprite.Group()
        self.setup_ui()

        self.load_select = False
        self.quit_select = False
        self.title_select = False

    def setup_ui(self):
        # Create controls in here so they're ready to go when needed.

        # buttons that are always visible
        self.save_button = Button(200, 200, 70, 70, self.call_save, text="save")
        self.load_button = Button(400, 200, 70, 70, self.call_load, text="load")
        self.quit_button = Button(600, 200, 70, 70, self.call_quit, text="quit")
        self.return_button = Button(200, 300, 70, 70, self.end_menu, text="return")
        self.title_button = Button(400, 300, 70, 70, self.quit_to_title, text="title")
        self.buttons.add(self.save_button)
        self.buttons.add(self.load_button)
        self.buttons.add(self.quit_button)
        self.buttons.add(self.return_button)
        self.buttons.add(self.title_button)

        # buttons that exist in order to confirm/deny selection

        self.quit_yes = Button(300, 400, 70, 70, self.quit_confirm, text="", disabled=UIResources.textbox)
        self.quit_no = Button(400, 400, 70, 70, self.quit_deny, text="", disabled=UIResources.textbox)
        self.load_yes = Button(300, 400, 70, 70, self.load_confirm, text="", disabled=UIResources.textbox)
        self.load_no = Button(400, 400, 70, 70, self.load_deny, text="", disabled=UIResources.textbox)
        self.title_yes = Button(300, 400, 70, 70, self.title_confirm, text="", disabled=UIResources.textbox)
        self.title_no = Button(400, 400, 70, 70, self.title_deny, text="", disabled=UIResources.textbox)
        self.save_yes = Button(300, 400, 70, 70, self.save_confirm, text="", disabled=UIResources.textbox)
        self.save_no = Button(400, 400, 70, 70, self.save_deny, text="", disabled=UIResources.textbox)

        self.confirm_buttons.add(self.quit_yes)
        self.confirm_buttons.add(self.quit_no)
        self.confirm_buttons.add(self.load_yes)
        self.confirm_buttons.add(self.load_no)
        self.confirm_buttons.add(self.title_yes)
        self.confirm_buttons.add(self.title_no)
        self.confirm_buttons.add(self.save_yes)
        self.confirm_buttons.add(self.save_no)

    def save_confirm(self):
        self.save_yes.set_text("")
        self.save_no.set_text("")
        self.save_yes.disable()
        self.save_no.disable()
        self.save_yes.kill()
        self.save_no.kill()
        self.save_confirm_label.kill()

        self.save_file()

        for button in self.buttons:
            button.enable()

    def save_deny(self):
        self.save_yes.set_text("")
        self.save_no.set_text("")
        self.save_yes.disable()
        self.save_no.disable()
        self.save_yes.kill()
        self.save_no.kill()
        self.save_confirm_label.kill()
        for button in self.buttons:
            button.enable()

    def quit_confirm(self):
        print("quitting game")
        self.quit_yes.set_text("")
        self.quit_no.set_text("")
        self.quit_yes.disable()
        self.quit_no.disable()
        self.quit_yes.kill()
        self.quit_no.kill()
        self.quit_confirm_label.kill()
        for button in self.buttons:
            button.enable()

        self.quit_select = True
        self.menu_on = False

    def quit_deny(self):
        self.quit_yes.set_text("")
        self.quit_no.set_text("")
        self.quit_yes.disable()
        self.quit_no.disable()
        self.quit_yes.kill()
        self.quit_no.kill()
        self.quit_confirm_label.kill()
        for button in self.buttons:
            button.enable()

    def load_confirm(self):
        print("loading file")
        self.load_yes.set_text("")
        self.load_no.set_text("")
        self.load_yes.disable()
        self.load_no.disable()
        self.load_yes.kill()
        self.load_no.kill()
        self.load_confirm_label.kill()
        for button in self.buttons:
            button.enable()

        self.load_select = True
        self.menu_on = False

    def load_deny(self):
        self.load_yes.set_text("")
        self.load_no.set_text("")
        self.load_yes.disable()
        self.load_no.disable()
        self.load_yes.kill()
        self.load_no.kill()
        self.load_confirm_label.kill()
        for button in self.buttons:
            button.enable()

    def title_confirm(self):
        self.title_yes.set_text("")
        self.title_no.set_text("")
        self.title_yes.disable()
        self.title_no.disable()
        self.title_yes.kill()
        self.title_no.kill()
        self.title_confirm_label.kill()
        for button in self.buttons:
            button.enable()

        self.title_select = True
        self.menu_on = False

    def title_deny(self):
        self.title_yes.set_text("")
        self.title_no.set_text("")
        self.title_yes.disable()
        self.title_no.disable()
        self.title_yes.kill()
        self.title_no.kill()
        self.title_confirm_label.kill()
        for button in self.buttons:
            button.enable()

    def call_load(self):
        for button in self.buttons:
            button.disable()

        self.load_yes.set_text("yes")
        self.load_no.set_text("no")
        self.load_yes.enable()
        self.load_no.enable()

        self.confirm_buttons.add(self.load_yes)
        self.confirm_buttons.add(self.load_no)
        self.labels.add(self.load_confirm_label)

    def call_quit(self):
        for button in self.buttons:
            button.disable()
        # self.confirm_buttons.add(self.quit_yes)
        # self.confirm_buttons.add(self.quit_no)
        self.quit_yes.set_text("yes")
        self.quit_no.set_text("no")
        self.quit_yes.enable()
        self.quit_no.enable()
        self.confirm_buttons.add(self.quit_yes)
        self.confirm_buttons.add(self.quit_no)
        self.labels.add(self.quit_confirm_label)

    def call_save(self):
        for button in self.buttons:
            button.disable()
        self.save_yes.set_text("yes")
        self.save_no.set_text("no")
        self.save_yes.enable()
        self.save_no.enable()
        self.confirm_buttons.add(self.save_yes)
        self.confirm_buttons.add(self.save_no)
        self.labels.add(self.save_confirm_label)

    def end_menu(self):
        self.menu_on = False

    def quit_to_title(self):
        for button in self.buttons:
            button.disable()
        # self.confirm_buttons.add(self.title_yes)
        # self.confirm_buttons.add(self.title_no)
        self.title_yes.set_text("yes")
        self.title_no.set_text("no")
        self.title_yes.enable()
        self.title_no.enable()
        self.confirm_buttons.add(self.title_yes)
        self.confirm_buttons.add(self.title_no)
        self.labels.add(self.title_confirm_label)

    def save_file(self):
        print("saving game")
        with open("savefile.txt", 'w') as savefile:
            # order: name, str, vit, agi, int, charm, magic, stress, day, hour, affection, current scene, life sim iter
            # flag1, flag2, flag3, flag4, flag5
            savestring = str(self.game_state.player_name) + "\n"
            savestring += str(self.game_state.strength) + "\n" + str(self.game_state.vitality) + "\n"
            savestring += str(self.game_state.agility) + "\n" + str(self.game_state.intelligence) + "\n"
            savestring += str(self.game_state.charm) + "\n" + str(self.game_state.magic) + "\n"
            savestring += str(self.game_state.stress) + "\n"
            savestring += str(self.game_state.day) + "\n" + str(self.game_state.hour) + "\n"
            savestring += str(self.game_state.affection) + "\n"
            savestring += str(self.game_state.current_scene) + "\n" + str(self.game_state.life_sim_iter) + "\n"
            savestring += str(self.game_state.flag1) + "\n" + str(self.game_state.flag2) + "\n"
            savestring += str(self.game_state.flag3) + "\n" + str(self.game_state.flag4) + "\n" + str(self.game_state.flag5)

            savefile.write(savestring)

    def set_game_state(self, game_state):
        self.game_state = game_state

    def loop(self):
        self.menu_on = True
        self.load_select = False
        self.quit_select = False
        self.title_select = False

        self.quit_yes.disable()
        self.quit_no.disable()
        self.load_yes.disable()
        self.load_no.disable()
        self.title_yes.disable()
        self.title_no.disable()
        self.save_yes.disable()
        self.save_no.disable()

        while self.menu_on:

            self.screen.blit(UIResources.backgrounds["paper"], (0, 0))

            for event in pygame.event.get():
                for button in self.buttons:
                    button.handle_event(event)
                for button in self.confirm_buttons:
                    button.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_SPACE]:
                        self.menu_on = False

            self.buttons.draw(self.screen)
            self.confirm_buttons.draw(self.screen)
            self.labels.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(40)

        if self.load_select:
            return "load"
        elif self.quit_select:
            return "quit"
        elif self.title_select:
            return "title"
        else:
            return "fine"
