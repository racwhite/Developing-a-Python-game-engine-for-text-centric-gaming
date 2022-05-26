import pygame
import copy
import re
import titleScreenScene
from typing import Optional, Dict
import gameMenu
import os

from lifeSimScene import *
from visualNovelScene import *
from inputScene import *


class GameState:
    def __init__(self):
        # Character stats
        self.player_name = "Alpha"
        self.wizard_name = "Adam Eldritch"
        self.strength = 0
        self.vitality = 0
        self.agility = 0
        self.intelligence = 0
        self.charm = 0
        self.magic = 0
        self.stress = 0
        # Time progression
        self.day = 0
        self.hour = 0
        # Wizard stats
        self.affection = 0
        # Key moment results
        self.dialogue_results = []
        self.stat_check_results = []
        # Other flags
        self.completed_prologue = False
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0
        self.flag4 = 0
        self.flag5 = 0
        # ...and whatever else...
        self.current_scene = None
        self.life_sim_iter = 0

    def reset_state(self):
        self.strength = 20
        self.vitality = 20
        self.intelligence = 20
        self.agility = 20
        self.charm = 20
        self.magic = 20
        self.stress = 0

        self.day = 1
        self.hour = 8

        self.affection = 50

        self.dialogue_results = []
        self.stat_check_results = []

        self.completed_prologue = False
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0
        self.flag4 = 0
        self.flag5 = 0
        # ...and whatever else...
        self.current_scene = None
        self.life_sim_iter = 0
        self.current_scene = "prologue"

    # noinspection PyArgumentList
    def __deepcopy__(self, memo: Optional[Dict] = None):
        if memo is None:
            memo = {}
        new_state = GameState()
        new_state.player_name = self.player_name
        new_state.wizard_name = self.wizard_name
        new_state.strength = self.strength
        new_state.vitality = self.vitality
        new_state.agility = self.agility
        new_state.intelligence = self.intelligence
        new_state.charm = self.charm
        new_state.magic = self.magic
        new_state.stress = self.stress
        # Time progression
        new_state.day = self.day
        new_state.hour = self.hour
        # Wizard stats
        new_state.affection = self.affection
        # Key moment results
        new_state.dialogue_results = copy.deepcopy(self.dialogue_results, memo)
        new_state.stat_check_results = copy.deepcopy(self.stat_check_results, memo)
        # Other flags
        new_state.completed_prologue = self.completed_prologue
        new_state.flag1 = self.flag1
        new_state.flag2 = self.flag2
        new_state.flag3 = self.flag3
        new_state.flag4 = self.flag4
        new_state.flag5 = self.flag5
        # ...and whatever else...
        new_state.current_scene = self.current_scene
        new_state.life_sim_iter = self.life_sim_iter

        return new_state


