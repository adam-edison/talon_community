import json
import re
from pathlib import Path

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

MARKER_COLOR = "1b5e20ff"
MARKER_BACKGROUND_COLOR = "e8d5aeff"
MARKER_TEXT_SIZE = 16
MARKER_TEXT_WEIGHT = 1.2
MARKER_OUTLINE_WIDTH = 2

SIDES = ("left", "right")
DEFAULT_SIDE = "right"

CLICK_HOLD = "100ms"
REPEAT_CLICK_GAP = "80ms"

LOCATIONS_PATH = Path(__file__).parent / "bloons_locations.json"
TALON_FILE_PATH = Path(__file__).parent / "bloons_td_battles_2.talon"

LOCATIONS_SECTION_START = "# === auto-generated locations (managed by bloons_td_battles_2.py) ==="
LOCATIONS_SECTION_END = "# === end auto-generated locations ==="


def _log(message: str):
    if game_debug:
        print(f"[bloons] {message}")


_spam_job = None
_spam_slot = ""

_placed_monkeys: list = []
_placement_pending = False
_marker_canvas = None

_current_side = DEFAULT_SIDE
_locations: dict = {}


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

mod.list("bloons_sides", "Bloons player sides")
ctx.lists["user.bloons_sides"] = {"left": "left", "right": "right"}

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


def _empty_locations() -> dict:
    return {side: {} for side in SIDES}


def _load_locations():
    global _locations
    _locations = _empty_locations()

    if not LOCATIONS_PATH.is_file():
        _log(f"no locations file at {LOCATIONS_PATH}")
        return

    stored = json.loads(LOCATIONS_PATH.read_text())
    for side in SIDES:
        _locations[side].update(stored.get(side, {}))

    _log(f"loaded locations: {[(side, len(_locations[side])) for side in SIDES]}")


def _save_locations():
    LOCATIONS_PATH.write_text(json.dumps(_locations, indent=2, sort_keys=True) + "\n")


def _click_at(x: int, y: int):
    ctrl.mouse_move(x, y)
    ctrl.mouse_click(button=0, down=True)
    actions.sleep(CLICK_HOLD)
    ctrl.mouse_click(button=0, up=True)


def _click_named(name: str):
    position = _locations[_current_side].get(name)

    if position is None:
        _log(f"no '{name}' location saved for the {_current_side} side")
        app.notify(f"No '{name}' location for the {_current_side} side")
        return

    _log(f"click '{name}' on the {_current_side} side at {position}")
    _click_at(*position)


def _normalize_name(text: str) -> str:
    return " ".join(text.lower().split())


def _extract_trigger_alternatives(line: str) -> list[str]:
    trigger = line.split(":", 1)[0].strip()
    if not trigger or trigger.startswith("#"):
        return []

    stripped = trigger.strip("()[]")
    return [alternative.strip().strip("()[]") for alternative in stripped.split("|")]


def _find_generated_section(lines: list[str]) -> tuple[int, int] | None:
    if LOCATIONS_SECTION_START not in lines or LOCATIONS_SECTION_END not in lines:
        return None

    start = lines.index(LOCATIONS_SECTION_START)
    end = lines.index(LOCATIONS_SECTION_END)
    return start, end


def _has_hand_written_collision(lines: list[str], name: str) -> bool:
    section = _find_generated_section(lines)
    generated_line_numbers = set(range(section[0], section[1] + 1)) if section else set()

    for line_number, line in enumerate(lines):
        if line_number in generated_line_numbers:
            continue
        for alternative in _extract_trigger_alternatives(line):
            if alternative.lower() == name:
                return True

    return False


def _replace_in_section(body: list[str], name: str, new_line: str) -> bool:
    for line_number, line in enumerate(body):
        if line.split(":", 1)[0].strip() == name:
            body[line_number] = new_line
            return True

    return False


def _upsert_location_command(lines: list[str], name: str) -> list[str]:
    new_line = f'{name}: user.bloons_click_named("{name}")'
    section = _find_generated_section(lines)

    if section is None:
        trailing_blank = [] if (not lines or lines[-1] == "") else [""]
        return lines + trailing_blank + [LOCATIONS_SECTION_START, new_line, LOCATIONS_SECTION_END]

    start, end = section
    body = lines[start + 1 : end]

    if not _replace_in_section(body, name, new_line):
        body.append(new_line)

    return lines[: start + 1] + body + lines[end:]


