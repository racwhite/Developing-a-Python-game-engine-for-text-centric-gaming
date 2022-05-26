import copy

from program import ScriptCommand
from ui_controls import *
import sys


class VisualNovelScene:

    def __init__(self, screen, clock, name, script, game_state, menu):
        self.screen = screen
        self.clock = clock
        self.name = name
        self.menu = menu
        self.script = script[name]
        self.game_state = game_state
        self.clone_state = game_state
        self.current_command = 0
        self.background = UIResources.backgrounds["city_background"]
        self.result = ""

        # entirely transparent textboxes... just in case
        self.clear_textbox = TextBox(tl=UIResources.textbox, ml=UIResources.textbox, bl=UIResources.textbox,
                                     tm=UIResources.textbox, mm=UIResources.textbox, bm=UIResources.textbox,
                                     tr=UIResources.textbox, mr=UIResources.textbox, br=UIResources.textbox)

        self.textbox = self.clear_textbox

        # self.textbox = TextBox(
        #    text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
        #         "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
        #         "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit "
        #         "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
        #         "culpa qui officia deserunt mollit anim id est laborum.", speaker="Gilgamesh")
        self.boxes = pygame.sprite.Group()
        self.boxes.add(self.textbox)

        # invisible button that sits on textbox and advances dialogue
        self.advance_button = Button(130, 370, 550, 200, self.increment_command, disabled=UIResources.textbox,
                                     idle=UIResources.textbox, hot=UIResources.textbox, active=UIResources.textbox)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.advance_button)

        # prime character sprite with clear box
        self.character = Label(150, 50, 525, 700, image=UIResources.textbox)
        self.character_left = Label(0, 50, 525, 700, image=UIResources.textbox)
        self.character_right = Label(350, 50, 525, 700, image=UIResources.textbox)
        self.talk_sprite = pygame.sprite.Group()
        self.talk_sprite.add(self.character)
        self.talk_sprite.add(self.character_left)
        self.talk_sprite.add(self.character_right)

        # buttons and other things important for script branching
        self.d1 = DecisionButton(400, 150, self.decision_jump)
        self.d2 = DecisionButton(400, 250, self.decision_jump)
        self.d3 = DecisionButton(400, 350, self.decision_jump)
        self.d4 = DecisionButton(400, 450, self.decision_jump)
        self.d_buttons = pygame.sprite.Group()
        self.d_buttons.add(self.d1)
        self.d_buttons.add(self.d2)
        self.d_buttons.add(self.d3)
        self.d_buttons.add(self.d4)

        self.buttons.add(self.d1)
        self.buttons.add(self.d2)
        self.buttons.add(self.d3)
        self.buttons.add(self.d4)

        self.executors = {"s": self.not_executable,
                          "b": self.execute_b,
                          "c": self.execute_c,
                          "t": self.execute_t,
                          "d": self.execute_d,
                          "x": self.not_executable,
                          "j": self.execute_j,
                          "k": self.execute_k,
                          "p": self.not_executable, # temporary, will eventually be the "play sound"
                          "gt": self.execute_gt,
                          "lt": self.execute_lt,
                          "eq": self.execute_eq,
                          "chg": self.execute_chg,
                          "z": self.execute_z}

    def decision_jump(self, jumptag: str):
        j_command = ScriptCommand("j", [jumptag])
        for button in self.d_buttons:
            button.disable()
        self.advance_button.enable()

        self.execute_j(j_command)

    def process_text(self, text):

        newText = text

        if text.find('<') >= 0:
            newText = newText.replace("<player_name>", self.game_state.player_name)
            newText = newText.replace("<wizard_name>", self.game_state.wizard_name)

        return newText

    def execute_commands(self, key: ScriptCommand):
        # noinspection PyArgumentList
        return self.executors[str(key.command)](key)

    def not_executable(self, com: ScriptCommand):
        print("I did nothing")
        self.current_command += 1

    def execute_b(self, com: ScriptCommand):

        self.background = UIResources.backgrounds[com.args[0]]
        self.current_command += 1

    def execute_c(self, com: ScriptCommand):
        # to clear a character sprite, use set_image(UIResources.characters["clear"]["clear"])
        # to clear a sprite from the script itself, make both args "clear"
        # format is c {character_left_name} {character_left_mood} {character_mid_name} {character_mid_mood} {character_right_name} {character_right_mood}
        # ex, for displaying only the middle sprite, use c {} {} {wizard} {neutral} {} {}
        if len(com.args[0]) == 0:
            self.character_left.set_image(UIResources.characters["clear"]["clear"])
        else:
            self.character_left.set_image(UIResources.characters[com.args[0]][com.args[1]])
        if len(com.args[2]) == 0:
            self.character.set_image(UIResources.characters["clear"]["clear"])
        else:
            self.character.set_image(UIResources.characters[com.args[2]][com.args[3]])
        if len(com.args[4]) == 0:
            self.character_right.set_image(UIResources.characters["clear"]["clear"])
        else:
            self.character_right.set_image(UIResources.characters[com.args[4]][com.args[5]])
        self.current_command += 1

    def execute_t(self, com: ScriptCommand):

        self.textbox.kill()
        processed_speaker = self.process_text(com.args[0])
        processed_text = self.process_text(com.args[1])

        if len(processed_speaker) > 0:
            self.textbox = TextBox(text=processed_text, speaker=processed_speaker)
        else:
            self.textbox = TextBox(text=processed_text, speaker=None)
        self.boxes.add(self.textbox)

    def execute_d(self, com: ScriptCommand):

        # disable dialogue advance
        self.advance_button.disable()

        # display up to 4 dialogue buttons by enabling them
        # extract relevant bits from key1:decision name 1:jump_tag_1
        args_list = []

        for arg in com.args:
            args_list.append(arg.split(":"))

        if len(com.args) == 1:
            # draw button 1
            self.d1.enable(args_list[0][1], args_list[0][2])
        elif len(com.args) == 2:
            # draw buttons 1 and 2
            self.d1.enable(args_list[0][1], args_list[0][2])
            self.d2.enable(args_list[1][1], args_list[1][2])
        elif len(com.args) == 3:
            # draw buttons 1, 2, and 3
            self.d1.enable(args_list[0][1], args_list[0][2])
            self.d2.enable(args_list[1][1], args_list[1][2])
            self.d3.enable(args_list[2][1], args_list[2][2])
        elif len(com.args) == 4:
            # draw buttons 1, 2, 3, and 4
            self.d1.enable(args_list[0][1], args_list[0][2])
            self.d2.enable(args_list[1][1], args_list[1][2])
            self.d3.enable(args_list[2][1], args_list[2][2])
            self.d3.enable(args_list[3][1], args_list[3][2])

    def execute_j(self, command: ScriptCommand):

        for i, com in enumerate(self.script):
            if com.command == "x" and com.args[0] == command.args[0]:
                self.current_command = i
                break

    def execute_k(self, command: ScriptCommand):
        # format: k {s/m} {name of sound in sound dictionary}
        # play sound
        # TODO: NEEDS TESTING!!!
        if command.args[0] == "s" and len(command.args[1]) > 0:
            pygame.mixer.Sound.play(UIResources.sounds(command.args[1]))
        elif command.args[0] == "m" and len(command.args[1]) > 0:
            pygame.mixer.music.load(UIResources.sounds(command.args[1]))
            # loop indefinitely
            pygame.mixer.music.play(-1)
        elif len(command.args[1]) == 0:
            pygame.mixer.music.stop()

    def execute_gt(self, command: ScriptCommand):

        stat_name = command.args[0]
        value = int(command.args[1])
        true_jump = command.args[2]
        false_jump = command.args[3]
        check_passed = False

        if stat_name == "strength":
            if self.game_state.strength > value:
                check_passed = True
        elif stat_name == "vitality":
            if self.game_state.vitality > value:
                check_passed = True
        elif stat_name == "agility":
            if self.game_state.agility > value:
                check_passed = True
        elif stat_name == "intelligence":
            if self.game_state.intelligence > value:
                check_passed = True
        elif stat_name == "charm":
            if self.game_state.charm > value:
                check_passed = True
        elif stat_name == "magic":
            if self.game_state.magic > value:
                check_passed = True
        elif stat_name == "stress":
            if self.game_state.stress > value:
                check_passed = True
        elif stat_name == "affection":
            if self.game_state.affection > value:
                check_passed = True

        if check_passed:
            jump_command = ScriptCommand("j", [true_jump])
        else:
            jump_command = ScriptCommand("j", [false_jump])

        self.execute_j(jump_command)

    def execute_lt(self, command: ScriptCommand):

        stat_name = command.args[0]
        value = int(command.args[1])
        true_jump = command.args[2]
        false_jump = command.args[3]
        check_passed = False

        if stat_name == "strength":
            if self.game_state.strength < value:
                check_passed = True
        elif stat_name == "vitality":
            if self.game_state.vitality < value:
                check_passed = True
        elif stat_name == "agility":
            if self.game_state.agility < value:
                check_passed = True
        elif stat_name == "intelligence":
            if self.game_state.intelligence < value:
                check_passed = True
        elif stat_name == "charm":
            if self.game_state.charm < value:
                check_passed = True
        elif stat_name == "magic":
            if self.game_state.magic < value:
                check_passed = True
        elif stat_name == "stress":
            if self.game_state.stress < value:
                check_passed = True
        elif stat_name == "affection":
            if self.game_state.affection < value:
                check_passed = True

        if check_passed:
            jump_command = ScriptCommand("j", [true_jump])
        else:
            jump_command = ScriptCommand("j", [false_jump])

        self.execute_j(jump_command)

    def execute_eq(self, command: ScriptCommand):

        stat_name = command.args[0]
        value = int(command.args[1])
        true_jump = command.args[2]
        false_jump = command.args[3]
        check_passed = False

        if stat_name == "strength":
            if self.game_state.strength == value:
                check_passed = True
        elif stat_name == "vitality":
            if self.game_state.vitality == value:
                check_passed = True
        elif stat_name == "agility":
            if self.game_state.agility == value:
                check_passed = True
        elif stat_name == "intelligence":
            if self.game_state.intelligence == value:
                check_passed = True
        elif stat_name == "charm":
            if self.game_state.charm == value:
                check_passed = True
        elif stat_name == "magic":
            if self.game_state.magic == value:
                check_passed = True
        elif stat_name == "stress":
            if self.game_state.stress == value:
                check_passed = True
        elif stat_name == "affection":
            if self.game_state.affection == value:
                check_passed = True

        if check_passed:
            jump_command = ScriptCommand("j", [true_jump])
        else:
            jump_command = ScriptCommand("j", [false_jump])

        self.execute_j(jump_command)

    def execute_chg(self, command: ScriptCommand):
        stat_name = command.args[0]
        adjust_value = 0
        if len(command.args[1]) > 0:
            adjust_value = int(command.args[1])
        new_value = 0
        if len(command.args[2]) > 0:
            new_value = int(command.args[2])

        if stat_name == "strength":
            if adjust_value != 0:
                self.game_state.strength += adjust_value
            else:
                self.game_state.strength = new_value
        elif stat_name == "vitality":
            if adjust_value != 0:
                self.game_state.vitality += adjust_value
            else:
                self.game_state.vitality = new_value
        elif stat_name == "agility":
            if adjust_value != 0:
                self.game_state.agility += adjust_value
            else:
                self.game_state.agility = new_value
        elif stat_name == "intelligence":
            if adjust_value != 0:
                self.game_state.intelligence += adjust_value
            else:
                self.game_state.intelligence = new_value
        elif stat_name == "charm":
            if adjust_value != 0:
                self.game_state.charm += adjust_value
            else:
                self.game_state.charm = new_value
        elif stat_name == "magic":
            if adjust_value != 0:
                self.game_state.magic += adjust_value
            else:
                self.game_state.magic = new_value
        elif stat_name == "stress":
            if adjust_value != 0:
                self.game_state.stress += adjust_value
            else:
                self.game_state.stress = new_value
        elif stat_name == "affection":
            if adjust_value != 0:
                self.game_state.affection += adjust_value
            else:
                self.game_state.affection = new_value

        # for inevitably rewriting this
        # god or i could just add a few more elif chains it's not like they'll kill anything at this point
        """for stat in ("strength", "vitality", "agility", "intelligence", "charm", "magic", "stress"):
            if getattr(self.game_state, stat) < 0:
                setattr(self.game_state, stat, 0)
            elif getattr(self.game_state, stat) > 100:
                setattr(self.game_state, stat, 100)"""

        self.current_command += 1

    # noinspection PyMethodMayBeStatic
    def execute_z(self, command: ScriptCommand):
        return command.args[0], command.args[1], command.args[2]

    def increment_command(self):
        self.current_command += 1

    def loop(self):
        self.screen.fill((255, 255, 255))
        self.current_command = 0
        self.game_state.current_scene = self.name
        # Clone game state at start of scene for game saving purposes.
        self.clone_state = copy.deepcopy(self.game_state)
        last_command = None
        print("GAME STATE CURRENT SCENE:", self.game_state.current_scene)

        for button in self.d_buttons:
            button.disable()

        while self.current_command < len(self.script):

            for event in pygame.event.get():
                for button in self.buttons:
                    button.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_SPACE]:
                        print("Spacebar pressed")
                        self.menu.set_game_state(self.clone_state)
                        result = self.menu.loop()
                        print("Result is " + result)
                        # if load or quit was selected
                        if result == "load":
                            return "load", "", ""
                        if result == "title":
                            return "title", "", ""
                        if result == "quit":
                            return "quit", "", ""

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # current_command_type = self.script[self.current_command].command
            # DEBUG, print out info on what command is being executed if it's new.
            if last_command != self.current_command:
                last_command = self.current_command
                print("I'm executing command " + self.script[self.current_command].command)
                if len(self.script[self.current_command].args) > 0:
                    print("my args are " + ", ".join([str(x) for x in self.script[self.current_command].args]))

                if self.script[self.current_command].command == "z":
                    return self.execute_commands(self.script[self.current_command])
                self.execute_commands(self.script[self.current_command])

            self.screen.blit(self.background, (0, 0))
            self.talk_sprite.draw(self.screen)
            self.boxes.draw(self.screen)
            self.d_buttons.draw(self.screen)

            pygame.display.flip()

            self.textbox.update_every_frame(self.clock.get_time())
            self.clock.tick(40)


        # should be unreachable
        return "life_sim", "", ""
