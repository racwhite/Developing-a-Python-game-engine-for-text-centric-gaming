import pygame

pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

NAME_LENGTH = 16


class UIResources:
    # textbox pieces
    text_topleft = pygame.image.load("images/curr/box_topleft.png").convert_alpha()
    text_middleleft = pygame.image.load("images/curr/box_middleleft.png").convert_alpha()
    text_bottomleft = pygame.image.load("images/curr/box_bottomleft.png").convert_alpha()
    text_bottommiddle = pygame.image.load("images/curr/box_bottommiddle2.png").convert_alpha()
    text_topright = pygame.image.load("images/curr/box_topright.png").convert_alpha()
    text_middleright = pygame.image.load("images/curr/box_middleright.png").convert_alpha()
    text_bottomright = pygame.image.load("images/curr/box_bottomright.png").convert_alpha()
    text_topmiddle = pygame.image.load("images/curr/box_topmiddle2.png").convert_alpha()
    text_middlemiddle = pygame.image.load("images/curr/box_middlemiddle.png").convert_alpha()
    text_nameplate = pygame.image.load("images/curr/Panel_Name.png").convert_alpha()
    text_ct = pygame.image.load("images/curr/Button_ContinueHL.png").convert_alpha()
    text_purp = pygame.image.load("images/curr/Button_Continue_P.png").convert_alpha()

    # special 100% transparent box
    textbox = pygame.image.load("images/curr/base_text.png").convert_alpha()

    # buttony bits
    testButtonInactive = pygame.image.load("images/curr/button_violet_inactive.png").convert_alpha()
    testButtonIdle = pygame.image.load("images/curr/button_violet_idle.png").convert_alpha()
    testButtonHot = pygame.image.load("images/curr/button_violet_hot.png").convert_alpha()
    testButtonActive = pygame.image.load("images/curr/button_violet_active.png").convert_alpha()
    testIcon = pygame.image.load("images/curr/claw_icon.png").convert_alpha()

    # dialogue option button bits
    dButtonIdle = pygame.image.load("images/curr/dialoguebutton_alt.png").convert_alpha()
    dButtonActive = pygame.image.load("images/curr/dialoguebutton_alt_active.png").convert_alpha()
    dButtonHot = pygame.image.load("images/curr/dialoguebutton_alt_hot.png").convert_alpha()

    # label pieces
    # TODO: replace with nice bitmap with alpha channel data
    testLabel = pygame.Surface((100, 100))
    testLabel.fill((128, 0, 128))

    calendar = pygame.image.load("images/curr/calendar_8.png").convert_alpha()

    backgrounds = {"city_background": pygame.image.load("images/curr/bg_small_donotuse.png").convert(),
                   "castle_interior": pygame.image.load("images/curr/temp_castle.png").convert(),
                   "paper": pygame.image.load("images/curr/paper_bg.png").convert(),
                   "ocean": pygame.image.load("images/curr/temp_ocean.jpg").convert()}

    # Access like characters["wizard"]["happy"]
    characters = {"clear": {"clear": textbox},
                  "wizard":
                      {"happy": pygame.image.load("images/curr/fantasy_wizard_happy.png").convert_alpha(),
                       "neutral": pygame.image.load("images/curr/fantasy_wizard.png").convert_alpha(),
                       "sad": pygame.image.load("images/curr/fantasy_wizard_sad.png").convert_alpha(),
                       "angry": pygame.image.load("images/curr/fantasy_wizard_angry.png").convert_alpha()},
                  "shopkeeper":
                      {"neutral": ":-|"},
                  }

    sounds = {"wizard_house": "placeholder",
              "beep": "i'm not a sound"}

    # city_background = pygame.image.load("images/curr/bg_small_donotuse.png")

    myriadProFont = pygame.font.SysFont("Myriad Pro", 24)


class InputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width=200, height=40, text="Default", is_active=False, image=UIResources.text_nameplate,
                 font=UIResources.myriadProFont,
                 aa=True,
                 text_color=(255, 255, 255), max_string_length=NAME_LENGTH):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = font
        self.aa = aa
        self.text_color = text_color
        self.max_len = max_string_length
        self.input_text = ""
        self.x = x
        self.y = y
        self.cursor_pos = 0
        self.input_group_list = []

        self.set_text(text)
        self.text_width, self.text_height = self.font.size("T")

        self.redraw_image = pygame.transform.scale(image, (width, height))
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # text surface
        # self.surface = pygame.transform.scale(UIResources.textbox, (200, 40))
        # self.surface.blit(self.image, (0, 0))

        self.is_active = is_active
        self.clicked = False

        # Display default name
        self.draw()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.clicked:
                self.is_active = True
                self.deactivate_others()
            self.clicked = False

        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_text()
            elif event.key == pygame.K_DELETE:
                self.delete_text()
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min((self.cursor_pos + 1), len(self.input_text))
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(self.cursor_pos - 1, 0)
            elif event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_TAB:
                pass
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.input_text)
            elif len(event.unicode) > 0:
                self.insert_text_at_cursor(event.unicode)

        self.draw()

    def get_rect(self):
        return self.rect

    def set_group_list(self, group_list):
        """Sets the list of InputBox controls that this is part of. Used for managing which is active."""
        self.input_group_list = group_list

    def deactivate_others(self):
        """
        Deactivates all other Input box controls in the current group.
        Assumed this is done when this box becomes active.
        """
        for input_box in self.input_group_list:
            if input_box != self:
                input_box.is_active = False

    def fix_text(self):
        """Helper method, makes sure text isn't too long based on max allowed length. Truncates it as necessary."""
        if len(self.input_text) > self.max_len:
            self.input_text = self.input_text[:self.max_len]
            if self.cursor_pos > len(self.input_text):
                self.cursor_pos = len(self.input_text)

    def set_text(self, new_text: str):
        """Sets the current input text to the given value, placing cursor at the end."""
        self.input_text = new_text
        self.cursor_pos = len(self.input_text)
        self.fix_text()

    def insert_text_at_cursor(self, new_text: str):
        """
        Adds the given character or string into current input text at cursor.
        Won't insert text once the text box is "full".
        """
        text_to_add = new_text
        while len(self.input_text) < self.max_len and len(text_to_add) > 0:
            self.input_text = self.input_text[:self.cursor_pos] + text_to_add[0] + self.input_text[self.cursor_pos:]
            self.cursor_pos += 1
            text_to_add = text_to_add[1:]

    def backspace_text(self):
        """Removes one character of text before the cursor."""
        if self.cursor_pos > 0:
            self.input_text = self.input_text[:self.cursor_pos - 1] + self.input_text[self.cursor_pos:]
            self.cursor_pos -= 1
            self.fix_text()

    def delete_text(self):
        """Deletes one character of text in front of the cursor."""
        if self.cursor_pos < len(self.input_text):
            self.input_text = self.input_text[:self.cursor_pos] + self.input_text[self.cursor_pos + 1:]
            self.fix_text()

    def get_text(self):
        """Get the actual "contents/value" of the text box."""
        return self.input_text

    def get_display_text(self):
        """
        Get a string with the "cursor" inserted into it, intended for display/drawing.
        Doesn't render cursor if not active.
        """
        display_text = self.input_text[:self.cursor_pos]
        if self.is_active:
            display_text += "|"
        display_text += self.input_text[self.cursor_pos:]
        return display_text

    def get_cursor_pos(self):
        return self.cursor_pos

    def clear_text(self):
        self.input_text = ""
        self.cursor_pos = 0

    def draw(self):
        text_surface = self.font.render(self.get_display_text(), self.aa, self.text_color)

        self.image.blit(self.redraw_image, (0, 0))
        self.image.blit(text_surface, (10, 10))


