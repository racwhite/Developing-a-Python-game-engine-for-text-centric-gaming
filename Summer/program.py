import pygame

pygame.init()
windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)

from typing import List
from sceneManager import *


class ScriptCommand:

    def __init__(self, command: str, args: List[str]):
        self.command = command
        self.args = args

    def print(self):
        print("Command: " + self.command)
        print("Arguments: ")
        print(" ".join(self.args))
        print("\n")


def parse_script():
    file_in = open("script.txt", "r")

    # assumes that first command will always be a type s in order to set first key
    # probably want to make that safer later
    scene_commands = {}

    key = ""
    for line in file_in:
        line = line.strip()
        if len(line) == 0:
            continue
        command = line[0:line.find(" ")]
        line = line[line.find(" "):]
        if command == "#":
            continue
        arguments = re.findall(r'{([^}]*?)}', line)

        if command == "s":
            key = arguments[0]

        script_command = ScriptCommand(command, arguments)

        if key in scene_commands:
            scene_commands[key].append(script_command)
        else:
            scene_commands[key] = [script_command]

    return scene_commands


if __name__ == "__main__":
    script = parse_script()
    scene_manager = SceneManager(screen, script)
    scene_manager.loop()
    pygame.quit()
    sys.exit()
