import sys
import random
import gameMenu

# import ui_controls  # ui_controls.Button(...)
# or
from ui_controls import *  # Button(...)
from titleScreenScene import *
from typing import List

STAT_STR = 1
STAT_VIT = 2
STAT_AGI = 3
STAT_INT = 4
STAT_CHARM = 5
STAT_MAGIC = 6

NUM_DAYS = 30

TIME_EXERCISE = 5
TIME_HOUSEKEEPING = 3
TIME_RESEARCH = 2
TIME_REST = 8
TIME_SHARPEN = 2
TIME_STALKING = 4
TIME_STUDY = 2

# TEXTBOX DIMENSIONS AND PLACEMENT
TEXT_X = 25
TEXT_Y = 445
TEXT_W = 750
TEXT_H = 150

# FOR INDEXING INTO DISPLAY LISTS
STR = 0
VIT = 1
AGI = 2
INT = 3
CHARM = 4
MAGIC = 5

# PLACEMENT AND SIZE OF CALENDAR ON SCREEN
CALENDAR_OFFSET = [80, 70]
CALENDAR_DIMENSIONS = [300, 225]


def shuffle_favors():
    # str vit agi int charm magic
    # 1    2   3   4    5    6

    # might want to rewrite this using shuffle() when i wake up
    all_days_list = []

    for k in range(int(NUM_DAYS / 6)):
        day_set = [x + 1 for x in range(6)]
        for j in range(2):
            for i in range(len(day_set) - 1):
                r = random.randint(i + 1, len(day_set) - 1)
                v = day_set[i]
                day_set[i] = day_set[r]
                day_set[r] = v
        all_days_list.extend(day_set)

    print("# of days shuffled is " + str(len(all_days_list)))
    print(" ".join(str(all_days_list)))

    return all_days_list


