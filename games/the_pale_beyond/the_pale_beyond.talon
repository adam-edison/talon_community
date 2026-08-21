win.title: /The Pale Beyond/i
mode: user.game
-
tag(): user.game_reserves_parrot_sounds

settings():
    user.parrot_config_combo_window = 1000

# Arrow keys - single sounds (no parrot_config needed)
# sss:stop   -> up
# shh:stop   -> down
# kuh        -> left
# puh        -> right
parrot(sss:stop): key(up)
parrot(shh:stop): key(down)
parrot(kuh): key(left)
parrot(puh): key(right)

# Menu - double noise
# spit spit -> escape
parrot(spit): user.parrot_config_noise("spit")
parrot(clop): key(space)

# Voice commands
quench: key(q)
each: key(e)
