from talon import Module, Context, actions

mod = Module()
ctx = Context()
ctx.matches = """
win.title: /The Pale Beyond/i
app.name: /The Pale Beyond/i
"""

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
