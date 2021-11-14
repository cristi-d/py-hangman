import sys
import os
from typing import List

from game import Game
from renderer import Renderer


def load_words() -> List[str]:
    words = []
    with open("resources/words.txt", "rt") as f:
        words = [line.strip() for line in f.readlines()]

    return words


def check_scenes_and_get_max_hits() -> int:
    scene_names = [scene_file_name for scene_file_name in os.listdir("resources/") if "scene-" in scene_file_name]

    missing_scenes = []
    for i in range(0, len(scene_names)):
        expected_scene_name = f"scene-{i}.txt"
        if expected_scene_name not in scene_names:
            missing_scenes += [expected_scene_name]

    if len(missing_scenes) > 0:
        raise ValueError("Missing scenes: " + ", ".join(missing_scenes))

    return len(scene_names) - 1


if __name__ == '__main__':

    renderer = Renderer()
    raw_words = load_words()
    max_hits = check_scenes_and_get_max_hits()

    if len(raw_words) == 0:
        renderer.render_no_words()
        sys.exit(1)

    game = Game(raw_words, max_hits, renderer)

    while True:
        user_input = None
        if game.requires_input():
            user_input = input()

        game.loop(user_input)

        if game.should_exit():
            sys.exit(0)
