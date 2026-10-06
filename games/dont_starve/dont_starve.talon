win.title: /Don't Starve/i
mode: user.game
-

tag(): user.game_reserves_parrot_sounds

###### Mouse

# primary (left click)
parrot(clop): mouse_click(0)

# secondary (right click)
parrot(kuh): mouse_click(1)

###### Action

# toggle holding space (auto-action)
parrot(shh:stop): user.dont_starve_toggle_space()

# auto-action
action: key(space)

# auto-attack
attack: key(f)

###### Movement (held until "stop")

walk up: user.dont_starve_walk("w")
walk down: user.dont_starve_walk("s")
walk left: user.dont_starve_walk("a")
walk right: user.dont_starve_walk("d")
stop: user.dont_starve_stop_walking()

# keypad directions: 8 is up, 9 is up-right, 3 is down-right, and so on
walk one: user.dont_starve_walk("s a")
walk two: user.dont_starve_walk("s")
walk three: user.dont_starve_walk("s d")
walk four: user.dont_starve_walk("a")
walk six: user.dont_starve_walk("d")
walk seven: user.dont_starve_walk("w a")
walk eight: user.dont_starve_walk("w")
walk nine: user.dont_starve_walk("w d")

###### Camera

turn left: key(q)
turn right: key(e)
zoom in: mouse_scroll(-200)
zoom out: mouse_scroll(200)

###### Modifier clicks

# examine (alt + left click)
inspect: user.dont_starve_modifier_click("alt")

# attack neutral creature / split stack (ctrl + left click)
force click: user.dont_starve_modifier_click("ctrl")

# move stack between containers (shift + left click)
move stack: user.dont_starve_modifier_click("shift")

###### Inventory hotkeys

slot one: key(1)
slot two: key(2)
slot three: key(3)
slot four: key(4)
slot five: key(5)
slot six: key(6)
slot seven: key(7)
slot eight: key(8)
slot nine: key(9)
slot ten: key(0)
slot eleven: key(minus)
slot twelve: key(equal)

###### Map and menus

map: key(tab)
aerial map: key(pause)
menu: key(escape)
debug screen: key(backspace)
console: key(`)
