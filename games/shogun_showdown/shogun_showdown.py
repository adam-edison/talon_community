from talon import Module, actions, app, cron, registry, scope, ui
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.types import Rect

mod = Module()

OVERLAY_TAG = "user.game_reserves_parrot_sounds"

# (panel title, [(section header or None, [(icon, label, trigger), ...]), ...])
# icon is an emoji standing in for the action; trigger is a parrot sound or a quoted spoken phrase
PANELS = [
    (
        "Navigation",
        [
            (
                None,
                [
                    ("⬆️", "up arrow", "sss"),
                    ("⬇️", "down arrow", "shh"),
                    ("⏪", "tile select left", "clop"),
                    ("⏩", "tile select right", "kuh"),
                    ("⬅️", "move left", "cha"),
                    ("➡️", "move right", "motor"),
                ],
            ),
        ],
    ),
    (
        "Combat",
        [
            (
                "Combat",
                [
                    ("⚔️", "attack", "whistle"),
                    ("✅", "select", "tih"),
                    ("⏳", "wait a turn", "wince"),
                    ("\U0001f504", "turn around", "snore"),
                    ("\U0001f199", "upgrade", '"upgrade" / "sacrifice" / "grab it"'),
                    ("▶️", "lets go", '"lets go" / "skip it"'),
                    ("\U0001f3b2", "reroll", '"reroll"'),
                ],
            ),
            (
                "Menu",
                [
                    ("\U0001f4cb", "menu", "spit"),
                ],
            ),
        ],
    ),
]

BACKGROUND_COLOR = "1a1a1aee"
TITLE_COLOR = "ffffffff"
SECTION_COLOR = "8ab4f8ff"
LABEL_COLOR = "e8e8e8ff"
KEYCAP_FILL = "33334dff"
KEYCAP_BORDER = "8ab4f8ff"
KEYCAP_TEXT = "8ab4f8ff"
FONT_SIZE = 15
EMOJI_FONT_SIZE = 20
EMOJI_TYPEFACE = "Apple Color Emoji"
TITLE_SIZE = 18
LINE_HEIGHT = 28
SECTION_GAP = 8
HEADER_GAP = 10
PADDING = 16
ICON_WIDTH = 30
LABEL_GAP = 12
KEYCAP_PAD_X = 8
KEYCAP_PAD_Y = 4
SCREEN_MARGIN = 24
CHAR_WIDTH = 8.5  # rough estimate at FONT_SIZE, used for layout (no live canvas yet)

canvases: list[tuple[Canvas, object]] = []
overlay_wanted = False


def all_items(sections):
    for _, items in sections:
        yield from items


def label_width(sections) -> float:
    return max(len(label) for _, label, _ in all_items(sections)) * CHAR_WIDTH


def keycap_width(trigger: str) -> float:
    return len(trigger) * CHAR_WIDTH + KEYCAP_PAD_X * 2


def panel_size(sections) -> tuple[float, float]:
    max_keycap = max(keycap_width(trigger) for _, _, trigger in all_items(sections))
    width = PADDING * 2 + ICON_WIDTH + label_width(sections) + LABEL_GAP + max_keycap

    rows = 0
    for header, items in sections:
        if header is not None:
            rows += 1
        rows += len(items)
    rows += SECTION_GAP * (len(sections) - 1) / LINE_HEIGHT
    height = PADDING * 2 + TITLE_SIZE + HEADER_GAP + LINE_HEIGHT * rows

    return width, height


def draw_icon(c: SkiaCanvas, x: float, y: float, icon: str):
    c.paint.typeface = EMOJI_TYPEFACE
    c.paint.textsize = EMOJI_FONT_SIZE
    c.draw_text(icon, x, y)
    c.paint.typeface = None


def draw_keycap(c: SkiaCanvas, x: float, y: float, label: str):
    c.paint.typeface = None
    c.paint.textsize = FONT_SIZE
    text_width = c.paint.measure_text(label)[1].width
    width = text_width + KEYCAP_PAD_X * 2
    height = FONT_SIZE + KEYCAP_PAD_Y * 2
    rect = Rect(x, y - height + KEYCAP_PAD_Y, width, height)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = KEYCAP_FILL
    c.draw_rect(rect)

    c.paint.style = c.paint.Style.STROKE
    c.paint.color = KEYCAP_BORDER
    c.draw_rect(rect)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = KEYCAP_TEXT
    c.draw_text(label, x + KEYCAP_PAD_X, y)


