from talon import Module

mod = Module()

mod.tag(
    "game_reserves_parrot_sounds",
    desc="Active while a game's Talon file claims exclusive use of parrot sounds that other tools (e.g. gaze-mouse-grid) would otherwise bind globally",
)

mod.tag(
    "game_enables_eye_gaze",
    desc="Active when a game wants to enable the eye gaze mouse grid (default: eye gaze is disabled in game mode)",
)

mod.tag(
    "game_enables_screen_spots",
    desc="Active when a game wants to enable screen spots commands (default: screen spots are disabled in game mode)",
)
