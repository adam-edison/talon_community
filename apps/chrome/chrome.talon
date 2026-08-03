app: chrome
-
tag(): browser
tag(): user.tabs
tag(): user.emoji

profile switch: user.chrome_mod("shift-m")

tab search: user.chrome_mod("shift-a")

# Requires the "Previous Tab" extension (https://chromewebstore.google.com/detail/previous-tab/bjaniflnlhhofabpoamhnobeonjcjjpl)
# with its shortcut set to alt-q via chrome://extensions/shortcuts.
tab back: key(alt-q)

tab search <user.text>$:
    user.chrome_mod("shift-a")
    sleep(200ms)
    insert("{text}")
    key(down)

tab clip:
    app.tab_open()
    sleep(200ms)
    edit.paste()
    key(enter)
