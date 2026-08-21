win.title: /The Pale Beyond/i
mode: user.game
-
tag(): user.game_reserves_parrot_sounds

settings():
    user.parrot_config_combo_window = 1000

# Parrot noises - double noise within 1 second to trigger
# sss:stop sss:stop -> up (arrow key)
# shh:stop shh:stop -> down (arrow key)
# kuh kuh           -> left (arrow key)
# puh puh           -> right (arrow key)
# spit spit         -> escape
# tih tih           -> enter (space)
parrot(sss:stop): user.parrot_config_noise("sss_stop")
parrot(shh:stop): user.parrot_config_noise("shh_stop")
parrot(kuh): user.parrot_config_noise("kuh")
parrot(puh): user.parrot_config_noise("puh")
parrot(spit): user.parrot_config_noise("spit")
parrot(tih): user.parrot_config_noise("tih")
