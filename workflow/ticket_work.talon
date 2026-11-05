<user.kiv_ticket>: insert(kiv_ticket)

open ember <number>:
    user.open_in_brave("https://linear.app/ember-and-tide/issue/EMB-{number}")

show pr <number>:
    user.open_in_brave("https://github.com/adam-edison/kivaro/pull/{number}")
