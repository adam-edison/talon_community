app.name: /Bloons|Battles/i
mode: user.game
-

tag(): user.game_reserves_parrot_sounds

settings():
    key_wait = 30
    key_hold = 50
    user.game_location_file = "games/bloons_td_battles_2/bloons_td_battles_2.talon"

<user.ordinals>: core.repeat_command(ordinals - 1)

send {user.bloons_positions}: user.bloons_send_once(bloons_positions)
send {user.bloons_positions} <number_small>: user.bloons_send(bloons_positions, number_small)
spam {user.bloons_positions}: user.bloons_spam(bloons_positions)

(upgrade | grade) {user.bloons_upgrade_paths}: user.bloons_upgrade(bloons_upgrade_paths)
place hero: user.bloons_place("0")
place {user.bloons_place_targets}: user.bloons_place(bloons_place_targets)
(ability | bill | tack) {user.bloons_positions}: user.bloons_ability(bloons_positions)
full panic: user.bloons_full_panic()

select <number_small>: user.bloons_select(number_small)
clear monkeys: user.bloons_clear_monkeys()

regrow: user.bloons_key("z")
camo: user.bloons_key("x")
fortified: user.bloons_key("c")
(tower boost | panic): user.bloons_key("space")
(bloon boost | push it | punch it): user.bloons_key("ctrl-space")
target: user.bloons_key("tab")
target left: user.bloons_key("ctrl-tab")
cancel: user.bloons_key("escape")
confirm: user.bloons_key("enter")

(stop | cease): user.bloons_clear_spam()

parrot(clop): user.bloons_click()

escape: key(escape)

# === auto-generated locations (managed by game_locations.py) ===
battle tab: user.game_click_location(133, 413, 100)
shop tab: user.game_click_location(169, 1003, 100)
season tab: user.game_click_location(144, 788, 100)
heroes tab: user.game_click_location(126, 263, 100)
monkey's tab: user.game_click_location(119, 133, 100)
clans tab: user.game_click_location(174, 636, 100)
clan war: user.game_click_location(925, 894, 100)
special one: user.game_click_location(1756, 330, 100)
special too: user.game_click_location(1757, 471, 100)
rankings: user.game_click_location(1073, 54, 100)
battle: user.game_click_location(1287, 880, 100)
skip: user.game_click_location(971, 864, 100)
continue: user.game_click_location(1100, 868, 100)
ready: user.game_click_location(1544, 763, 100)
start: user.game_click_location(1508, 874, 100)
comment: user.game_click_location(961, 938, 100)
laugh: user.game_click_location(1349, 546, 100)
# === end auto-generated locations ===
