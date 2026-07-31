from talon import Context, Module, actions, clip
import re

ctx = Context()
mod = Module()

ctx.matches = """
"""

mod.list("task_status", desc="Statuses for task lists")

DONE_EMOJI = "✅"

ctx.lists["user.task_status"] = {
    "done": DONE_EMOJI,
    "complete": DONE_EMOJI,
    "passed": DONE_EMOJI,
    "in progress": "🚧",
    "skipped": "⏭️",
    "blocked": "⛔️",
    "waiting": "⏳",
    "paused": "⏸️",
    "failed": "❌"
}

# Matches a markdown checkbox at the start of a line, e.g. "- [ ]", "* [x]", "[ ]", "   [ ]"
CHECKBOX_PATTERN = re.compile(r"^(\s*(?:[-*]\s+)?)\[([ xX])\]")


def find_checkbox(contents):
    """Find a markdown checkbox at the start of the current line's contents"""
    return CHECKBOX_PATTERN.match(contents)


def replace_checkbox_state(checkbox_match, new_state):
    """Move to the checkbox's state character on the current line and replace it"""
    state_position = checkbox_match.end() - 2

    actions.edit.line_start()
    actions.sleep("15ms")

    for i in range(state_position):
        actions.edit.right()
        actions.sleep("15ms")

    actions.edit.delete_right()
    actions.sleep("50ms")
    actions.insert(new_state)


@mod.action_class
class Actions:
    def mark_clear_status():
        """Remove the status from the current line"""
        actions.user.copy_line()
        actions.sleep("100ms")
        contents = clip.text()

        checkbox_match = find_checkbox(contents)

        if checkbox_match and checkbox_match.group(2) in ("x", "X"):
            replace_checkbox_state(checkbox_match, " ")
            return

        emoji_is_present = re.search(r"[✅🚧⏭️⛔️⏳⏸️❌]", contents)

        if not emoji_is_present:
            return

        emoji_position = emoji_is_present.end()

        actions.edit.line_start()
        actions.sleep("15ms")

        for i in range(emoji_position - 1):
            actions.edit.right()
            actions.sleep("15ms")

        actions.edit.delete_right()
        actions.sleep("50ms")

        if contents[emoji_position] == " ":
            actions.edit.delete_right()

    def mark_status(status_emoji: str):
        """Parse the current line and mark or change a status"""
        actions.user.mark_clear_status()

        actions.user.copy_line()
        actions.sleep("100ms")
        contents = clip.text()

        checkbox_match = find_checkbox(contents)
        is_marking_done = status_emoji == DONE_EMOJI

        if checkbox_match and is_marking_done and checkbox_match.group(2) == " ":
            replace_checkbox_state(checkbox_match, "x")

        if checkbox_match and is_marking_done:
            return

        star_is_present = re.match(r"^[\s]*\*", contents)
        dash_is_present = re.match(r"^[\s]*-", contents)

        leading_whitespace_length = len(re.match(r"^[\s]*", contents).group(0))
        star_length = star_is_present and 2 or 0
        dash_length = dash_is_present and 2 or 0
        total_left_length = leading_whitespace_length + star_length + dash_length

        actions.edit.line_start()
        actions.sleep("50ms")

        for i in range(total_left_length):
            actions.edit.right()
            actions.sleep("15ms")

        actions.insert(f"{status_emoji} ")