def make_draw_fn(title: str, sections, label_x: float, keycap_x: float):
    def on_draw(c: SkiaCanvas):
        c.paint.style = c.paint.Style.FILL
        c.paint.color = BACKGROUND_COLOR
        c.draw_rect(c.rect)

        c.paint.typeface = None
        c.paint.textsize = TITLE_SIZE
        c.paint.color = TITLE_COLOR
        left_x = c.rect.x + PADDING
        row_y = c.rect.y + PADDING + TITLE_SIZE
        c.draw_text(title, left_x, row_y)

        row_y += HEADER_GAP + LINE_HEIGHT
        for header, items in sections:
            if header is not None:
                c.paint.typeface = None
                c.paint.textsize = FONT_SIZE
                c.paint.style = c.paint.Style.FILL
                c.paint.color = SECTION_COLOR
                c.draw_text(header, left_x, row_y)
                row_y += LINE_HEIGHT

            for icon, label, trigger in items:
                c.paint.style = c.paint.Style.FILL
                draw_icon(c, left_x, row_y, icon)

                c.paint.typeface = None
                c.paint.textsize = FONT_SIZE
                c.paint.color = LABEL_COLOR
                c.draw_text(label, left_x + label_x, row_y)

                draw_keycap(c, left_x + keycap_x, row_y, trigger)
                row_y += LINE_HEIGHT

            row_y += SECTION_GAP

    return on_draw


def panel_rects() -> list[Rect]:
    screen = ui.main_screen()
    rects = []
    for i, (_, sections) in enumerate(PANELS):
        width, height = panel_size(sections)
        y = screen.rect.bot - SCREEN_MARGIN - height
        if i == 0:
            x = screen.rect.x + SCREEN_MARGIN
        else:
            x = screen.rect.right - SCREEN_MARGIN - width
        rects.append(Rect(x, y, width, height))
    return rects


def show_overlay():
    global canvases
    if canvases:
        return
    for (title, sections), rect in zip(PANELS, panel_rects()):
        label_x = ICON_WIDTH
        keycap_x = ICON_WIDTH + label_width(sections) + LABEL_GAP
        draw_fn = make_draw_fn(title, sections, label_x, keycap_x)
        panel_canvas = Canvas.from_rect(rect)
        panel_canvas.register("draw", draw_fn)
        panel_canvas.freeze()
        canvases.append((panel_canvas, draw_fn))


def hide_overlay():
    global canvases
    for panel_canvas, draw_fn in canvases:
        panel_canvas.unregister("draw", draw_fn)
        panel_canvas.close()
    canvases = []


def update_visibility():
    context_active = OVERLAY_TAG in scope.get("tag")
    if overlay_wanted and context_active:
        show_overlay()
    else:
        hide_overlay()


def on_update_contexts():
    update_visibility()


def on_ready():
    registry.register("update_contexts", on_update_contexts)
    update_visibility()


app.register("ready", on_ready)


DEBOUNCE_MS = 300
_debounce_busy: dict[str, bool] = {}


def _debounce_clear(action_id: str):
    _debounce_busy[action_id] = False


def debounced_key(action_id: str, key_name: str):
    if _debounce_busy.get(action_id):
        return
    _debounce_busy[action_id] = True
    actions.key(key_name)
    cron.after(f"{DEBOUNCE_MS}ms", lambda: _debounce_clear(action_id))


@mod.action_class
class Actions:
    def shogun_controls_toggle():
        """Toggles the Shogun Showdown controls overlay"""
        global overlay_wanted
        overlay_wanted = not overlay_wanted
        update_visibility()

    def shogun_debounced_key(action_id: str, key_name: str):
        """Presses a key, ignoring repeats of the same action_id within the debounce window"""
        debounced_key(action_id, key_name)

    def shogun_upgrade():
        """Holds space for 3 seconds then releases (upgrade)"""
        actions.key("space:down")
        actions.sleep("3s")
        actions.key("space:up")

    def shogun_lets_go():
        """Holds s for 3 seconds then releases (lets go)"""
        actions.key("s:down")
        actions.sleep("3s")
        actions.key("s:up")

    def shogun_reroll():
        """Holds w for 3 seconds then releases (reroll)"""
        actions.key("w:down")
        actions.sleep("3s")
        actions.key("w:up")
