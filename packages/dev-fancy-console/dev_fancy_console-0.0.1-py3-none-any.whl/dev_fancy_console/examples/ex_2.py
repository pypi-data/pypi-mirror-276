
def example_2() -> None:
    from dev_fancy_console import FancyMessage
    from dev_fancy_console.presets import FancyColors, FancyBackgroundColors, FancyStyles
    print("[[EXAMPLE_2:DEFAULT MESSAGE COMPOSE FUNCTION EXAMPLES]]")
    print(FancyMessage("DEFAULT MESSAGE").compose_message)
    print(FancyMessage("SIMPLE MESSAGE COMPOSE", color=FancyColors.BLACK,
                       background=FancyBackgroundColors.WHITE_BG).compose_message)
    print(
        f'{FancyMessage("MIX MESSAGE ", color=FancyColors.BLACK, background=FancyBackgroundColors.MAGENTA_BG_HI).compose_message}'
        f'{FancyMessage("COMPOSE + STYLE", color=FancyColors.GREEN_HI, background=FancyBackgroundColors.YELLOW_BG, styles=[FancyStyles.BOLD, FancyStyles.ITALIC]).compose_message}')