def get_calendar_grid_pos(day):
    # using the passed in date, calculate where it would be on the grid (returns [x,y])
    day_offset = 1
    col_index = (day + day_offset - 1) % 8
    row_index = ((day + day_offset - 1) // 8) + 1
    return [col_index, row_index]


class LifeSimScene:
    def __init__(self, screen, clock, game_state, menu):
        self.screen = screen
        self.clock = clock
        self.game_state = game_state
        self.menu = menu
        self.result = None
        self.favored_stats = shuffle_favors()
        self.buttons = pygame.sprite.Group()
        # self.testButton = Button(200, 200, 100, 100, self.test_event, text="hello")
        # self.buttons.add(self.testButton)
        self.labels = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        # iteration - 1 is the index into this.
        # Each element is a dictionary with the time to do the transition to the next scene, and where to go.
        self.transitions = [
            {
                "day": 1,
                "hour": 18,
                "scene": "day_1",
                "draw": True,
                "result": ""
            },
            {
                "day": 3,
                "hour": 8,
                "scene": "day_3",
                "draw": False,
                "result": ""
            },
            {
                "day": 5,
                "hour": 8,
                "scene": "day_5",
                "draw": False,
                "result": ""
            },
            {
                "day": 7,
                "hour": 12,
                "scene": "day_7",
                "draw": True,
                "result": ""
            },
            {
                "day": 8,
                "hour": 8,
                "scene": "day_8",
                "draw": True,
                "result": ""
            },
            {
                "day": 9,
                "hour": 10,
                "scene": "day_9",
                "draw": False,
                "result": ""
            },
            {
                "day": 10,
                "hour": 12,
                "scene": "day_10",
                "draw": False,
                "result": ""
            },
            {
                "day": 12,
                "hour": 20,
                "scene": "day_12",
                "draw": True,
                "result": ""
            },
            {
                "day": 14,
                "hour": 23,
                "scene": "day_14",
                "draw": True,
                "result": ""
            },
            {
                "day": 15,
                "hour": 10,
                "scene": "day_15",
                "draw": False,
                "result": ""
            },
            {
                "day": 17,
                "hour": 8,
                "scene": "day_17",
                "draw": False,
                "result": ""
            },
            {
                "day": 18,
                "hour": 10,
                "scene": "day_18",
                "draw": False,
                "result": ""
            },
            {
                "day": 20,
                "hour": 6,
                "scene": "day_20_early",
                "draw": False,
                "result": ""
            },
            {
                "day": 20,
                "hour": 20,
                "scene": "day_20_late",
                "draw": False,
                "result": ""
            },
            {
                "day": 22,
                "hour": 20,
                "scene": "day_22",
                "draw": False,
                "result": ""
            },
            {
                "day": 23,
                "hour": 10,
                "scene": "day_23",
                "draw": False,
                "result": "day_23_check"
            },
            {
                "day": 25,
                "hour": 10,
                "scene": "day_25",
                "draw": False,
                "result": ""
            },
            {
                "day": 27,
                "hour": 10,
                "scene": "day_27",
                "draw": False,
                "result": "day_27_check"
            },
            {
                "day": 30,
                "hour": 16,
                "scene": "day_30",
                "draw": True,
                "result": "day_30_check"
            }
        ]

        # labels for testing
        # self.testLabel = Label(50, 50, 200, 100, "Hello world", border=True)
        # self.testLabel2 = Label(50, 70, 200, 100, "Hello world", border=True)
        # self.labels.add(self.testLabel)
        # self.labels.add(self.testLabel2)
        self.boxes = pygame.sprite.Group()
        self.textbox = TextBox(x=TEXT_X, y=TEXT_Y, width=TEXT_W, height=TEXT_H, text="", suppressarrow=True)
        self.boxes.add(self.textbox)

        # calendar
        self.cal = Label(CALENDAR_OFFSET[0], CALENDAR_OFFSET[1], CALENDAR_DIMENSIONS[0], CALENDAR_DIMENSIONS[1],
                         image=UIResources.calendar)
        self.labels.add(self.cal)

        # pop up for reading stars
        self.star_popup = Button(350, 150, 150, 50, self.end_stars, text="", disabled=UIResources.textbox)
        self.stars.add(self.star_popup)

        # create window for displaying stats via labels
        self.stat_bg = Label(50, 330, 300, 140, "")
        self.day_bg = Label(50, 50, 200, 20, "")
        self.day_label = Label(10, 50, 150, 20, "Day: ", image=UIResources.textbox)
        self.day_num = Label(50, 50, 150, 20, str(self.game_state.day), image=UIResources.textbox)
        self.hour_label = Label(100, 50, 150, 20, "Hour: ", image=UIResources.textbox)
        self.hour_num = Label(150, 50, 150, 20, str(self.game_state.hour), image=UIResources.textbox)

        # stats by column
        self.stress_label = Label(50, 350, 100, 15, "Stress", image=UIResources.textbox)
        self.stress_num = Label(150, 350, 30, 15, str(game_state.stress), image=UIResources.textbox)
        self.str_label = Label(50, 380, 100, 15, "Strength", image=UIResources.textbox)
        self.str_num = Label(150, 380, 30, 15, str(game_state.strength), image=UIResources.textbox)
        self.vit_label = Label(50, 410, 100, 15, "Vitality", image=UIResources.textbox)
        self.vit_num = Label(150, 410, 30, 15, str(game_state.vitality), image=UIResources.textbox)
        self.agi_label = Label(50, 440, 100, 15, "Agility", image=UIResources.textbox)
        self.agi_num = Label(150, 440, 30, 15, str(game_state.vitality), image=UIResources.textbox)

        self.int_label = Label(200, 380, 100, 15, "Intellect", image=UIResources.textbox)
        self.int_num = Label(300, 380, 30, 15, str(game_state.vitality), image=UIResources.textbox)
        self.charm_label = Label(200, 410, 100, 15, "Charm", image=UIResources.textbox)
        self.charm_num = Label(300, 410, 30, 15, str(game_state.vitality), image=UIResources.textbox)
        self.magic_label = Label(200, 440, 100, 15, "Magic", image=UIResources.textbox)
        self.magic_num = Label(300, 440, 30, 15, str(game_state.vitality), image=UIResources.textbox)
        # these exist for testing purposes
        self.affection_label = Label(200, 350, 100, 15, "Affection", image=UIResources.textbox)
        self.affection_num = Label(300, 350, 30, 15, str(game_state.affection), image=UIResources.textbox)

        self.labels.add(self.day_bg)
        self.labels.add(self.day_label)
        self.labels.add(self.day_num)
        self.labels.add(self.hour_label)
        self.labels.add(self.hour_num)
        self.labels.add(self.stat_bg)
        # testing purposes
        self.labels.add(self.affection_label)
        self.labels.add(self.affection_num)

        self.labels.add(self.stress_label)
        self.labels.add(self.stress_num)
        self.labels.add(self.str_label)
        self.labels.add(self.str_num)
        self.labels.add(self.vit_label)
        self.labels.add(self.vit_num)
        self.labels.add(self.agi_label)
        self.labels.add(self.agi_num)
        self.labels.add(self.int_label)
        self.labels.add(self.int_num)
        self.labels.add(self.charm_label)
        self.labels.add(self.charm_num)
        self.labels.add(self.magic_label)
        self.labels.add(self.magic_num)

        # create and place buttons
        self.housekeepingButton = ActionButton(450, 50, 70, 70, self.perform_housekeeping, self.hover_house,
                                               text="house")
        self.stalkingButton = ActionButton(565, 50, 70, 70, self.perform_stalking, self.hover_stalk, text="stalk")
        self.studyButton = ActionButton(680, 50, 70, 70, self.perform_study, self.hover_study, text="study")
        self.exerciseButton = ActionButton(450, 150, 70, 70, self.perform_exercise, self.hover_exercise,
                                           text="exercise")
        self.sharpenButton = ActionButton(565, 150, 70, 70, self.perform_sharpen, self.hover_sharpen, text="sharpen")
        self.practiceButton = ActionButton(680, 150, 70, 70, self.perform_research, self.hover_research,
                                           text="practice")
        self.restButton = ActionButton(450, 250, 70, 70, self.perform_rest, self.hover_rest, text="rest")
        self.star_button = ActionButton(565, 250, 70, 70, self.read_stars, self.hover_star, text="stars")
        self.menu_button = Button(450, 350, 70, 70, self.open_menu, text="menu")

        self.buttons.add(self.housekeepingButton)
        self.buttons.add(self.stalkingButton)
        self.buttons.add(self.studyButton)
        self.buttons.add(self.exerciseButton)
        self.buttons.add(self.sharpenButton)
        self.buttons.add(self.practiceButton)
        self.buttons.add(self.restButton)
        self.buttons.add(self.star_button)
        self.buttons.add(self.menu_button)

        # box for keeping track of the current day
        self.day_tracker = Label(0, 0, 1, 1, image=UIResources.textbox)
        self.labels.add(self.day_tracker)
        # can't add a none object to the labels group, so initialize it here
        self.highlight_key_dates()
        self.highlight_current_day()

    def validate_stats(self):
        for stat in ("strength", "vitality", "agility", "intelligence", "charm", "magic", "stress"):
            if getattr(self.game_state, stat) < 0:
                setattr(self.game_state, stat, 0)
            elif getattr(self.game_state, stat) > 100:
                setattr(self.game_state, stat, 100)

    def read_stars(self):
        # TODO: Display fluff text
        # yeah you're gonna do a 2d array where the first index is the stat of the day and the second index is pointing to
        # some kinda silly string
        # and then you put that into the following
        # self.textbox.update_text_and_speaker()
        pass

    def end_stars(self):

        self.star_popup.set_text("")
        self.star_popup.disable()
        self.star_popup.kill()
        for button in self.buttons:
            button.enable()

    def open_menu(self):
        self.result = ""
        self.menu.set_game_state(self.game_state)
        self.result = self.menu.loop()

    def advance_time(self, hours: int):
        self.game_state.hour += hours
        while self.game_state.hour >= 24:
            self.game_state.day += 1
            self.game_state.hour -= 24
        while self.game_state.hour < 0:
            self.game_state.day -= 1
            self.game_state.hour += 24

        self.highlight_current_day()

    def compare_to_time(self, day: int, hour: int) -> int:
        """
        Compares game state's time to the provided day & hour.
        :return -1 if game state's time is before the provided time, 0 if they're the same, 1 if game state's time is after the given time.
        """
        this_game_time = self.game_state.day * 24 + self.game_state.hour
        other_game_time = day * 24 + hour
        if this_game_time < other_game_time:
            return -1
        elif this_game_time == other_game_time:
            return 0
        else:
            return 1

    def check_for_next_scene(self):
        """
        Checks if we've reached the cutoff time to transition to the next scene.
        :return (True, "scene_name") if it's time to transition, (False, "") if not.
        """
        trans_index = self.game_state.life_sim_iter - 1
        if trans_index < len(self.transitions):
            if self.compare_to_time(self.transitions[trans_index]["day"], self.transitions[trans_index]["hour"]) >= 0:
                return True, self.transitions[trans_index]["result"], self.transitions[trans_index]["scene"]
        return False, "", ""

    def highlight_key_dates(self):
        # for every key date given in self.key_dates, generate a label using UIResources.textbox (which is a transparent
        # bitmap) and add those labels to the labels group in order to be drawn to the screen
        # current day should have a different color outline to mark it as special
        day_width = CALENDAR_DIMENSIONS[0] // 8
        day_height = CALENDAR_DIMENSIONS[1] // 6
        # CALENDAR_OFFSET is the calendar's (x, y) position on the screen, where (x, y) is the top left of the image

        key_dates = [t["day"] for t in self.transitions if t["draw"]]

        for date in key_dates:
            calendar_pos = get_calendar_grid_pos(date)
            # highlight_box_pos is topleft=(x,y) of the day being highlit
            highlight_box_pos = [2 + CALENDAR_OFFSET[0] + (day_width * calendar_pos[0]),
                                 2 + CALENDAR_OFFSET[1] + (day_height * calendar_pos[1])]
            highlight = Label(highlight_box_pos[0], highlight_box_pos[1], day_width, day_height,
                              image=UIResources.textbox, border=True,
                              border_color=(254, 223, 0))
            self.labels.add(highlight)

    def highlight_current_day(self):
        # as above, but recalculate every time the day/hour is updated
        day_width = CALENDAR_DIMENSIONS[0] // 8
        day_height = CALENDAR_DIMENSIONS[1] // 6
        self.day_tracker.kill()
        calendar_pos = get_calendar_grid_pos(self.game_state.day)
        # highlight_box_pos is topleft=(x,y) of the day being highlit
        highlight_box_pos = [CALENDAR_OFFSET[0] + (day_width * calendar_pos[0]),
                             CALENDAR_OFFSET[1] + (day_height * calendar_pos[1])]
        self.day_tracker = Label(highlight_box_pos[0] + 2, highlight_box_pos[1] + 2, day_width, day_height,
                                 image=UIResources.textbox,
                                 border=True, border_color=(191, 0, 255))
        self.labels.add(self.day_tracker)

    def apply_favored_stat(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        if self.favored_stats[self.game_state.day - 1] == STAT_STR:
            self.game_state.strength += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_VIT:
            self.game_state.vitality += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_AGI:
            self.game_state.agility += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_INT:
            self.game_state.intelligence += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_CHARM:
            self.game_state.charm += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_MAGIC:
            self.game_state.magic += 1

    def adjust_stat_display(self, bonuses: List):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        if self.favored_stats[self.game_state.day - 1] == STAT_STR:
            bonuses[STR] += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_VIT:
            bonuses[VIT] += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_AGI:
            bonuses[AGI] += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_INT:
            bonuses[INT] += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_CHARM:
            bonuses[CHARM] += 1
        elif self.favored_stats[self.game_state.day - 1] == STAT_MAGIC:
            bonuses[MAGIC] += 1

        return bonuses

    def hover_house(self):
        adj = [1, 0, -1, 0, 2, 0]
        adj = self.adjust_stat_display(adj)
        stat_string = self.build_display_string(adj)
        stat_string += " Takes {} hours.".format(str(TIME_HOUSEKEEPING))
        self.textbox.update_text_and_speaker(stat_string, None)

    def hover_stalk(self):
        adj = [1, 1, 2, -1, -1, 0]
        adj = self.adjust_stat_display(adj)
        stat_string = self.build_display_string(adj)
        stat_string += " Takes {} hours.".format(str(TIME_STALKING))
        self.textbox.update_text_and_speaker(stat_string, None)

    def hover_study(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6
        adj = [-1, -1, -1, 2, 1, 1]
        adj = self.adjust_stat_display(adj)
        stat_string = self.build_display_string(adj)
        stat_string += " Takes {} hours.".format(str(TIME_STUDY))
        self.textbox.update_text_and_speaker(stat_string, None)

    def hover_exercise(self):
        adj = [2, 1, 1, -1, 1, -1]
        adj = self.adjust_stat_display(adj)
        stat_string = self.build_display_string(adj)
        stat_string += " Takes {} hours.".format(str(TIME_EXERCISE))
        self.textbox.update_text_and_speaker(stat_string, None)

    def hover_sharpen(self):
        adj = [-1, 1, 1, -1, 1, -1]
        adj = self.adjust_stat_display(adj)
        stat_string = self.build_display_string(adj)
        stat_string += " Takes {} hours.".format(str(TIME_SHARPEN))
        self.textbox.update_text_and_speaker(stat_string, None)

    def hover_research(self):
        adj = [-1, -1, 0, 0, 1, 2]
        adj = self.adjust_stat_display(adj)
        stat_string = self.build_display_string(adj)
        stat_string += " Takes {} hours.".format(str(TIME_RESEARCH))
        self.textbox.update_text_and_speaker(stat_string, None)

    def hover_rest(self):
        self.textbox.update_text_and_speaker("Take a nap to reduce stress. Decreases stats. Takes {} hours.".format(str(TIME_REST)),
                                             None)

    def hover_star(self):
        favor = ""
        if self.favored_stats[self.game_state.day - 1] == STAT_STR:
            favor = "strength"
        elif self.favored_stats[self.game_state.day - 1] == STAT_VIT:
            favor = "vitality"
        elif self.favored_stats[self.game_state.day - 1] == STAT_AGI:
            favor = "agility"
        elif self.favored_stats[self.game_state.day - 1] == STAT_INT:
            favor = "intellect"
        elif self.favored_stats[self.game_state.day - 1] == STAT_CHARM:
            favor = "charm"
        elif self.favored_stats[self.game_state.day - 1] == STAT_MAGIC:
            favor = "magic"

        self.textbox.update_text_and_speaker("Today the stars favor: {}".format(favor), None)

    # noinspection PyMethodMayBeStatic
    def build_display_string(self, stat_adjustments: List):
        first_half = ""
        second_half = ""
        string_part_list = []
        stat_names = ["strength", "vitality", "agility", "intellect", "charm", "magic"]

        for i in range(len(stat_adjustments)):
            if stat_adjustments[i] > 0:
                string_part_list.append("{stat} by {val:d}".format(stat=stat_names[i], val=stat_adjustments[i]))

        if len(string_part_list) > 0:
            first_half = "Increases {stats}.".format(stats=", ".join(string_part_list))

        # reset string_part_list
        string_part_list = []

        for i in range(len(stat_adjustments)):
            if stat_adjustments[i] < 0:
                string_part_list.append("{stat} by {val:d}".format(stat=stat_names[i], val=stat_adjustments[i]))

        if len(string_part_list) > 0:
            if len(first_half) > 0:
                second_half += " "
            second_half += "Decreases {stats}.".format(stats=", ".join(string_part_list))

        return first_half + second_half

    def perform_housekeeping(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.charm += 2
        self.game_state.strength += 1
        self.game_state.agility -= 1

        self.game_state.stress += random.randint(5, 10)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_HOUSEKEEPING)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)

        print("Debug: Housekeeping was clicked.")

    def perform_stalking(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.agility += 2
        self.game_state.vitality += 1
        self.game_state.strength += 1
        self.game_state.intelligence -= 1
        self.game_state.charm -= 1

        self.game_state.stress += random.randint(8, 13)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_STALKING)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)
        print("Debug: Stalking was clicked.")

    def perform_study(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.intelligence += 2
        self.game_state.charm += 1
        self.game_state.magic += 1
        self.game_state.vitality -= 1
        self.game_state.strength -= 1
        self.game_state.agility -= 1

        self.game_state.stress += random.randint(7, 11)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_STUDY)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)
        print("Debug: Study was clicked.")

    def perform_exercise(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.strength += 2
        self.game_state.vitality += 1
        self.game_state.agility += 1
        self.game_state.charm += 1
        self.game_state.intelligence -= 1
        self.game_state.magic -= 1

        self.game_state.stress += random.randint(10, 18)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_EXERCISE)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)
        print("Debug: Exercise was clicked.")

    def perform_sharpen(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.vitality += 2
        self.game_state.agility += 1
        self.game_state.charm += 1
        self.game_state.strength -= 1
        self.game_state.intelligence -= 1
        self.game_state.magic -= 1

        self.game_state.stress += random.randint(7, 11)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_SHARPEN)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)
        print("Debug: Sharpen was clicked.")

    def perform_research(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.magic += 2
        self.game_state.intelligence += 1
        self.game_state.strength -= 1
        self.game_state.vitality -= 1

        self.game_state.stress += random.randint(4, 9)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_RESEARCH)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)
        print("Debug: Research was clicked.")

    def perform_rest(self):
        # str vit agi int charm magic
        # 1    2   3   4    5    6

        self.game_state.strength -= 1
        self.game_state.vitality -= 1
        self.game_state.agility -= 1
        self.game_state.intelligence -= 1
        self.game_state.charm -= 1
        self.game_state.magic -= 1

        self.game_state.stress -= random.randint(35, 45)

        self.apply_favored_stat()
        self.validate_stats()
        self.advance_time(TIME_REST)

        results = ["Random1", "Random2", "Random3"]
        r = random.randint(0, 2)
        self.textbox.update_text_and_speaker(results[r], None)
        print("Debug: Rest was clicked.")

    def test_event(self):
        print("Button was clicked.")

    def loop(self):
        self.game_state.life_sim_iter += 1
        self.game_state.current_scene = "life_sim"
        self.star_popup.disable()
        self.result = ""
        self.highlight_current_day()

        # TODO: Make background image change depending on time of day, to help player keep track of the time.

        while True:

            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                for button in self.buttons:
                    button.handle_event(event)
                    self.star_popup.handle_event(event)
                    if self.result == "load":
                        return "load", "", ""
                    if self.result == "quit":
                        return "quit", "", ""
                    if self.result == "title":
                        return "title", "", ""

                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_SPACE]:
                        print("Spacebar pressed")
                        self.open_menu()
                        print("Result is " + self.result)
                        # if load or quit was selected
                        if self.result == "load":
                            return "load", "", ""
                        if self.result == "quit":
                            return "quit", "", ""
                        if self.result == "title":
                            return "title", "", ""

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.game_state.stress > 80:
                for button in self.buttons:
                    if button.enabled:
                        button.disable()
                if not self.restButton.enabled:
                    self.restButton.enable()
            else:
                for button in self.buttons:
                    if not button.enabled:
                        button.enable()

            # draw bg
            self.screen.blit(UIResources.backgrounds["city_background"], (0, 0))

            # draw stuff
            self.buttons.draw(self.screen)
            self.labels.draw(self.screen)
            self.stars.draw(self.screen)
            self.boxes.draw(self.screen)

            # update labels to reflect current game state
            self.stress_num.set_text(str(self.game_state.stress))
            self.str_num.set_text(str(self.game_state.strength))
            self.vit_num.set_text(str(self.game_state.vitality))
            self.int_num.set_text(str(self.game_state.intelligence))
            self.agi_num.set_text(str(self.game_state.agility))
            self.charm_num.set_text(str(self.game_state.charm))
            self.magic_num.set_text(str(self.game_state.magic))
            self.day_num.set_text(str(self.game_state.day))
            self.hour_num.set_text(str(self.game_state.hour))
            # testing purposes
            self.affection_num.set_text(str(self.game_state.affection))

            pygame.display.flip()
            self.clock.tick(40)

            should_transition, result, scene_name = self.check_for_next_scene()
            if should_transition:
                return result, scene_name, ""
