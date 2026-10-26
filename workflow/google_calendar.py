from talon import Context, Module, actions

mod = Module()
ctx_mac = Context()
ctx_mac.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def google_calendar_submit():
        """Submit the Google Calendar event dialog using the platform shortcut"""
        actions.key("ctrl-enter")


@ctx_mac.action_class("user")
class MacUserActions:
    def google_calendar_submit():
        actions.key("cmd-enter")
