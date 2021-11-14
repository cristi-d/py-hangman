import os
from typing import List


class Renderer:
    def render(self, hits: int, revealed: List[str], attempts: List[str]):
        with open("resources/scene-{}.txt".format(hits), "rt") as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                to_print = line
                if i == 7:
                    to_print = line.replace("{}", "".join(revealed))
                if i == 9:
                    to_print = line.replace("{}", "Attempts: " + ", ".join(attempts).upper())

                print(to_print, end='')
        print()

    def render_round_input_query(self):
        print("Guess (or 'quit'/'exit'): ", end='')

    def render_game_over(self):
        print("Game over :(")
        print("Press any key to continue or type 'exit' to close")

    def render_game_win(self):
        print("You won ! :)")
        print("Press any key to continue or type 'exit' to close")


    def render_quit_message(self):
        print("Press any key to start a new game or type 'exit' to close")


    def render_no_words(self):
        print("No words found. Exiting")

    def clear_screen(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
        print()