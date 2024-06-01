def example_3(steps: int) -> None:
    from dev_fancy_console import FancyMessage
    from dev_fancy_console.presets import FancyColors, FancyBackgroundColors, FancyStyles
    print("[[EXAMPLE_3: RANDOM LOOP EXAMPLE FOR FUN]]")
    while steps > 0:
        print(FancyMessage(f"RANDOM REVERSE COUNTDOWN: {str(steps)}", color=FancyColors.RANDOM(),
                           background=FancyBackgroundColors.RANDOM_BG(),
                           styles=[FancyStyles.DIM]).compose_message)
        steps -= 1
