mode: command
mode: dictation
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    user.gdb_disable()
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
    app.notify("Command mode enabled")
^game mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("user.game")
    app.notify("Game mode enabled")
