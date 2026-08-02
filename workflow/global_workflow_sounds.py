"""
Global workflow sounds: scroll (sss/shh) and command/dictation toggle.

- Scrolling: sss/shh sustained 300ms scroll up/down.
- Command/dictation toggle: whistle.
"""

from talon import Module, actions, cron, ctrl, scope, ui

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

# Scroll speed (0.5-32.0, default 8.0). Higher = more events per second.
# 8.0 reproduces the original 16ms cron interval. Interval = 128 / _scroll_speed ms.
_scroll_speed: float = 8.0

# Per-tick scroll amount stays fixed at the known-good value to avoid mouse_scroll
# rounding issues at small fractional deltas.
_SCROLL_AMOUNT_PER_TICK = 0.1


def _interval_ms() -> int:
    return max(4, min(512, int(round(128.0 / _scroll_speed))))


def _do_scroll_up():
    actions.user.mouse_scroll_up(_SCROLL_AMOUNT_PER_TICK)


def _do_scroll_down():
    actions.user.mouse_scroll_down(_SCROLL_AMOUNT_PER_TICK)


def _start_scroll_up():
    _pending_jobs.pop("sss", None)
    _scroll_jobs["sss"] = cron.interval(f"{_interval_ms()}ms", _do_scroll_up)


def _start_scroll_down():
    _pending_jobs.pop("shh", None)
    _scroll_jobs["shh"] = cron.interval(f"{_interval_ms()}ms", _do_scroll_down)


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
        """Multiply sound scroll speed by factor (clamped to 0.5-32.0)."""
        global _scroll_speed
        _scroll_speed = max(0.5, min(32.0, _scroll_speed * factor))
        actions.app.notify(f"Sound scroll speed: {_scroll_speed:.2f} ({_interval_ms()}ms)")

    def workflow_toggle_command_dictation():
        """Toggle between command and dictation mode."""
        _toggle_command_dictation()

    def workflow_toggle_left_drag():
        """Toggle left mouse drag and show ON/OFF notification."""
        _toggle_left_drag()
