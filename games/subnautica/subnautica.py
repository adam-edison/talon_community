from talon import Context, Module

mod = Module()

mod.tag(
    "game_subnautica",
    desc="Active when the Subnautica command set is turned on by voice. Cloud gaming (GeForce NOW) gives no usable app name or window title to match on",
)

ctx = Context()
ctx.matches = r"""
mode: user.game
"""


@mod.action_class
class Actions:
    def game_subnautica_enable():
        """Turn on the Subnautica command set"""
        ctx.tags = ["user.game_subnautica"]

    def game_subnautica_disable():
        """Turn off the Subnautica command set"""
        ctx.tags = []
