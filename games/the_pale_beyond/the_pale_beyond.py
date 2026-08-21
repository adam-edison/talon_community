from talon import Module, Context, actions

mod = Module()
ctx = Context()
ctx.matches = """
win.title: /The Pale Beyond/i
app.name: /The Pale Beyond/i
"""

parrot_config = {
    "sss_stop sss_stop": ("up",     lambda: actions.user.the_pale_beyond_up()),
    "shh_stop shh_stop": ("down",   lambda: actions.user.the_pale_beyond_down()),
    "kuh kuh":           ("left",   lambda: actions.user.the_pale_beyond_left()),
    "puh puh":           ("right",  lambda: actions.user.the_pale_beyond_right()),
    "spit spit":         ("escape", lambda: actions.user.the_pale_beyond_escape()),
    "tih tih":           ("enter",  lambda: actions.user.the_pale_beyond_enter()),
}


@ctx.action_class("user")
class UserActions:
    def parrot_config():
        return parrot_config


@mod.action_class
class Actions:
    def the_pale_beyond_up():
        """Navigate up"""
        actions.key("up")

    def the_pale_beyond_down():
        """Navigate down"""
        actions.key("down")

    def the_pale_beyond_left():
        """Navigate left"""
        actions.key("left")

    def the_pale_beyond_right():
        """Navigate right"""
        actions.key("right")

    def the_pale_beyond_enter():
        """Confirm / interact"""
        actions.key("space")

    def the_pale_beyond_escape():
        """Cancel / open menu"""
        actions.key("escape")
