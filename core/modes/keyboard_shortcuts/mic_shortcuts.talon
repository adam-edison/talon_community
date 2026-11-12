mode: all
-

key(keypad_minus):
    user.face_scroll_stop_all()
    speech.disable()
    sound.set_microphone("None")

key(keypad_plus):
    speech.enable()
    sound.set_microphone("System Default")
