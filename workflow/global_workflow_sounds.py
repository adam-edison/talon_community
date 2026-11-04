"""
Global workflow sounds: scroll (sss/shh) and command/dictation toggle.

- Scrolling: sss/shh sustained 300ms scroll up/down.
- Command/dictation toggle: whistle.
"""

from talon import Module, actions, cron, ctrl, scope, ui

from ..core.user_settings import SETTINGS_DIR, track_csv_list
from .sound_scroll_speeds import (
    DEFAULT_SCROLL_SPEED,
    clamp_scroll_speed,
    format_scroll_speed,
    parse_scroll_speeds,
    write_scroll_speeds,
)

mod = Module()

ITERM_BUNDLE_ID = "com.googlecode.iterm2"


# --- Mode switch: command <-> dictation with notification ---


def _switch_to_dictation():
    actions.mode.disable("sleep")
    actions.mode.disable("command")
    actions.mode.enable("dictation")
    actions.user.code_clear_language_mode()
    actions.user.gdb_disable()
    actions.app.notify("Dictation mode")


def _switch_to_command():
    actions.mode.disable("sleep")
    actions.mode.disable("dictation")
    actions.mode.enable("command")
    actions.app.notify("Command mode")


def _toggle_command_dictation():
    modes = scope.get("mode", set())

    if "dictation" in modes and "command" not in modes:
        _switch_to_command()
    else:
        _switch_to_dictation()


_drag_relay_job: cron.Job | None = None
_iterm_drag_active = False


def _relay_drag_position():
    x, y = ctrl.mouse_pos()
    ctrl.mouse_move(x, y)


def _is_iterm_active() -> bool:
    return ui.active_app().bundle == ITERM_BUNDLE_ID


def _start_left_drag():
    # iTerm2 only extends its own selection off synthetic LeftMouseDragged
    # events (real hardware movement while the button is synthetically held
    # is delivered as plain MouseMoved and gets ignored), and it reports
    # clicks to any program requesting xterm mouse tracking instead of
    # selecting text, unless Option is held. Hold Option and relay the real
    # cursor position as synthetic moves to work around both.
    global _drag_relay_job, _iterm_drag_active
    _iterm_drag_active = _is_iterm_active()

    if _iterm_drag_active:
        actions.key("alt:down")

    ctrl.mouse_click(0, down=True)

    if _iterm_drag_active:
        _drag_relay_job = cron.interval("16ms", _relay_drag_position)


def _end_left_drag():
    global _drag_relay_job, _iterm_drag_active
    if job := _drag_relay_job:
        cron.cancel(job)
        _drag_relay_job = None

    ctrl.mouse_click(0, up=True)

    if _iterm_drag_active:
        actions.key("alt:up")
        _iterm_drag_active = False


def _toggle_left_drag():
    if 0 in ctrl.mouse_buttons_down():
        _end_left_drag()
        actions.app.notify("Left drag OFF")
    else:
        _start_left_drag()
        actions.app.notify("Left drag ON")


# --- Scrolling ---

_pending_jobs: dict[str, cron.Job] = {}
_scroll_jobs: dict[str, cron.Job] = {}

# Scroll speed (0.5-32.0, default 8.0) is looked up per app when a scroll starts.
# Higher = more events per second. 8.0 reproduces the original 16ms cron
# interval. Interval = 128 / speed ms.
SCROLL_SPEEDS_FILENAME = "sound_scroll_speeds.csv"
SCROLL_SPEEDS_HEADERS = ("App name", "Scroll speed")

# Speeds saved in the CSV, keyed by app name.
_saved_speeds: dict[str, float] = {}

# "scroll double" / "scroll half" adjustments, kept until Talon restarts.
_session_speeds: dict[str, float] = {}

# Per-tick scroll amount stays fixed at the known-good value to avoid mouse_scroll
# rounding issues at small fractional deltas.
_SCROLL_AMOUNT_PER_TICK = 0.1


