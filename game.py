from enum import Enum
import random
from typing import List

from renderer import Renderer
from word import Word


class GameState(Enum):
    MAIN_MENU = 1
    START_GAME = 2
    ROUND_BEGIN = 3
    ROUND_AWAIT_INPUT = 4
    GAME_WIN = 5
    GAME_OVER = 6
    GAME_AWAIT_INPUT = 7
    GAME_QUIT = 8
    EXIT = 9


class Game:
    def __init__(self, raw_words: List[str], max_hits: int, renderer: Renderer):
        self._state = GameState.START_GAME
        self._hits = 0
        self._max_hits = max_hits
        self._word = None
        self._raw_words = raw_words
        self._attempts = set()
        self._renderer = renderer

        self._state_handlers = {
            GameState.START_GAME: self.handle_game_start,
            GameState.ROUND_BEGIN: self.handle_round_begin,
            GameState.ROUND_AWAIT_INPUT: self.handle_round_await_input,
            GameState.GAME_WIN: self.handle_game_win,
            GameState.GAME_OVER: self.handle_game_over,
            GameState.GAME_QUIT: self.handle_game_quit,
            GameState.GAME_AWAIT_INPUT: self.handle_game_await_input
        }

    def requires_input(self,) -> bool:
        state = self._state
        return state == GameState.ROUND_AWAIT_INPUT or state == GameState.GAME_AWAIT_INPUT

    def should_exit(self) -> bool:
        return self._state == GameState.EXIT

    def loop(self, user_input: str = None) -> GameState:
        handler = self._state_handlers[self._state]

        self._state = handler(user_input)

        return self._state

    def handle_game_start(self, user_input: str = None) -> GameState:
        self._word = Word(random.choice(self._raw_words))
        self._attempts = set()
        self._hits = 0

        return GameState.ROUND_BEGIN

    def handle_round_begin(self, user_input: str = None) -> GameState:
        self._renderer.clear_screen()
        self._renderer.render(self._hits, self._word.revealed, self._attempts)
        self._renderer.render_round_input_query()

        return GameState.ROUND_AWAIT_INPUT

    def handle_round_await_input(self, user_input: str) -> GameState:
        if user_input is None or user_input.strip() == "":
            return GameState.ROUND_AWAIT_INPUT

        if user_input.lower() == "quit":
            return GameState.GAME_QUIT

        if user_input.lower() == "exit":
            return GameState.EXIT

        if len(user_input) > 1:
            return GameState.ROUND_AWAIT_INPUT

        self._attempts.add(user_input)
        did_match, revealed = self._word.reveal(user_input)

        if not did_match:
            self._hits += 1

        self._renderer.clear_screen()
        self._renderer.render(self._hits, self._word.revealed, self._attempts)

        if self._word.is_complete:
            return GameState.GAME_WIN

        if self._hits >= self._max_hits:
            return GameState.GAME_OVER

        return GameState.ROUND_BEGIN

    def handle_game_win(self, user_input: str = None) -> GameState:
        self._renderer.render_game_win()

        return GameState.GAME_AWAIT_INPUT

    def handle_game_over(self, user_input: str = None) -> GameState:
        self._renderer.render_game_over()

        return GameState.GAME_AWAIT_INPUT

    def handle_game_await_input(self, user_input: str) -> GameState:
        if user_input == "exit":
            return GameState.EXIT

        return GameState.START_GAME

    def handle_game_quit(self, user_input: str = None) -> GameState:
        self._renderer.render_quit_message()

        return GameState.GAME_AWAIT_INPUT