# Open localhost:<port> in Brave browser
# e.g. "launch local 3000" -> http://localhost:3000
launch local <number>: user.launch_local(number)

# e.g. "launch local 4300 app" -> http://localhost:4300/app
launch local <number> app: user.launch_local_app(number)