@track_csv_list(
    SCROLL_SPEEDS_FILENAME,
    headers=SCROLL_SPEEDS_HEADERS,
    default={},
    is_spoken_form_first=True,
)
def _on_scroll_speeds_update(rows: dict[str, str]):
    global _saved_speeds
    _saved_speeds = parse_scroll_speeds(rows)


def _active_app_name() -> str:
    return ui.active_app().name


def _saved_speed(app_name: str) -> float:
    return _saved_speeds.get(app_name, DEFAULT_SCROLL_SPEED)


def _speed_for_app(app_name: str) -> float:
    return _session_speeds.get(app_name, _saved_speed(app_name))


def _interval_ms(speed: float) -> int:
    return max(4, min(512, int(round(128.0 / speed))))


def _current_interval() -> str:
    speed = _speed_for_app(_active_app_name())
    return f"{_interval_ms(speed)}ms"


def _notify_speed(app_name: str, speed: float):
    actions.app.notify(
        f"{app_name} scroll speed: {format_scroll_speed(speed)} ({_interval_ms(speed)}ms)"
    )


def _save_speed(app_name: str, speed: float):
    _saved_speeds[app_name] = speed
    path = SETTINGS_DIR / SCROLL_SPEEDS_FILENAME
    write_scroll_speeds(path, SCROLL_SPEEDS_HEADERS, _saved_speeds)


def _do_scroll_up():
    actions.user.mouse_scroll_up(_SCROLL_AMOUNT_PER_TICK)


def _do_scroll_down():
    actions.user.mouse_scroll_down(_SCROLL_AMOUNT_PER_TICK)


def _start_scroll_up():
    _pending_jobs.pop("sss", None)
    _scroll_jobs["sss"] = cron.interval(_current_interval(), _do_scroll_up)


def _start_scroll_down():
    _pending_jobs.pop("shh", None)
    _scroll_jobs["shh"] = cron.interval(_current_interval(), _do_scroll_down)


def _stop_scroll(key: str):
    if job := _pending_jobs.pop(key, None):
        cron.cancel(job)

    if job := _scroll_jobs.pop(key, None):
        cron.cancel(job)


@mod.action_class
class Actions:
    def sound_scroll_up_start(delay_ms: int = 300):
        """Schedule continuous scroll up after delay."""
        _stop_scroll("sss")
        _pending_jobs["sss"] = cron.after(f"{delay_ms}ms", _start_scroll_up)

    def sound_scroll_up_stop():
        """Stop scroll up."""
        _stop_scroll("sss")

    def sound_scroll_down_start(delay_ms: int = 300):
        """Schedule continuous scroll down after delay."""
        _stop_scroll("shh")
        _pending_jobs["shh"] = cron.after(f"{delay_ms}ms", _start_scroll_down)

    def sound_scroll_down_stop():
        """Stop scroll down."""
        _stop_scroll("shh")

    def sound_scroll_speed_multiply(factor: float):
        """Multiply the focused app's sound scroll speed by factor until Talon restarts (clamped to 0.5-32.0)."""
        app_name = _active_app_name()
        speed = clamp_scroll_speed(_speed_for_app(app_name) * factor)
        _session_speeds[app_name] = speed
        _notify_speed(app_name, speed)

    def sound_scroll_speed_save(speed: float):
        """Set the focused app's sound scroll speed and save it to the CSV (clamped to 0.5-32.0)."""
        app_name = _active_app_name()
        clamped = clamp_scroll_speed(speed)
        _session_speeds.pop(app_name, None)
        _save_speed(app_name, clamped)
        _notify_speed(app_name, clamped)

    def workflow_toggle_command_dictation():
        """Toggle between command and dictation mode."""
        _toggle_command_dictation()

    def workflow_toggle_left_drag():
        """Toggle left mouse drag and show ON/OFF notification."""
        _toggle_left_drag()
