from pathlib import Path

from talon import Context, Module, actions, app, ctrl, settings

mod = Module()
ctx = Context()

ctx.matches = """
mode: user.game
"""

mod.setting(
    "game_location_file",
    type=str,
    default="",
    desc="Path (relative to the talon_community repo root) of the .talon file that `location <text>` "
    "commands should be saved into for the current game",
)

LOCATIONS_SECTION_START = "# === auto-generated locations (managed by game_locations.py) ==="
LOCATIONS_SECTION_END = "# === end auto-generated locations ==="

TALON_USER_DIRECTORY = Path(__file__).resolve().parents[2]


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


def _has_hand_written_collision(lines: list[str], normalized_text: str) -> bool:
    section = _find_generated_section(lines)
    generated_line_numbers = set(range(section[0], section[1] + 1)) if section else set()

    for line_number, line in enumerate(lines):
        if line_number in generated_line_numbers:
            continue
        for alternative in _extract_trigger_alternatives(line):
            if alternative.lower() == normalized_text:
                return True

    return False


def _upsert_location_command(lines: list[str], normalized_text: str, x: int, y: int, hold_ms: int) -> list[str]:
    new_line = f"{normalized_text}: user.game_click_location({x}, {y}, {hold_ms})"
    section = _find_generated_section(lines)

    if section is None:
        trailing_blank = [] if (not lines or lines[-1] == "") else [""]
        return lines + trailing_blank + [LOCATIONS_SECTION_START, new_line, LOCATIONS_SECTION_END]

    start, end = section
    body = lines[start + 1 : end]
    replaced = False

    for line_number, line in enumerate(body):
        if line.split(":", 1)[0].strip() == normalized_text:
            body[line_number] = new_line
            replaced = True
            break

    if not replaced:
        body.append(new_line)

    return lines[: start + 1] + body + lines[end:]


@mod.action_class
class Actions:
    def game_save_location(text: str):
        """Save the current mouse position as a new voice command named [text] in the current game's Talon file"""
        relative_path = settings.get("user.game_location_file")
        if not relative_path:
            app.notify("game_location_file is not configured for this game")
            return

        target_path = TALON_USER_DIRECTORY / relative_path
        if not target_path.is_file():
            app.notify(f"game_location_file not found: {target_path}")
            return

        normalized_text = " ".join(text.lower().split())
        lines = target_path.read_text().splitlines()

        if _has_hand_written_collision(lines, normalized_text):
            app.notify(f"'{normalized_text}' already exists as a command, pick a different name")
            return

        x, y = ctrl.mouse_pos()
        updated_lines = _upsert_location_command(lines, normalized_text, int(x), int(y), 100)
        target_path.write_text("\n".join(updated_lines) + "\n")
        app.notify(f"Saved location '{normalized_text}' at ({int(x)}, {int(y)})")

    def game_click_location(x: int, y: int, hold_ms: int = 100):
        """Move the mouse to [x],[y] and click, holding the button down for at least [hold_ms] milliseconds"""
        ctrl.mouse_move(x, y)
        ctrl.mouse_click(button=0, down=True)
        actions.sleep(f"{hold_ms}ms")
        ctrl.mouse_click(button=0, up=True)