class TextBox(pygame.sprite.Sprite):

    def __init__(self, x=130, y=370, width=550, height=200, text="", font=UIResources.myriadProFont,
                 text_color=(255, 255, 255), full_image=UIResources.textbox, tl=UIResources.text_topleft,
                 ml=UIResources.text_middleleft, bl=UIResources.text_bottomleft, tm=UIResources.text_topmiddle,
                 mm=UIResources.text_middlemiddle, bm=UIResources.text_bottommiddle, tr=UIResources.text_topright,
                 mr=UIResources.text_middleright, br=UIResources.text_bottomright, ct=UIResources.text_ct, aa=True,
                 np=UIResources.text_nameplate, speaker=None, suppressarrow=False, purp=UIResources.text_purp):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = full_image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.font = font

        self.image = None
        self.rect = None
        self.trect = None
        self.speaker = speaker

        self.tl = tl
        self.ml = ml
        self.bl = bl
        self.bm = bm
        self.br = br
        self.mr = mr
        self.tr = tr
        self.tm = tm
        self.mm = mm
        self.np = np
        self.ct = pygame.transform.scale(ct, (20, 15))
        self.p = pygame.transform.scale(purp, (20, 15))

        self.cornerWidth = 30
        self.cornerHeight = 30
        self.borderThickness = 30

        self.label_padding = 10
        self.label_width = 0

        self.text = text
        self.aa = aa
        self.suppress = suppressarrow

        # trying some bullshit to make the arrow blink
        self.arrow_visible = True
        self.arrow_switch_ms = 1000  # every second
        self.arrow_counter_ms = 0

        self.update_ui()

    def update_ui(self):

        # base textbox image transformed to scale, should be a transparent rectangle
        self.image = pygame.transform.scale(self.base_image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # cover base image with textbox parts
        # reserve 50px at the top for the name plate

        centerWidth = self.width - (2 * self.cornerWidth)
        centerHeight = self.height - (2 * self.cornerHeight)
        minWidth = (self.cornerWidth * 2) + centerWidth
        minHeight = (self.cornerHeight * 2) + centerHeight

        middleWidth = self.width - (2 * self.cornerWidth)
        middleHeight = self.height - (3 * self.cornerHeight)

        # scale everything to fit
        mm_scaled = pygame.transform.scale(self.mm, (middleWidth, middleHeight))
        tl_scaled = pygame.transform.scale(self.tl, (self.cornerWidth, self.cornerHeight))
        ml_scaled = pygame.transform.scale(self.ml, (self.cornerWidth, centerHeight - 30))
        bl_scaled = pygame.transform.scale(self.bl, (self.cornerWidth, self.cornerHeight))
        bm_scaled = pygame.transform.scale(self.bm, (centerWidth, self.cornerHeight))
        br_scaled = pygame.transform.scale(self.br, (self.cornerWidth, self.cornerHeight))
        mr_scaled = pygame.transform.scale(self.mr, (self.cornerWidth, centerHeight - 30))
        tr_scaled = pygame.transform.scale(self.tr, (self.cornerWidth, self.cornerHeight))
        tm_scaled = pygame.transform.scale(self.tm, (centerWidth, self.cornerHeight))

        # begin the blitting
        # leave 30 pixel height at the top for adding in (optional) speaker label
        self.image.blit(ml_scaled, (0, self.cornerHeight + 30))

        self.image.blit(mr_scaled, (self.cornerWidth + centerWidth, self.cornerHeight + 30))
        self.image.blit(tm_scaled, (self.cornerWidth, 30))
        self.image.blit(mm_scaled, (self.cornerWidth, self.cornerHeight + 30))
        self.image.blit(bm_scaled, (self.cornerWidth, self.cornerHeight + centerHeight))

        self.image.blit(tl_scaled, (0, 30))
        self.image.blit(br_scaled, (self.cornerWidth + centerWidth, self.cornerHeight + centerHeight))
        self.image.blit(tr_scaled, (self.cornerWidth + centerWidth, 30))
        self.image.blit(bl_scaled, (0, self.cornerHeight + centerHeight))

        if self.speaker is not None:
            name_length = self.font.size(self.speaker)
            self.label_width = name_length[0] + self.label_padding

            np_scaled = pygame.transform.scale(self.np, (self.label_width + self.label_padding, 40))
            name_surf = self.font.render(self.speaker, True, self.text_color)
            image_center = np_scaled.get_rect()

            self.image.blit(np_scaled, (50, 15))
            self.image.blit(name_surf, (image_center[0] + 58, image_center[1] + 25))

        self.trect = mm_scaled.get_rect(topleft=(self.cornerWidth + 5, self.cornerHeight + 35))
        self.draw_text()

    def draw_text(self):
        # oh boy it's text time
        text_y = self.trect.top
        line_spacing = -2

        # get the height of the font
        font_height = self.font.size("Tg")[1]

        while self.text:
            i = 1

            # determine if the row of text will be outside the area
            if text_y + font_height > self.trect.bottom - 5:
                break

            # determine maximum width of line
            while self.font.size(self.text[:i])[0] < self.trect.width and i < len(self.text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(self.text):
                i = self.text.rfind(" ", 0, i) + 1

            rendered_text = self.font.render(self.text[:i], self.aa, self.text_color)

            self.image.blit(rendered_text, (self.trect.left, text_y))
            text_y += font_height + line_spacing

            # remove rendered text from line and repeat
            self.text = self.text[i:]

        return self.text

    def update_every_frame(self, time):
        # blit the arrow, or blit a purple square to cover the arrow on redraw
        if not self.suppress and self.arrow_visible:
            self.image.blit(self.ct, (self.trect.right - 20, self.trect.bottom - 20))
        elif not self.suppress and not self.arrow_visible:
            self.image.blit(self.p, (self.trect.right - 20, self.trect.bottom - 20))

        # toggle arrow on and off based on time passed since the last frame
        self.arrow_counter_ms += time
        if self.arrow_counter_ms >= self.arrow_switch_ms:
            self.arrow_counter_ms %= self.arrow_switch_ms
            self.arrow_visible = not self.arrow_visible

    def update_text_and_speaker(self, text, speaker):
        self.text = text
        self.speaker = speaker
        self.update_ui()


class Label(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, text="", font=UIResources.myriadProFont,
                 text_color=(255, 255, 255), image=UIResources.testLabel, border=False, border_width=1,
                 border_color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = image
        self.image = None
        self.rect = None
        self.border = border
        self.border_width = border_width
        self.border_color = border_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.text_color = text_color

        self.update_ui()

    def update_ui(self):
        self.image = pygame.transform.scale(self.base_image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if self.border:
            pygame.draw.rect(self.image, self.border_color,
                             (0, 0,
                              self.width, self.height), self.border_width)

        # put text on label
        image_center = self.image.get_rect().center
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(image_center[0], image_center[1]))
        self.image.blit(text_surf, text_rect)

    def set_text(self, text):
        self.text = text
        self.update_ui()

    def set_image(self, new_image):
        self.base_image = new_image
        self.update_ui()


class Button(pygame.sprite.Sprite):

    # pass in x and y position, reference to Scene's event, size, and images to draw itself with
    def __init__(self, x, y, width, height, callevent, text="", font=UIResources.myriadProFont, text_color=(0, 0, 0),
                 disabled=UIResources.testButtonInactive, idle=UIResources.testButtonIdle,
                 hot=UIResources.testButtonHot, active=UIResources.testButtonActive, icon=None):
        pygame.sprite.Sprite.__init__(self)
        self.base_idle = idle
        self.base_active = active
        self.base_hot = hot
        self.base_disabled = disabled
        self.base_icon = icon

        self.image = None
        self.idle = None
        self.active = None
        self.hot = None
        self.disabled = None
        self.rect = None
        self.icon = None

        self.text = text
        self.font = font
        self.text_color = text_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.enabled = True
        self.clicked = False

        self.callevent = callevent
        self.update_ui()

    def update_ui(self):
        self.active = pygame.transform.scale(self.base_active, (self.width, self.height))
        self.disabled = pygame.transform.scale(self.base_disabled, (self.width, self.height))
        self.hot = pygame.transform.scale(self.base_hot, (self.width, self.height))
        self.idle = pygame.transform.scale(self.base_idle, (self.width, self.height))

        self.rect = self.idle.get_rect(topleft=(self.x, self.y))

        image_center = self.idle.get_rect().center
        # put icon on button
        if self.base_icon is not None:
            self.icon = pygame.transform.scale(self.base_icon, (self.width, self.height))
            icon_rect = self.icon.get_rect(center=image_center)
            for button in (self.active, self.hot, self.idle):
                button.blit(self.icon, icon_rect)

        # put text on button
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=image_center)
        for image in (self.active, self.disabled, self.hot, self.idle):
            image.blit(text_surf, text_rect)

        self.image = self.idle

    def handle_event(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.image = self.active
                    self.clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos) and self.clicked:
                    self.callevent()
                    self.image = self.hot
                self.clicked = False
            elif event.type == pygame.MOUSEMOTION:
                collided = self.rect.collidepoint(event.pos)
                if collided and not self.clicked:
                    self.image = self.hot
                elif not collided:
                    self.image = self.idle

    def disable(self):
        self.image = self.disabled
        self.enabled = False

    def enable(self):
        # self.image = self.idle
        self.enabled = True
        self.update_ui()

    def set_text(self, text):
        self.text = text
        self.update_ui()

    def set_icon(self, icon):
        self.icon = icon
        self.update_ui()


class ActionButton(Button):
    def __init__(self, x, y, width, height, callevent, hoverevent, text="", font=UIResources.myriadProFont,
                 text_color=(0, 0, 0), disabled=UIResources.testButtonInactive, idle=UIResources.testButtonIdle,
                 hot=UIResources.testButtonHot, active=UIResources.testButtonActive, icon=None):
        Button.__init__(self, x, y, width, height, callevent, text, font, text_color, disabled, idle, hot, active, icon)

        self.hoverevent = hoverevent

    def handle_event(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.image = self.active
                    self.clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos) and self.clicked:
                    self.image = self.hot
                    self.callevent()
                self.clicked = False
            elif event.type == pygame.MOUSEMOTION:
                collided = self.rect.collidepoint(event.pos)
                if collided and not self.clicked:
                    self.image = self.hot
                    self.hoverevent()
                elif not collided:
                    self.image = self.idle


class DecisionButton(pygame.sprite.Sprite):
    # pass in x and y position, reference to Scene's event, size, and images to draw itself with
    def __init__(self, x, y, callevent, jumptag=None, width=None, height=None, text="", font=UIResources.myriadProFont,
                 text_color=(255, 255, 255),
                 disabled=UIResources.textbox, idle=UIResources.dButtonIdle,
                 hot=UIResources.dButtonHot, active=UIResources.dButtonActive,
                 auto_center_pos=True):
        pygame.sprite.Sprite.__init__(self)
        self.base_idle = idle
        self.base_active = active
        self.base_hot = hot
        self.base_disabled = disabled

        self.image = None
        self.idle = None
        self.active = None
        self.hot = None
        self.disabled = None
        self.rect = None
        self.icon = None

        self.text = text
        self.font = font
        self.text_color = text_color
        self.original_x = x
        self.x = x
        self.original_y = y
        self.y = y
        self.original_width = width
        self.original_height = height
        self.width = 150 if width is None else width
        self.height = 50 if height is None else height
        self.padding = 25
        self.auto_center_pos = auto_center_pos

        self.enabled = False
        self.clicked = False
        self.jumptag = jumptag
        self.callevent = callevent
        self.update_ui()

    def update_ui(self):
        text_size = self.font.size(self.text)
        if self.original_width is None:
            self.width = text_size[0] + self.padding
        if self.original_height is None:
            self.height = text_size[1] + self.padding
        if self.auto_center_pos:
            self.x = self.original_x - (self.width // 2)
            self.y = self.original_y - (self.height // 2)
        self.active = pygame.transform.scale(self.base_active, (self.width, self.height))
        self.disabled = pygame.transform.scale(self.base_disabled, (self.width, self.height))
        self.hot = pygame.transform.scale(self.base_hot, (self.width, self.height))
        self.idle = pygame.transform.scale(self.base_idle, (self.width, self.height))

        self.rect = self.idle.get_rect(topleft=(self.x, self.y))

        image_center = self.idle.get_rect().center

        # put text on button
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=image_center)
        for image in (self.active, self.hot, self.idle):
            image.blit(text_surf, text_rect)

        if self.enabled:
            self.image = self.idle
        else:
            self.image = self.disabled

    def handle_event(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.image = self.active
                    self.clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos) and self.clicked:
                    self.image = self.hot
                    self.callevent(self.jumptag)
                self.clicked = False
            elif event.type == pygame.MOUSEMOTION:
                collided = self.rect.collidepoint(event.pos)
                if collided and not self.clicked:
                    self.image = self.hot
                elif not collided:
                    self.image = self.idle

    def disable(self):
        self.image = self.disabled
        self.text = ""
        self.enabled = False
        self.update_ui()

    def enable(self, text, jumptag):
        self.image = self.idle
        self.jumptag = jumptag
        self.text = text
        self.enabled = True
        self.update_ui()

    def set_text(self, text):
        self.text = text
        self.update_ui()
