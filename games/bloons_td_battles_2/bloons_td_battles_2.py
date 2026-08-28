from talon import Context, Module, actions, cron, ctrl

game_debug = False

mod = Module()
ctx = Context()

ctx.matches = """
win.title: /Bloons/i
mode: user.game
"""

SLOT_KEYS = {
    "1": "a",
    "2": "s",
    "3": "d",
    "4": "f",
    "5": "g",
    "6": "h",
    "7": "j",
    "8": "k",
    "9": "l",
    "10": ";",
}

UPGRADE_KEYS = {"1": ",", "2": ".", "3": "/"}
PLACE_KEYS = {"0": "q", "1": "w", "2": "e", "3": "r", "farmer": "t", "spammer": "y", "bot": "u"}

SEND_INTERVAL = "300ms"


def _log(message: str):
    if game_debug:
        print(f"[bloons] {message}")


_spam_job = None
_spam_slot = ""


mod.list("bloons_positions", "Bloons send slot positions")
ctx.lists["user.bloons_positions"] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}

mod.list("bloons_upgrade_paths", "Bloons upgrade paths")
ctx.lists["user.bloons_upgrade_paths"] = {"one": "1", "two": "2", "three": "3"}

mod.list("bloons_place_targets", "Bloons place targets")
ctx.lists["user.bloons_place_targets"] = {
    "hero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "farmer": "farmer",
    "spammer": "spammer",
    "bot": "bot",
}


def _clear_spam():
    global _spam_job, _spam_slot
    if _spam_job is not None:
        _log("clear spam, cancelling cron job")
    else:
        _log("clear spam, no cron job")
    if _spam_job is not None:
        cron.cancel(_spam_job)
        _spam_job = None
    _spam_slot = ""


def _spam_tick():
    if _spam_slot:
        key = SLOT_KEYS[_spam_slot]
        _log(f"spam tick: slot={_spam_slot} key={key}")
        actions.key(key)


@mod.action_class
class Actions:
    def bloons_log(message: str):
        """Log [message] while game_debug is enabled"""
        _log(message)

    def bloons_send(position: str, count: int):
        """Send send-slot [position] [count] times"""
        _clear_spam()
        _log(f"send slot={position} count={count}")
        if count < 1:
            return
        for _ in range(count):
            actions.key(SLOT_KEYS[position])
            actions.sleep("80ms")

    def bloons_send_once(position: str):
        """Send send-slot [position] once"""
        _clear_spam()
        _log(f"send once slot={position}")
        actions.key(SLOT_KEYS[position])

    def bloons_spam(position: str):
        """Keep sending send-slot [position] until another game command is spoken"""
        global _spam_job, _spam_slot
        _log(f"spam start slot={position}")
        _spam_slot = position
        if _spam_job is None:
            _spam_job = cron.interval(SEND_INTERVAL, _spam_tick)

    def bloons_clear_spam():
        """Stop the continuous spam"""
        _clear_spam()

    def bloons_upgrade(path: str):
        """Upgrade path [path] of the selected tower"""
        _clear_spam()
        _log(f"upgrade path={path}")
        actions.key(UPGRADE_KEYS[path])

    def bloons_place(x: str):
        """Select [x] for placement (0 hero, 1-3 tower slots)"""
        _clear_spam()
        _log(f"place target={x}")
        actions.key(PLACE_KEYS[x])

    def bloons_ability(n: str):
        """Activate ability slot [n]"""
        _clear_spam()
        _log(f"ability slot={n}")
        key = "0" if n == "10" else n
        actions.key(key)

    def bloons_key(key: str):
        """Stop spam and press [key]"""
        _clear_spam()
        _log(f"key {key}")
        actions.key(key)

    def bloons_click():
        """Stop spam and click"""
        _clear_spam()
        _log("click")
        ctrl.mouse_click(button=0, down=True)
        actions.sleep("50ms")
        ctrl.mouse_click(button=0, up=True)


_log("module loaded")