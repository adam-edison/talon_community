from talon import Context, Module, actions
from talon.mac import applescript

ctx = Context()
mod = Module()

mod.apps.iterm2 = """
os: mac
and app.bundle: com.googlecode.iterm2
"""
ctx.matches = r"""
app: iterm2
"""

primary_tab: int = 1
total_tabs: int = 9
cycle_index: int = 0
skip_tabs: set = set()

CLEAR_PANES_AFTER_FIRST_SCRIPT = """
tell application "iTerm2"
    set paneList to sessions of current tab of current window
    repeat with paneIndex from 2 to count of paneList
        tell item paneIndex of paneList to write text "clear"
    end repeat
end tell
"""

def _clear_skip_list():
    """Clear the skip list (internal)."""
    global skip_tabs
    skip_tabs = set()

@mod.action_class
class PaneActions:
    def pane_jump(number: int):
        """Jumps to the specified pane in the current tab."""

    def pane_jump_into(tab_number: int, pane_number: int):
        """Jumps to the specified pane in the specified tab."""

    def clear_panes_after_first():
        """Runs clear in every pane of the current iTerm tab except the first one."""
        applescript.run(CLEAR_PANES_AFTER_FIRST_SCRIPT)

    def set_iterm_tab_primary(number: int):
        """Sets the primary iTerm tab number."""
        global primary_tab, cycle_index
        primary_tab = number
        cycle_index = 0
        _clear_skip_list()
        actions.app.notify(f"Primary tab: {primary_tab}")

    def jump_to_primary():
        """Jumps to the primary iTerm tab."""
        actions.key(f"cmd-{primary_tab}")

    def set_iterm_tab_total(number: int):
        """Sets the total number of iTerm tabs."""
        global total_tabs, cycle_index
        total_tabs = number
        cycle_index = 0
        _clear_skip_list()
        actions.app.notify(f"Total tabs: {total_tabs}")

    def skip_tab(number: int):
        """Add a tab number to the skip list (excluded from secondaries)."""
        global skip_tabs
        skip_tabs.add(number)

    def clear_skip_list():
        """Clear the skip list for secondary tabs."""
        _clear_skip_list()

    def cycle_tabs():
        """Cycles to the next tab: primary, secondary 1, primary, secondary 2, etc."""
        global cycle_index
        secondaries = [
            t
            for t in range(1, total_tabs + 1)
            if t != primary_tab and t not in skip_tabs
        ]
        # Order: primary, sec1, primary, sec2, primary, sec3, ...
        tabs = [primary_tab]
        for s in secondaries:
            tabs.append(s)
            tabs.append(primary_tab)
        if not tabs:
            return
        cycle_index = cycle_index % len(tabs)
        actions.key(f"cmd-{tabs[cycle_index]}")
        cycle_index = (cycle_index + 1) % len(tabs)

directories_to_remap = {}
directories_to_exclude = {}


@ctx.action_class("app")
class AppActions:
    def tab_next():
        actions.key("shift-cmd-]")

    def tab_previous():
        actions.key("shift-cmd-[")


@ctx.action_class("edit")
class EditActions:
    def line_start():
        actions.key("home")

    def line_end():
        actions.key("end")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        actions.key(f"cmd-{number}")

    def tab_final():
        actions.key("cmd-9")

    def terminal_clear_screen():
        """Clear screen"""
        actions.key("ctrl-l")

    def pane_jump(number: int):
        actions.key(f"ctrl-{number}")

    def pane_jump_into(tab_number: int, pane_number: int):
        if not (1 <= tab_number <= 9):
            return

        if not (1 <= pane_number <= 9):
            return

        actions.key(f"cmd-{tab_number}")
        actions.sleep("200ms")
        actions.key(f"ctrl-{pane_number}")
