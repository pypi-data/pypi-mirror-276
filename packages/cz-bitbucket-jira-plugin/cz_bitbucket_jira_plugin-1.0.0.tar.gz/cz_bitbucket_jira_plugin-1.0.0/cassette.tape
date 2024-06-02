Output demo.gif

Set Shell zsh
Set LoopOffset 95%

# Trigger cz commit
Sleep 1s
Type@100ms "cz commit --dry-run"
Sleep 1s
Enter

# Jira project key
Sleep 2s
Enter
Sleep 1.5s
Type@200ms "DEV-"
Sleep 1.5s
Backspace@200ms 4
Sleep 500ms
Type@200ms "1500"
Sleep 1s
Enter

# Issue number
Enter
Sleep 1.5s
Enter
Sleep 1s
Type@200ms "2000"
Sleep 1s
Enter

# Issue subtask
Sleep 1s
Type@200ms "2001"
Sleep 200ms
Type@100ms ","
Sleep 200ms
Type@200ms " 2002"
Sleep 1s
Enter

# Issue related tasks
Sleep 1s
Type@200ms "3000"
Sleep 1s
Enter

# Commit type
Sleep 1
Down
Sleep 350ms
Down
Sleep 350ms
Down
Sleep 350ms
Down
Sleep 350ms
Down
Sleep 1.3s
Enter

# Commit title
Sleep 1s
Type@100ms "Implement fibonacci using recursion"
Sleep 300ms
Enter

# Commit description
Sleep 1s
Type@100ms "Recursion is hard, but it works"
Sleep 300ms
Alt+Enter

# Footer
Sleep 1s
Type@200ms "DEV-2000 #done"
Sleep 500ms
Alt+Enter

Sleep 7s