class SceneManager:
    def __init__(self, screen, script):
        self.screen = screen
        self.game_state = GameState()
        self.script = script
        self.clock = pygame.time.Clock()

        self.game_state.reset_state()

        self.menu = gameMenu.GameMenu(self.screen, self.clock, self.game_state)

        self.scenes = {"title_screen": titleScreenScene.TitleScreenScene(self.screen, self.clock, self.game_state),
                       "life_sim": LifeSimScene(self.screen, self.clock, self.game_state, self.menu),
                       "get_input": PlayerInputScene(self.screen, self.clock, self.game_state),
                       "prologue": VisualNovelScene(self.screen, self.clock, "prologue", self.script, self.game_state,
                                                    self.menu),
                       "day_1": VisualNovelScene(self.screen, self.clock, "day_1", self.script, self.game_state,
                                                 self.menu),
                       "day_3": VisualNovelScene(self.screen, self.clock, "day_3", self.script, self.game_state,
                                                 self.menu),
                       "day_5": VisualNovelScene(self.screen, self.clock, "day_5", self.script, self.game_state,
                                                 self.menu),
                       "day_7": VisualNovelScene(self.screen, self.clock, "day_7", self.script, self.game_state,
                                                 self.menu),
                       "day_8": VisualNovelScene(self.screen, self.clock, "day_8", self.script, self.game_state,
                                                 self.menu),
                       "day_9": VisualNovelScene(self.screen, self.clock, "day_9", self.script, self.game_state,
                                                 self.menu),
                       "day_10": VisualNovelScene(self.screen, self.clock, "day_10", self.script, self.game_state,
                                                  self.menu),
                       "day_12": VisualNovelScene(self.screen, self.clock, "day_12", self.script, self.game_state,
                                                  self.menu),
                       "day_14": VisualNovelScene(self.screen, self.clock, "day_14", self.script, self.game_state,
                                                  self.menu),
                       "day_15": VisualNovelScene(self.screen, self.clock, "day_15", self.script, self.game_state,
                                                  self.menu),
                       "day_17": VisualNovelScene(self.screen, self.clock, "day_17", self.script, self.game_state,
                                                  self.menu),
                       "day_18": VisualNovelScene(self.screen, self.clock, "day_18", self.script, self.game_state,
                                                  self.menu),
                       "day_20_early": VisualNovelScene(self.screen, self.clock, "day_20_early", self.script,
                                                        self.game_state, self.menu),
                       "day_20_late": VisualNovelScene(self.screen, self.clock, "day_20_late", self.script,
                                                       self.game_state, self.menu),
                       "day_22": VisualNovelScene(self.screen, self.clock, "day_22", self.script, self.game_state,
                                                  self.menu),
                       "day_23_bad": VisualNovelScene(self.screen, self.clock, "day_23_bad", self.script, self.game_state,
                                                      self.menu),
                       "day_23_good": VisualNovelScene(self.screen, self.clock, "day_23_good", self.script, self.game_state,
                                                       self.menu),
                       "day_25": VisualNovelScene(self.screen, self.clock, "day_25", self.script, self.game_state,
                                                  self.menu),
                       "day_27_bad": VisualNovelScene(self.screen, self.clock, "day_27_bad", self.script, self.game_state,
                                                      self.menu),
                       "day_27_good": VisualNovelScene(self.screen, self.clock, "day_27_good", self.script, self.game_state,
                                                       self.menu),
                       "day_30": VisualNovelScene(self.screen, self.clock, "day_30", self.script, self.game_state,
                                                  self.menu),
                       "dead_end1": VisualNovelScene(self.screen, self.clock, "dead_end1", self.script, self.game_state,
                                                     self.menu),
                       "dead_end2": VisualNovelScene(self.screen, self.clock, "dead_end2", self.script, self.game_state,
                                                     self.menu),
                       "dead_end3": VisualNovelScene(self.screen, self.clock, "dead_end3", self.script, self.game_state,
                                                     self.menu),
                       "bad_end": VisualNovelScene(self.screen, self.clock, "bad_end", self.script, self.game_state,
                                                   self.menu),
                       "normal_end": VisualNovelScene(self.screen, self.clock, "normal_end", self.script,
                                                      self.game_state, self.menu),
                       "good_end": VisualNovelScene(self.screen, self.clock, "good_end", self.script, self.game_state,
                                                    self.menu),
                       "stress": VisualNovelScene(self.screen, self.clock, "stress", self.script, self.game_state,
                                                  self.menu)
                       }

    def draw_fade_out(self):
        fade = pygame.Surface((800, 600))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

    def load_game(self):
        result = True
        # noinspection PyBroadException
        try:
            with open("savefile.txt", 'r') as savefile:
                stats = savefile.read().splitlines()
                # order: name, str, vit, int, agi, charm, magic, stress, day, hour, affection, current scene, life sim iter
                # set game_state to values from this list
                self.game_state.player_name = str(stats[0])
                self.game_state.strength = int(stats[1])
                self.game_state.vitality = int(stats[2])
                self.game_state.agility = int(stats[3])
                self.game_state.intelligence = int(stats[4])
                self.game_state.charm = int(stats[5])
                self.game_state.magic = int(stats[6])
                self.game_state.stress = int(stats[7])
                self.game_state.day = int(stats[8])
                self.game_state.hour = int(stats[9])
                self.game_state.affection = int(stats[10])
                self.game_state.current_scene = str(stats[11])
                self.game_state.life_sim_iter = int(stats[12])
                self.game_state.flag1 = int(stats[13])
                self.game_state.flag2 = int(stats[14])
                self.game_state.flag3 = int(stats[15])
                self.game_state.flag4 = int(stats[16])
                self.game_state.flag5 = int(stats[17])
        except Exception as e:
            print(f"Error loading save file: {e:s}")
            result = False

        return result, self.game_state.current_scene

    def loop(self):
        result, next_scene, transition = self.scenes["title_screen"].loop()
        self.draw_fade_out()

        while result != "quit":
            print("I'm back in scene manager")
            if result == "new_game":
                self.scenes["get_input"].loop()
                result, next_scene, transition = self.scenes["prologue"].loop()
            elif result == "title":
                print("I should go back to the title")
                self.draw_fade_out()
                result, next_scene, transition = self.scenes["title_screen"].loop()
            elif result == "load":
                # Do stuff to load a saved game, and then transition to the right scene.
                print("I should go here to load")
                load_result, next_scene = self.load_game()
                if load_result:
                    # Avoid the life sim incorrectly incrementing its iteration counter too much.
                    if next_scene == "life_sim":
                        self.game_state.life_sim_iter -= 1
                    result, next_scene, transition = self.scenes[next_scene].loop()
                else:
                    # TODO: Show some kind of "Load Failed!" message on the title screen, or a message box, etc.
                    pass
            elif result == "flag1":
                self.game_state.flag1 = 1
                result, next_scene, transition = self.scenes[next_scene].loop()
            elif result == "flag2":
                self.game_state.flag2 = 1
                result, next_scene, transition = self.scenes[next_scene].loop()
            elif result == "flag3":
                self.game_state.flag3 = 1
                result, next_scene, transition = self.scenes[next_scene].loop()
            elif result == "flag4":
                self.game_state.flag4 = 1
                result, next_scene, transition = self.scenes[next_scene].loop()
            elif result == "flag5":
                self.game_state.flag5 = 1
                result, next_scene, transition = self.scenes[next_scene].loop()

            elif result == "day_23_check":
                # TODO: Make this check actually match script values.
                self.draw_fade_out()
                if self.game_state.flag1 > 0:
                    result, next_scene, transition = self.scenes[next_scene + "_good"].loop()
                else:
                    result, next_scene, transition = self.scenes[next_scene + "_bad"].loop()
            elif result == "day_27_check":
                # TODO: Make this check actually match script values.
                self.draw_fade_out()
                if self.game_state.flag1 > 0:
                    result, next_scene, transition = self.scenes[next_scene + "_good"].loop()
                else:
                    result, next_scene, transition = self.scenes[next_scene + "_bad"].loop()
            elif result == "day_30_check":
                # TODO: Make this check actually match script values.
                self.draw_fade_out()
                if self.game_state.flag1 + self.game_state.flag2 + self.game_state.flag3 + self.game_state.flag4 + self.game_state.flag5 > 0:
                    result, next_scene, transition = self.scenes[next_scene].loop()
                else:
                    result, next_scene, transition = self.scenes["bad_end"].loop()
            elif result == "end_game":
                if self.game_state.flag1 + self.game_state.flag2 + self.game_state.flag3 + self.game_state.flag4 + self.game_state.flag5 >= 5:
                    self.draw_fade_out()
                    result, next_scene, transition = self.scenes["good_end"].loop()
                else:
                    self.draw_fade_out()
                    result, next_scene, transition = self.scenes["normal_end"].loop()
            elif len(next_scene) > 0:
                # Put any logic in here to potentially change things before moving to the next scene.
                self.draw_fade_out()
                result, next_scene, transition = self.scenes[next_scene].loop()
            else:
                break

        pygame.quit()
        sys.exit()
