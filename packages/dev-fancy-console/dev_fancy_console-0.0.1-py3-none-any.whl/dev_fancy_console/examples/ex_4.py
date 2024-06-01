def example_4():
    from dev_fancy_console.presets import FancyColors, FancyBackgroundColors, FancyStyles
    from dev_fancy_console import FancyMessage, FancyMessageSegmented
    print("[[EXAMPLE_4: Segmented Print]]")
    print(FancyMessageSegmented([FancyMessage(message="TEST:", color=FancyColors.BLACK,
                                              background=FancyBackgroundColors.WHITE_BG, styles=[FancyStyles.BOLD]),
                                 FancyMessage(message="MESSAGE:", color=FancyColors.RED_HI),
                                 FancyMessage(message="STEP", color=FancyColors.RANDOM(),
                                              background=FancyBackgroundColors.RANDOM_BG())
                                 ]).compose_segment_message)