def _write_talon_command(name: str) -> bool:
    lines = TALON_FILE_PATH.read_text().splitlines()

    if _has_hand_written_collision(lines, name):
        app.notify(f"'{name}' already exists as a command, pick a different name")
        return False

    updated_lines = _upsert_location_command(lines, name)
    TALON_FILE_PATH.write_text("\n".join(updated_lines) + "\n")
    return True


def _store_position(name: str, sides: tuple, x: int, y: int):
    for side in sides:
        _locations[side][name] = [x, y]

    _save_locations()


def _save_location(text: str, sides: tuple):
    name = _normalize_name(text)

    if not _write_talon_command(name):
        return

    x, y = ctrl.mouse_pos()
    _store_position(name, sides, int(x), int(y))

    _log(f"saved '{name}' for {sides} at ({int(x)}, {int(y)})")
    app.notify(f"Saved '{name}' for {' and '.join(sides)} at ({int(x)}, {int(y)})")


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


def _prepare_marker_paint(paint):
    paint.antialias = True
    paint.textsize = MARKER_TEXT_SIZE
    paint.font.embolden = True
    paint.text_align = Paint.TextAlign.CENTER


def _draw_marker_circle(c, x, y, radius):
    paint = c.paint

    paint.style = Paint.Style.FILL
    paint.color = MARKER_BACKGROUND_COLOR
    c.draw_circle(x, y, radius)

    paint.style = Paint.Style.STROKE
    paint.stroke_width = MARKER_OUTLINE_WIDTH
    paint.color = MARKER_COLOR
    c.draw_circle(x, y, radius)


def _draw_marker_number(c, text, x, baseline):
    paint = c.paint
    paint.color = MARKER_COLOR

    paint.style = Paint.Style.FILL
    c.draw_text(text, x, baseline)

    paint.style = Paint.Style.STROKE
    paint.stroke_width = MARKER_TEXT_WEIGHT
    c.draw_text(text, x, baseline)


def _draw_markers(c):
    _prepare_marker_paint(c.paint)

    for index, position in enumerate(_placed_monkeys, start=1):
        text = str(index)
        x, y = position
        text_rect = c.paint.measure_text(text)[1]
        radius = max(text_rect.width, text_rect.height) / 2 + 5

        _draw_marker_circle(c, x, y, radius)
        _draw_marker_number(c, text, x, y + text_rect.height / 2)


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
    _clear_spam()


def _on_app_activate(active_app):
    if GAME_APP_NAME_PATTERN.search(active_app.name):
        _log(f"app activated: {active_app.name}, showing markers")
        _refresh_markers()
    else:
        _log(f"app activated: {active_app.name}, hiding markers")
        _close_markers()


def _on_ready():
    _load_locations()
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
        """Clear tracked monkey positions and their on-screen numbers, and stop any spam"""
        _clear_monkeys()

    def bloons_set_side(side: str):
        """Set the side you are playing on to [side], which picks the coordinate set locations resolve against"""
        global _current_side
        _current_side = side
        _log(f"side set to {side}")
        app.notify(f"{side} side")

    def bloons_current_side() -> str:
        """Return the side you are currently playing on"""
        return _current_side

    def bloons_click_named(name: str):
        """Click the saved location [name] using the current side's coordinates"""
        _click_named(name)

    def bloons_click_named_times(name: str, count: int):
        """Click the saved location [name] [count] times using the current side's coordinates"""
        for click_number in range(count):
            if click_number > 0:
                actions.sleep(REPEAT_CLICK_GAP)
            _click_named(name)

    def bloons_save_location(text: str):
        """Save the mouse position as location [text] for the side you are currently on"""
        _save_location(text, (_current_side,))

    def bloons_save_both_location(text: str):
        """Save the mouse position as location [text] for both sides at once"""
        _save_location(text, SIDES)

    def bloons_save_side_location(side: str, text: str):
        """Save the mouse position as location [text] for the [side] side only"""
        _save_location(text, (side,))


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