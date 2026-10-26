win.title: /Google Calendar/
-

settings():
  key_wait = 20

edit {user.task_status}:
  key(tab)
  sleep(50ms)
  key(enter)
  sleep(2000ms)
  key(tab)
  sleep(200ms)
  user.mark_status(user.task_status)
  sleep(100ms)
  user.google_calendar_submit()
  sleep(600ms)
  key(enter)
  sleep(1000ms)
  key(esc)
  sleep(50ms)
  key(esc)
  sleep(50ms)
  key(esc)
  sleep(50ms)


event {user.task_status}:
  key(tab)
  sleep(50ms)
  user.mark_status(user.task_status)
  sleep(50ms)
  user.google_calendar_submit()
  sleep(600ms)
  key(enter)

event (dupe | duplicate | copy):
  key(tab:4)
  sleep(1000ms)
  key(enter)
  sleep(200ms)
  key(down)
  sleep(300ms)
  key(enter)
  sleep(1000ms)
  user.google_calendar_submit()
  sleep(1000ms)
  key(enter)
  sleep(1000ms)
