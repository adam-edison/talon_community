mode: user.game
tag: user.game_subnautica
-

settings():
    key_hold = 8
    key_wait = 16

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

# secondary mapped in game
# U = mouse click = use
parrot(kuh): key(u)

harvest: key(u:5)

(bail out | bailout):
    key(5)
    sleep(15ms)
    user.mouse_right_hold(5000)

