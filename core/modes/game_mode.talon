mode: user.game
-

^command mode$:
    mode.disable("user.game")
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
    app.notify("Command mode enabled")
