mode: command
mode: dictation
-
# Left click (universal)
parrot(clop): mouse_click(0)

# Enter (universal)
parrot(tih): key(enter)

# Tab (universal)
parrot(puh): key(tab)

# Scrolling sounds
parrot(sss):      user.sound_scroll_up_start(300)
parrot(sss:stop): user.sound_scroll_up_stop()
parrot(shh):      user.sound_scroll_down_start(300)
parrot(shh:stop): user.sound_scroll_down_stop()

# sound scroll speed control
scroll double: user.sound_scroll_speed_multiply(2.0)
scroll half: user.sound_scroll_speed_multiply(0.5)

# Command/dictation toggle
parrot(whistle:stop): user.workflow_toggle_command_dictation()

# Left drag toggle with notifications
parrot(cha): user.workflow_toggle_left_drag()

# Copy / paste
parrot(wince): edit.copy()
parrot(spit): edit.paste()
