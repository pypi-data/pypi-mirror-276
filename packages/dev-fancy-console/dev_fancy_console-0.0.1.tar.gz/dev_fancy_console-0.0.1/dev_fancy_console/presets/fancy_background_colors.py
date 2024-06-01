import random


class FancyBackgroundColors:
    # EMPTY
    EMPTY_BG: str = ""

    # Background Colors
    BLACK_BG: str = '\033[40m'
    RED_BG: str = '\033[41m'
    GREEN_BG: str = '\033[42m'
    YELLOW_BG: str = '\033[43m'
    BLUE_BG: str = '\033[44m'
    MAGENTA_BG: str = '\033[45m'
    CYAN_BG: str = '\033[46m'
    WHITE_BG: str = '\033[47m'
    GRAY_BG: str = '\033[100m'

    # High Intensity Background Colors
    BLACK_BG_HI: str = '\033[100m'
    RED_BG_HI: str = '\033[101m'
    GREEN_BG_HI: str = '\033[102m'
    YELLOW_BG_HI: str = '\033[103m'
    BLUE_BG_HI: str = '\033[104m'
    MAGENTA_BG_HI: str = '\033[105m'
    CYAN_BG_HI: str = '\033[106m'
    WHITE_BG_HI: str = '\033[107m'
    GRAY_BG_HI: str = '\033[47m'

    # HACK FIX
    @staticmethod
    def RANDOM_BG() -> str:
        colors = [color for color in dir(FancyBackgroundColors) if isinstance(getattr(FancyBackgroundColors, color), str) and not color.startswith("__")]
        return getattr(FancyBackgroundColors, random.choice(colors))
