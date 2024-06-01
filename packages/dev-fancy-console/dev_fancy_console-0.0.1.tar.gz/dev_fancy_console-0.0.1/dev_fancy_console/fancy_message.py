from typing import List

from dev_fancy_console.presets import FancyColors, FancyBackgroundColors, FancyStyles, FancyUtilities


class FancyMessage:
    def __init__(self, message: str, color: str = FancyColors.EMPTY,
                 background: str = FancyBackgroundColors.EMPTY_BG,
                 styles=None,
                 utility: str = FancyUtilities.RESET):
        if styles is None:
            styles = [FancyStyles.EMPTY_STYLE]
        self.message = message
        self.color = color
        self.background = background
        self.styles = styles
        self.utility = utility

    @property
    def compose_message(self) -> str:
        return f"{self.color}{self.background}{''.join([style for style in self.styles])}{self.message}{self.utility}"


print(FancyMessage(message="Message", color=FancyColors.EMPTY, background=FancyBackgroundColors.EMPTY_BG,
                   styles=[FancyStyles.EMPTY_STYLE], utility=FancyUtilities.EMPTY))


class FancyMessageSegmented:
    def __init__(self, fancy_messages: List[FancyMessage]):
        self.fancy_messages = fancy_messages

    @property
    def compose_segment_message(self) -> str:
        final_message: str = ''
        shift: int = 0

        for index, fancy_message in enumerate(self.fancy_messages):
            final_message += fancy_message.compose_message
            if index < len(self.fancy_messages) - 1:
                shift += len(fancy_message.message)
                final_message += f'\n{" " * shift}'
        return final_message
