from talon import Module, Context, actions, ctrl

mod = Module()
ctx = Context()
ctx.matches = """
win.title: /The Pale Beyond/i
app.name: /The Pale Beyond/i
"""

ctrl_held = False


def toggle_ctrl():
    global ctrl_held
    ctrl_held = not ctrl_held
    if ctrl_held:
        actions.key("ctrl:down")
    else:
        actions.key("ctrl:up")


parrot_config = {
    "spit spit": ("escape", lambda: actions.user.the_pale_beyond_escape()),
}


@ctx.action_class("user")
class UserActions:
    def parrot_config():
        return parrot_config


@mod.action_class
class Actions:
    def the_pale_beyond_escape():
        """Cancel / open menu"""
        actions.key("escape")

    def the_pale_beyond_toggle_ctrl():
        """Toggle ctrl held down"""
        toggle_ctrl()
