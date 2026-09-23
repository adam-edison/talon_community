mode: user.game
tag: user.game_subnautica
-

^subnautica off$:
    user.game_subnautica_disable()
    app.notify("Subnautica commands disabled")

full speed ahead: key(w:down)
full stop: key(w:up)

parrot(clop): key(tab)
