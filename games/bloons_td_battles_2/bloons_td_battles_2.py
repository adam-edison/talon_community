import re

from talon import Context, Module, actions, app, canvas, cron, ctrl, scope, speech_system, ui
from talon.skia import Paint

game_debug = False

GAME_APP_NAME_PATTERN = re.compile("bloons|battles|btdb2", re.IGNORECASE)

mod = Module()
ctx = Context()

ctx.matches = """
app.name: /Bloons|Battles/i
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

SEND_INTERVAL = "100ms"


def _log(message: str):
    if game_debug:
        print(f"[bloons] {message}")


_spam_job = None
_spam_slot = ""

_placed_monkeys: list = []
_placement_pending = False
_marker_canvas = None


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


def _draw_markers(c):
    paint = c.paint
    paint.textsize = 16
    paint.fake_bold_text = True
    paint.color = "ff0000ff"
    paint.stroke_width = 1.5
    paint.text_align = Paint.TextAlign.CENTER
    for index, position in enumerate(_placed_monkeys, start=1):
        text = str(index)
        x, y = position
        text_rect = paint.measure_text(text)[1]
        radius = max(text_rect.width, text_rect.height) / 2 + 2

        paint.style = Paint.Style.STROKE
        c.draw_circle(x, y, radius)

        paint.style = Paint.Style.FILL
        c.draw_text(text, x, y + text_rect.height / 2)


def _close_markers():
    global _marker_canvas
    if _marker_canvas is None:
        return
    _marker_canvas.unregister("draw", _draw_markers)
    _marker_canvas.close()
    _marker_canvas = None


def _refresh_markers():
    global _marker_canvas
    if not _placed_monkeys:
        _close_markers()
        return
    if _marker_canvas is None:
        screen = ui.screen_containing(*_placed_monkeys[0])
        _marker_canvas = canvas.Canvas.from_screen(screen)
        _marker_canvas.register("draw", _draw_markers)
    _marker_canvas.freeze()


def _record_monkey_position():
    position = ctrl.mouse_pos()
    _placed_monkeys.append(position)
    _log(f"recorded monkey {len(_placed_monkeys)} at {position}")
    _refresh_markers()


def _clear_monkeys():
    _log(f"clearing {len(_placed_monkeys)} tracked monkeys")
    _placed_monkeys.clear()
    _close_markers()


def _on_app_activate(active_app):
    if GAME_APP_NAME_PATTERN.search(active_app.name):
        _log(f"app activated: {active_app.name}, showing markers")
        _refresh_markers()
    else:
        _log(f"app activated: {active_app.name}, hiding markers")
        _close_markers()


def _on_ready():
    ui.register("app_activate", _on_app_activate)
    _on_app_activate(ui.active_app())


app.register("ready", _on_ready)


@mod.action_class
class Actions:
    def bloons_log(message: str):
        """Log [message] to the Talon log (always on)"""
        print(f"[bloons] {message}")

    def bloons_send(position: str, count: int):
        """Send send-slot [position] [count] times"""
        _log(f"send slot={position} count={count}")
        if count < 1:
            return
        for _ in range(count):
            actions.key(SLOT_KEYS[position])
            actions.sleep("80ms")

    def bloons_send_once(position: str):
        """Send send-slot [position] once"""
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
        _log(f"upgrade path={path}")
        actions.key(UPGRADE_KEYS[path])

    def bloons_place(x: str):
        """Select [x] for placement (0 hero, 1-3 tower slots)"""
        global _placement_pending
        _log(f"place target={x}")
        _placement_pending = True
        actions.key(PLACE_KEYS[x])

    def bloons_ability(n: str):
        """Activate ability slot [n]"""
        _log(f"ability slot={n}")
        key = "0" if n == "10" else n
        actions.key(key)

    def bloons_full_panic():
        """Activate ability one, ability two, and tower boost"""
        _log("full panic")
        actions.key("1")
        actions.sleep("80ms")
        actions.key("2")
        actions.sleep("80ms")
        actions.key("space")

    def bloons_key(key: str):
        """Press [key], canceling a pending placement if [key] is escape"""
        global _placement_pending
        _log(f"key {key}")
        if key == "escape":
            _placement_pending = False
        actions.key(key)

    def bloons_click():
        """Click, recording the mouse position as a placed monkey if placement is pending"""
        global _placement_pending
        _log("click")
        if _placement_pending:
            _record_monkey_position()
            _placement_pending = False
        ctrl.mouse_click(button=0, down=True)
        actions.sleep("50ms")
        ctrl.mouse_click(button=0, up=True)

    def bloons_select(n: int):
        """Click the monkey placed at position [n]"""
        index = n - 1
        if index < 0 or index >= len(_placed_monkeys):
            _log(f"select {n}: no monkey recorded at that position")
            return
        position = _placed_monkeys[index]
        _log(f"select {n}: moving to {position}")
        ctrl.mouse_move(*position)
        ctrl.mouse_click(button=0, down=True)
        actions.sleep("50ms")
        ctrl.mouse_click(button=0, up=True)

    def bloons_clear_monkeys():
        """Clear tracked monkey positions and their on-screen numbers"""
        _clear_monkeys()


_log("module loaded")


def _on_phrase(d):
    words = [w for w in d.get("phrase", [])]
    text = " ".join(str(w) for w in words)
    modes = scope.get("mode") or {}
    app_name = scope.get("app.name")
    title = scope.get("win.title")
    in_game_mode = "user.game" in modes
    is_game_app = app_name is not None and GAME_APP_NAME_PATTERN.search(str(app_name))
    if in_game_mode or is_game_app:
        print(
            f"[bloons] phrase={text!r} app_name={app_name!r} title={title!r} "
            f"modes={sorted(modes)} speech_enabled={actions.speech.enabled()}"
        )


speech_system.register("post:phrase", _on_phrase)