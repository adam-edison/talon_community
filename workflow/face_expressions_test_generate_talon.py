"""
Generate face_expressions_test.talon from the EXPRESSION_SECTIONS list below.

To add or rename a face expression, edit EXPRESSION_SECTIONS and run this script.

Usage: python face_expressions_test_generate_talon.py
"""

import os

SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "face_expressions_test.talon")

DIVIDER = "# " + "=" * 77

HEADER = """\
win.title: /face_expressions_test\\.log/i
-

# Face expression test file - 300ms delay before firing
# Only active when viewing the log file: workflow/face_expressions_test.log
# Say "clear face log" to clear the log file

clear face log: user.face_test_clear_log()"""

EXPRESSION_SECTIONS = [
    (
        "PSEUDO-EXPRESSIONS (high-level, combines left+right)",
        [
            ("blink", "close both eyes briefly"),
            ("smile", "raise corners of mouth (happiness)"),
            ("frown", "lower corners of mouth (sadness/displeasure)"),
            ("squint", "partially close both eyes (like bright light)"),
            ("dimple", "pull mouth corners back toward ears (creates cheek dimples)"),
            ("open_mouth", "drop jaw to open mouth"),
            ("raise_eyebrows", "lift both eyebrows (surprise)"),
            ("eye_blink", "same as blink - close both eyes"),
            ("pucker_lips_outwards", "push lips forward like a kiss"),
            ("pucker_lips_left", "push lips toward left side"),
            ("pucker_lips_right", "push lips toward right side"),
        ],
    ),
    (
        "EYEBROWS - fine-grained control",
        [
            ("brow_down_left", "lower/furrow left eyebrow (angry or focused)"),
            ("brow_down_right", "lower/furrow right eyebrow"),
            ("brow_inner_up", "raise inner ends of eyebrows (worry/concern)"),
            ("brow_outer_up_left", "raise outer end of left eyebrow (skeptical)"),
            ("brow_outer_up_right", "raise outer end of right eyebrow"),
        ],
    ),
    (
        "EYES - blink/squint/wide (NOT gaze direction)",
        [
            ("blink_left", "close left eye (wink)"),
            ("blink_right", "close right eye (wink)"),
            ("squint_left", "partially close left eye"),
            ("squint_right", "partially close right eye"),
            ("eye_wide_left", "open left eye wider than normal (surprise)"),
            ("eye_wide_right", "open right eye wider than normal"),
        ],
    ),
    (
        "JAW",
        [
            ("jaw_open", "drop jaw to open mouth wide"),
            ("jaw_left", "shift jaw to the left"),
            ("jaw_right", "shift jaw to the right"),
        ],
    ),
    (
        "MOUTH - general shapes",
        [
            ("mouth_close", "press lips firmly together"),
            ("mouth_funnel", 'make "O" shape with lips (like saying "oo")'),
            ("mouth_pucker", "pucker lips tightly (kissing face)"),
            ("mouth_left", "shift whole mouth toward left"),
            ("mouth_right", "shift whole mouth toward right"),
        ],
    ),
    (
        "MOUTH - lower lip movements",
        [
            (
                "mouth_lower_down_left",
                "pull lower lip down on left (showing lower teeth)",
            ),
            ("mouth_lower_down_right", "pull lower lip down on right"),
        ],
    ),
    (
        "MOUTH - press (lips pressed together tightly)",
        [
            ("mouth_press_left", "press lips together tightly on left side"),
            ("mouth_press_right", "press lips together tightly on right side"),
        ],
    ),
    (
        "MOUTH - roll (rolling lip inward, tucking it in)",
        [
            ("mouth_roll_lower", "roll lower lip inward (tuck under teeth)"),
            ("mouth_roll_upper", "roll upper lip inward"),
        ],
    ),
    (
        'MOUTH - shrug (raising lip like uncertainty "meh")',
        [
            ("mouth_shrug_lower", 'raise lower lip upward (pouting, "meh")'),
            ("mouth_shrug_upper", "raise upper lip (mild disgust)"),
        ],
    ),
    (
        "MOUTH - smile (per-side)",
        [
            ("smile_left", "raise left corner of mouth"),
            ("smile_right", "raise right corner of mouth"),
        ],
    ),
    (
        "MOUTH - stretch (pulling corner outward, like grimace)",
        [
            ("mouth_stretch_left", "stretch left corner of mouth outward (grimace)"),
            ("mouth_stretch_right", "stretch right corner outward"),
        ],
    ),
    (
        "MOUTH - upper lip movements",
        [
            (
                "mouth_upper_up_left",
                "raise upper lip on left (snarl, showing upper teeth)",
            ),
            ("mouth_upper_up_right", "raise upper lip on right"),
        ],
    ),
    (
        "DIMPLES (per-side) - pulling mouth corners back",
        [
            ("dimple_left", "pull left mouth corner back toward ear"),
            ("dimple_right", "pull right mouth corner back toward ear"),
        ],
    ),
    (
        "FROWN (per-side) - lowering mouth corners",
        [
            ("frown_left", "lower left corner of mouth (sadness)"),
            ("frown_right", "lower right corner of mouth"),
        ],
    ),
]


def generate_section_heading(title):
    """Return the divider-wrapped heading comment for a section."""
    return f"{DIVIDER}\n# {title}\n{DIVIDER}"


def generate_expression_block(name, description):
    """Return the comment and start/stop rules for one expression."""
    comment = f"# {name}: {description}"
    start_rule = f'face({name}:start): user.face_test_start("{name}")'
    stop_rule = f'face({name}:stop): user.face_test_stop("{name}")'
    return "\n".join([comment, start_rule, stop_rule])


def generate_section(title, expressions):
    """Return the heading followed by every expression block in the section."""
    heading = generate_section_heading(title)
    blocks = [generate_expression_block(name, text) for name, text in expressions]
    return "\n\n".join([heading] + blocks)


def generate_talon_text(sections):
    """Return the full contents of the .talon file."""
    section_texts = [generate_section(title, items) for title, items in sections]
    return "\n\n".join([HEADER] + section_texts) + "\n"


def write_talon_file(path, text):
    """Write the .talon file."""
    with open(path, "w") as f:
        f.write(text)


def main():
    text = generate_talon_text(EXPRESSION_SECTIONS)
    write_talon_file(OUTPUT_PATH, text)

    expression_count = sum(len(items) for _, items in EXPRESSION_SECTIONS)
    print(f"Generated {OUTPUT_PATH}")
    print(f"  {expression_count} expressions")


if __name__ == "__main__":
    main()
