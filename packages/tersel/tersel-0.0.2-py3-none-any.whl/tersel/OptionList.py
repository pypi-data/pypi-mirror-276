from tersel import Option


class OptionList:
    def __init__(self, options: [any], option_identifier: str = "[{index}] "):
        self.option_identifier = option_identifier
        self.options: [Option] = self.get_options(options)

    def get_options(self, options: [any], indent_level: int = 0) -> [Option]:
        option_list: [Option] = []
        for i, option in enumerate(options):
            if isinstance(option, (list, tuple)):
                option_list += self.get_options(option, indent_level + 1)
            else:
                option_list.append([Option(str(option), self.option_identifier, indent_level)])

        return option_list

    def to_list(self) -> list[Option]:
        return [option for nested_options in self.options for option in nested_options]
