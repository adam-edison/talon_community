app.name: /Bloons|Battles/i
mode: user.game
-

tag(): user.game_reserves_parrot_sounds
tag(): user.game_enables_screen_spots

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

notify me:
    user.bloons_log("notify me command fired")
    app.notify("hello")

(stop | cease): user.bloons_clear_spam()

parrot(clop): user.bloons_click()
parrot(tih): user.bloons_click()