app: brave
-
tag(): browser
tag(): user.tabs

# Requires the "Previous Tab" extension (https://chromewebstore.google.com/detail/previous-tab/bjaniflnlhhofabpoamhnobeonjcjjpl)
# with its shortcut set to alt-q via brave://extensions/shortcuts.
tab back: key(alt-q)

window <user.text>:
    key(cmd-shift-a)
    sleep(300ms)
    insert(text)
    key(enter)

window <number>:
    key(cmd-shift-a)
    sleep(300ms)
    insert("{number}")
    key(enter)
