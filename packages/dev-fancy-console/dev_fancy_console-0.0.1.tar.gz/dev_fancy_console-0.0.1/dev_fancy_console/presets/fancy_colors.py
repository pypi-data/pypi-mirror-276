import random


class FancyColors:
    # EMPTY
    EMPTY: str = ""

    # Regular Colors
    BLACK: str = '\033[30m'
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    BLUE: str = '\033[34m'
    MAGENTA: str = '\033[35m'
    CYAN: str = '\033[36m'
    WHITE: str = '\033[37m'
    GRAY: str = '\033[90m'

    # High Intensity Colors
    BLACK_HI: str = '\033[90m'
    RED_HI: str = '\033[91m'
    GREEN_HI: str = '\033[92m'
    YELLOW_HI: str = '\033[93m'
    BLUE_HI: str = '\033[94m'
    MAGENTA_HI: str = '\033[95m'
    CYAN_HI: str = '\033[96m'
    WHITE_HI: str = '\033[97m'
    GRAY_HI: str = '\033[37m'

    @staticmethod
    def RANDOM() -> str:
        colors = [color for color in dir(FancyColors) if isinstance(getattr(FancyColors, color), str) and not color.startswith("__")]
        return getattr(FancyColors, random.choice(colors))

