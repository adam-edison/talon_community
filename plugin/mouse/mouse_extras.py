from talon import Module, actions, ctrl

LEFT_BUTTON = 0
RIGHT_BUTTON = 1

mod = Module()


@mod.action_class
class Actions:
    def mouse_left_down():
        """Press the left mouse button and keep it held"""
        ctrl.mouse_click(button=LEFT_BUTTON, down=True)

    def mouse_left_up():
        """Release the left mouse button"""
        ctrl.mouse_click(button=LEFT_BUTTON, up=True)

    def mouse_right_down():
        """Press the right mouse button and keep it held"""
        ctrl.mouse_click(button=RIGHT_BUTTON, down=True)

    def mouse_right_up():
        """Release the right mouse button"""
        ctrl.mouse_click(button=RIGHT_BUTTON, up=True)

    def mouse_left_hold(duration_ms: int):
        """Hold the left mouse button down for duration_ms, then release it"""
        hold_button(LEFT_BUTTON, duration_ms)

    def mouse_right_hold(duration_ms: int):
        """Hold the right mouse button down for duration_ms, then release it"""
        hold_button(RIGHT_BUTTON, duration_ms)


def hold_button(button: int, duration_ms: int):
    """Press a mouse button, wait duration_ms, then release it"""
    ctrl.mouse_click(button=button, down=True)

    try:
        actions.sleep(f"{duration_ms}ms")
    finally:
        ctrl.mouse_click(button=button, up=True)
