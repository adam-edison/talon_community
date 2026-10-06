from talon import Module, actions

mod = Module()

MOVEMENT_KEYS = ["w", "a", "s", "d"]

space_held = False


def press_space():
    actions.key("space:down")


def release_space():
    actions.key("space:up")


def toggle_space():
    global space_held
    space_held = not space_held
    if space_held:
        press_space()
        return
    release_space()


def release_movement_keys():
    for key_name in MOVEMENT_KEYS:
        actions.key(f"{key_name}:up")


def hold_keys(key_names: str):
    for key_name in key_names.split():
        actions.key(f"{key_name}:down")


@mod.action_class
class Actions:
    def dont_starve_toggle_space():
        """Toggles holding space (auto-action) down"""
        toggle_space()

    def dont_starve_walk(key_names: str):
        """Releases all movement keys, then holds down the space-separated key_names"""
        release_movement_keys()
        hold_keys(key_names)

    def dont_starve_stop_walking():
        """Releases all movement keys"""
        release_movement_keys()

    def dont_starve_modifier_click(modifier: str):
        """Left clicks while holding modifier"""
        actions.key(f"{modifier}:down")
        actions.mouse_click(0)
        actions.key(f"{modifier}:up")
