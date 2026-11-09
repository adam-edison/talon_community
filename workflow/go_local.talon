app: brave
-
# Load localhost:<port> in the current Brave tab
# e.g. "go local 3000" -> http://localhost:3000
go local <number>: user.go_local(number)

# e.g. "go local 4300 app" -> http://localhost:4300/app
go local <number> app: user.go_local_app(number)
