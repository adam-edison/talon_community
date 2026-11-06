tag: terminal
-
# Repo path commands
list repos: insert('ls -al ~/repositories\n')

list all: insert('ls -al\n')

hunt repo <user.text>: 
    insert('cd ~/repositories\n')
    sleep(200ms)
    insert('cd {text}')
    sleep(100ms)
    key(tab:3)

city <user.word>: insert('cd {word}\t')

open [repo] <user.repo_paths>: insert('cd "{repo_paths}"\n')
cursor <user.repo_paths>: insert('cursor "{repo_paths}"\n')
cursor dot: insert('cursor .\n')

(claude | chat) launch: insert('claude\n')

backlog browser: insert('backlog browser\n')

(claude | chat) clear: insert('/clear\n')

(claude | chat) resume:
    key(ctrl-c)
    sleep(200ms)
    key(ctrl-c)
    sleep(2000ms)
    insert('clear\n')
    sleep(1000ms)
    insert('claude --resume\n')
    sleep(4000ms)

    key(enter)

(claude | chat) restart:
    key(ctrl-c)
    sleep(200ms)
    insert('/quit')
    sleep(200ms)
    key(enter)
    sleep(1000ms)
    insert('clear\n')
    sleep(1000ms)
    insert('claude\n')

clear next ticket:
    insert('/clear')
    sleep(100ms)
    key(enter)
    sleep(100ms)
    insert('/next-ticket')
    sleep(100ms)
    key(enter)