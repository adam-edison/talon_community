os: mac
win.title: /Google Calendar/
-

# uses military time
move <number>:
  # open event editor
  key(tab)
  sleep(50ms)
  key(enter)
  sleep(1200ms)

  # navigate to start time
  key(tab:5)

  # set start time
  insert("{number}")
  sleep(500ms)
  key(enter)

  # save
  key(cmd-s)

  # confirm for single event
  sleep(500ms)
  key(enter)

  # cancel selection
  sleep(1000ms)
  key(esc)
  sleep(50ms)
  key(esc)
  sleep(50ms)
  key(esc)
  sleep(50ms)
