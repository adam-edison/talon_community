app: vscode
app: cursor
-

bar right:
    key(alt-cmd-b)

bar left:
    key(cmd-b)

safe saver:
    user.vscode("workbench.action.files.saveWithoutFormatting")

auto fix: key(alt-enter)

comment line: key(cmd-/)

follower:
    key(cmd:down)
    mouse_click()
    key(cmd:up)

completer:
    key(tab)
    sleep(200ms)
    key(tab)

slide left:
    user.vscode("workbench.action.moveEditorLeftInGroup")

slide right:
    user.vscode("workbench.action.moveEditorRightInGroup")

terminal max:
    user.vscode("workbench.action.toggleMaximizedPanel")

toggle selection:
    user.vscode("toggleFindInSelection")

toggle regex:
    user.vscode("toggleFindRegex")

hunt failure:
    user.vscode_terminal(1)
    sleep(100ms)
    user.find("")
    sleep(200ms)
    insert("FAIL")

[copy] permalink: user.vscode("copy-github-permalink.copy")

^hunt again$: key(shift-cmd-r)

paste clean object: user.clean_jest_object_paste()

filter test selection:
    edit.copy()
    sleep(200ms)
    user.vscode_terminal(1)
    sleep(100ms)
    insert(" -- -t ''")
    sleep(800ms)
    key(left)
    sleep(300ms)
    edit.paste()
    key(enter)

^assistant <user.word> [<number_small>]$:
    terminal = number_small or 1
    user.vscode_terminal(terminal)
    sleep(300ms)
    insert("dwa {user.word}")

^assistant <user.word> <user.word> [<number_small>]$:
    terminal = number_small or 1
    user.vscode_terminal(terminal)
    sleep(300ms)
    insert("dwa {user.word_1}:{user.word_2}")

window <user.word>:
    user.vscode("workbench.action.switchWindow")
    sleep(100ms)
    insert("{user.word}\n")

clean run:
    user.vscode_terminal(1)
    sleep(500ms)
    insert("clear\n")
    sleep(1000ms)
    key(up up enter)

(rerun | run last):
    user.vscode_terminal(1)
    key(up enter)

coding:
    user.vscode("workbench.action.focusActiveEditorGroup")
    user.vscode("workbench.action.focusActiveEditorGroup")

terminal this line:
    user.copy_line()
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    edit.paste()
    sleep(200ms)
    key(enter)

git status:
    user.vscode("workbench.scm.focus")
    key(ctrl-shift-alt-f5)

git publish:
    user.vscode("git.publish")

git checkout dot:
    user.vscode_terminal(1)
    sleep(500ms)
    insert("git checkout .")

next change:
    key(down space)

first change:
    key(tab:2)
    key(down:2)
    key(space)

view to do:
    user.vscode("workbench.action.quickOpen")
    sleep(50ms)
    insert("view todo")
    sleep(100ms)
    key(enter)

log below:
    edit.copy()
    edit.line_end()
    key(enter)
    user.paste("console.log({{ ")
    edit.paste()
    user.paste(" }});")

open folder:
    user.vscode("workbench.action.files.openFolder")

terminal here:
    key(ctrl-shift-`)

terminal status:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git status\n")

terminal bottom:
    user.vscode("workbench.action.terminal.scrollToBottom")

terminal top:
    user.vscode("workbench.action.terminal.scrollToTop")

fetch develop:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git checkout develop && git fetch -p && git pull\n")

rebase against develop:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git checkout develop && git pull && git checkout - && git rebase develop\n")

git graph:
    user.vscode("git-graph.view")

terminal paster <user.word>:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    user.indexed_clipboard_paste(clipboard_index)

terminal paster:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    edit.paste()

new folder [<user.word>]:
    title = user.word or ""
    user.vscode("explorer.newFolder")
    insert("{title}")

new file [<user.word>]:
    title = user.word or ""
    user.vscode("explorer.newFile")
    insert("{title}")

git checkout dot confirm:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git checkout .\n")

terminal push:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git push\n")

terminal push force:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git push --force-with-lease\n")

show to doos:
    user.vscode("todo-tree-view.focus")

terminal clear:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("clear\n")

^(expand | grow | shrink | contract):
    user.vscode("workbench.action.toggleMaximizedPanel")

uninstall clip:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("npm uninstall ")
    sleep(200ms)
    edit.paste()

git changes:
    user.vscode("git.viewChanges")

reference <user.word>+:
    insert("@")
    sleep(200ms)
    user.insert_many(word_list)

cursor stop: key(cmd-shift-backspace)

cursor ask: key(cmd-l)

cursor agent: key(cmd-i)

cursor mode: key(cmd-.)

git generate: user.vscode("cursor.generateGitCommitMessage")

give claude: key(cmd-alt-k)

code go:
    user.vscode("workbench.action.quickOpen")
    sleep(100ms)
    insert("claude code")
    sleep(100ms)
    key(enter)

code clear:
    user.vscode("workbench.action.quickOpen")
    sleep(300ms)
    insert("claude code")
    sleep(300ms)
    key(enter)
    sleep(500ms)
    insert("/clear")
    sleep(100ms)
    key(enter)

clear all tools:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("clear")
    sleep(100ms)
    key(enter)
    sleep(700ms)
    user.vscode("workbench.action.quickOpen")
    sleep(300ms)
    insert("claude code")
    sleep(300ms)
    key(enter)
    sleep(500ms)
    insert("/clear")
    sleep(100ms)
    key(enter)

git add <user.word>:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git add \"*{user.word}*\"\n")
    sleep(200ms)
    user.vscode("workbench.scm.focus")

git amend force:
    user.vscode("workbench.action.terminal.focus")
    sleep(200ms)
    insert("git commit --amend --no-edit\n")
    sleep(200ms)
    insert("git push --force-with-lease\n")
    sleep(3000ms)
    user.vscode("workbench.scm.focus")

mark <number> {user.task_status}:
    edit.jump_line(number)
    user.mark_status(user.task_status)

complete <number>:
    edit.jump_line(number)
    user.mark_status("✅")
