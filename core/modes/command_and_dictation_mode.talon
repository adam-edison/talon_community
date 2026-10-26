mode: command
mode: dictation
-

^dictation mode$:
    user.dictation_mode()
    app.notify("Dictation mode enabled")
^command mode$:
    user.command_mode()
    app.notify("Command mode enabled")
^mixed mode$: user.mixed_mode()
^game mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("user.game")
    app.notify("Game mode enabled")
