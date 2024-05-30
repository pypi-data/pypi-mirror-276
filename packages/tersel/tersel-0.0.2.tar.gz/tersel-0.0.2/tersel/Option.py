class Option:
    def __init__(self, text: str, option_identifier: str = '[{index}]', indent_level: int = 0):
        self.text: str = text
        self.option_identifier: str = option_identifier
        self.indent_level: int = indent_level

    def __str__(self) -> str:
        return self.option_identifier + " -- " * self.indent_level + self.text
