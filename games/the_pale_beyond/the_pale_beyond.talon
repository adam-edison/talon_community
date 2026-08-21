win.title: /The Pale Beyond/i
mode: user.game
-
tag(): user.game_reserves_parrot_sounds

settings():
    key_wait = 30
    user.parrot_config_combo_window = 1000

parrot(sss:stop): key(up)
parrot(shh:stop): key(down)
parrot(kuh): key(left)
parrot(puh): key(right)

parrot(whistle:stop): key(c)
parrot(cha:stop): key(q)
parrot(motor:stop): key(e)

parrot(wince): user.the_pale_beyond_toggle_ctrl()

parrot(spit): user.parrot_config_noise("spit")
parrot(clop): key(space)

quench: key(q)
each: key(e)
tab: key(tab)

ending:
    key(e:down)
    sleep(3000ms)
    key(e:up)
