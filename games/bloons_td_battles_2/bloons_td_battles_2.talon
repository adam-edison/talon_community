app.name: /Bloons|Battles/i
mode: user.game
-

tag(): user.game_reserves_parrot_sounds

settings():
    key_wait = 30
    key_hold = 50

<user.ordinals>: core.repeat_command(ordinals - 1)

send {user.bloons_positions}: user.bloons_send_once(bloons_positions)
send {user.bloons_positions} <number_small>: user.bloons_send(bloons_positions, number_small)
spam {user.bloons_positions}: user.bloons_spam(bloons_positions)

(upgrade | grade) {user.bloons_upgrade_paths}: user.bloons_upgrade(bloons_upgrade_paths)
place hero: user.bloons_place("0")
place {user.bloons_place_targets}: user.bloons_place(bloons_place_targets)
(ability | bill | tack) {user.bloons_positions}: user.bloons_ability(bloons_positions)
full panic: user.bloons_full_panic()

(select | fox) <number_small>: user.bloons_select(number_small)

clear monkeys: user.bloons_clear_monkeys()

game over: user.bloons_clear_monkeys()

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

{user.bloons_sides} side: user.bloons_set_side(bloons_sides)

location both <user.text>: user.bloons_save_both_location(user.text)
location {user.bloons_sides} side <user.text>: user.bloons_save_side_location(bloons_sides, user.text)
location <user.text>: user.bloons_save_location(user.text)

# === auto-generated locations (managed by bloons_td_battles_2.py) ===
battle tab: user.bloons_click_named("battle tab")
shop tab: user.bloons_click_named("shop tab")
season tab: user.bloons_click_named("season tab")
heroes tab: user.bloons_click_named("heroes tab")
monkey's tab: user.bloons_click_named("monkey's tab")
clans tab: user.bloons_click_named("clans tab")
clan war: user.bloons_click_named("clan war")
special one: user.bloons_click_named("special one")
special too: user.bloons_click_named("special too")
rankings: user.bloons_click_named("rankings")
battle: user.bloons_click_named("battle")
skip: user.bloons_click_named("skip")
continue: user.bloons_click_named("continue")
ready: user.bloons_click_named("ready")
start: user.bloons_click_named("start")
comment: user.bloons_click_named("comment")
laugh: user.bloons_click_named("laugh")
get map: user.bloons_click_named("get map")
ok: user.bloons_click_named("ok")
git map: user.bloons_click_named("git map")
skip map: user.bloons_click_named("skip map")
# === end auto-generated locations ===
