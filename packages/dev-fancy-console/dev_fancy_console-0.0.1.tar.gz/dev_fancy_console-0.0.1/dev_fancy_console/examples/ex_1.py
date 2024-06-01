
def example_1() -> None:
    from dev_fancy_console.presets import FancyColors, FancyUtilities, FancyBackgroundColors, FancyStyles
    print("[[EXAMPLE_1:]]")
    print('-->FancyColors<--')
    print("(Regular Colors):")
    print(f"{FancyColors.BLACK}BLACK{FancyUtilities.RESET} "
          f"{FancyColors.RED}RED{FancyUtilities.RESET} "
          f"{FancyColors.GREEN}GREEN{FancyUtilities.RESET} "
          f"{FancyColors.YELLOW}YELLOW{FancyUtilities.RESET} "
          f"{FancyColors.BLUE}BLUE{FancyUtilities.RESET} "
          f"{FancyColors.MAGENTA}MAGENTA{FancyUtilities.RESET} "
          f"{FancyColors.CYAN}CYAN{FancyUtilities.RESET} "
          f"{FancyColors.WHITE}WHITE{FancyUtilities.RESET} "
          f"{FancyColors.GRAY}GRAY{FancyUtilities.RESET}"
          )
    print("(High Intensity Colors):")
    print(f"{FancyColors.BLACK_HI}BLACK{FancyUtilities.RESET} "
          f"{FancyColors.RED_HI}RED{FancyUtilities.RESET} "
          f"{FancyColors.GREEN_HI}GREEN{FancyUtilities.RESET} "
          f"{FancyColors.YELLOW_HI}YELLOW{FancyUtilities.RESET} "
          f"{FancyColors.BLUE_HI}BLUE{FancyUtilities.RESET} "
          f"{FancyColors.MAGENTA_HI}MAGENTA{FancyUtilities.RESET} "
          f"{FancyColors.CYAN_HI}CYAN{FancyUtilities.RESET} "
          f"{FancyColors.WHITE_HI}WHITE{FancyUtilities.RESET} "
          f"{FancyColors.GRAY_HI}GRAY{FancyUtilities.RESET}"
          )
    print()
    print('-->FancyBackgroundColors<--')
    print("(Regular Colors):")
    print(f"{FancyBackgroundColors.BLACK_BG}BLACK{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.RED_BG}RED{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.GREEN_BG}GREEN{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.YELLOW_BG}YELLOW{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.BLUE_BG}BLUE{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.MAGENTA_BG}MAGENTA{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.CYAN_BG}CYAN{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.WHITE_BG}WHITE{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.GRAY_BG}GRAY{FancyUtilities.RESET}"
          )
    print("(High Intensity Colors):")
    print(f"{FancyBackgroundColors.BLACK_BG_HI}BLACK{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.RED_BG_HI}RED{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.GREEN_BG_HI}GREEN{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.YELLOW_BG_HI}YELLOW{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.BLUE_BG_HI}BLUE{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.MAGENTA_BG_HI}MAGENTA{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.CYAN_BG_HI}CYAN{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.WHITE_BG_HI}WHITE{FancyUtilities.RESET} "
          f"{FancyBackgroundColors.GRAY_BG_HI}GRAY{FancyUtilities.RESET}"
          )
    print()
    print('-->FancyStyles<--')
    print(f"{FancyStyles.BOLD}BOLD{FancyUtilities.RESET} "
          f"{FancyStyles.DIM}DIM{FancyUtilities.RESET} "
          f"{FancyStyles.ITALIC}ITALIC{FancyUtilities.RESET} "
          f"{FancyStyles.STRIKETHROUGH}STRIKETHROUGH{FancyUtilities.RESET}"
          )
