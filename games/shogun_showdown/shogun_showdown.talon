win.title: /ShogunShowdown/i
mode: user.game
-

tag(): user.game_reserves_parrot_sounds

###### Overlay

# toggle the controls overlay on/off
show controls:
  user.shogun_controls_toggle()

###### Arrows

# up arrow
parrot(sss:stop):
  user.shogun_debounced_key("up", "up")

# down arrow
parrot(shh:stop):
  user.shogun_debounced_key("down", "down")

# tile selection: move left in queue
parrot(clop):
  user.shogun_debounced_key("tile_left", "left")

# tile selection: move right in queue
parrot(kuh):
  user.shogun_debounced_key("tile_right", "right")

###### Movement

# move left
parrot(cha:stop):
  user.shogun_debounced_key("move_left", "a")

# move right
parrot(motor:stop):
  user.shogun_debounced_key("move_right", "d")

###### Combat

# attack
parrot(whistle:stop):
  user.shogun_debounced_key("attack", "space")

# select
parrot(tih):
  user.shogun_debounced_key("select", "enter")

# wait a turn
parrot(wince:stop):
  user.shogun_debounced_key("wait", "s")

# turn around
parrot(snore:stop):
  user.shogun_debounced_key("turn_around", "w")

# upgrade (hold space 3 seconds)
(upgrade | sacrifice | grab it):
  user.shogun_upgrade()

# holds s for 3 seconds (lets go)
(lets go | skip it):
  user.shogun_lets_go()

# reroll (hold w 3 seconds)
reroll:
  user.shogun_reroll()

###### Menu

# menu
parrot(spit):
  user.shogun_debounced_key("menu", "escape")
