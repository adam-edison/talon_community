mode: user.game
tag: user.game_subnautica
-

^subnautica off$:
    user.game_subnautica_disable()
    app.notify("Subnautica commands disabled")

running: key(w:down)
stop: key(w:up)

one: key(1)
two: key(2)
three: key(3)
four: key(4)
five: key(5)

word <user.word>: insert(word)

parrot(clop): key(tab)
