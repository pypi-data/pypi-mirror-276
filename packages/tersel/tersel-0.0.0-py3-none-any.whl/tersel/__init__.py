import os
import warnings

import keyboard
from colorama import Fore, Style
from colorama import init as colorama_init


class Tersel:
    def __init__(self, title: str, options: [any], max_options_shown: int = 5, line_start: str = "[{index}] ",
                 title_color: str = Fore.GREEN, option_color: str = Fore.LIGHTBLACK_EX,
                 selected_color: str = Fore.LIGHTCYAN_EX):
        """
        :param title: Text shown above the options
        :param options: All possible options, can be any type that has a __str__ method
        :param max_options_shown: Maximum number of options shown before scrolling
        :param line_start: Text shown before each option, option number can be added using {index}
        :param title_color: Colorama color for title
        :param option_color: Colorama color for options
        :param selected_color: Colorama color of selected option
        """
        self.title: str = title
        self.options: [any] = options
        self.max_options_shown = max_options_shown
        self.selected: int = 0
        self.line_start = line_start
        self.title_color = title_color
        self.option_color = option_color
        self.selected_color = selected_color

        self.clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

        self.check_validity()
        colorama_init()

    def check_validity(self) -> bool:
        """
        Checks whether all parameters are valid
        :return: bool indicating of all checks passed
        """
        passed = True

        if len(self.title.strip()) == 0:
            passed = False
            warnings.warn("'title' should not be empty!")

        if len(self.options) <= 1:
            passed = False
            warnings.warn("'options' should have more than 1 entry")

        return passed

    def show(self, clear: bool = True) -> any:
        """
        Shows the option dialog
        :return: the chosen object from the options list
        """

        self.draw_options(clear)
        keyboard.on_press_key("up arrow", lambda _: self.on_arrow_up())
        keyboard.on_press_key("down arrow", lambda _: self.on_arrow_down())
        keyboard.on_press_key("right arrow", lambda _: keyboard.press('enter'))
        input()

        return self.options[self.selected]

    def on_arrow_up(self):
        if self.selected != 0:
            self.selected -= 1
        self.draw_options()

    def on_arrow_down(self):
        if len(self.options) - 1 > self.selected:
            self.selected += 1
        self.draw_options()

    def draw_options(self, clear: bool = True):
        if clear:
            self.clear()

        self.print_line(f"{self.title_color}{self.title}")
        for i, option in enumerate(self.options):
            text = f"{self.line_start}{option}"
            self.print_line(text.format(index=i + 1), i == self.selected)

    def print_line(self, text: str, selected: bool = False):
        print(f"\n{self.selected_color if selected is True else self.option_color}{text}", end=Style.RESET_ALL)
