# aoc template

# Setup Cookie
## How to get cookie
https://github.com/wimglenn/advent-of-code-wim/issues/1

## How to put it in this repo
Put just the value in here without the session= prefix:

Filename: utils/aoc\_cookie.json

Contents:

{"aoc-session-cookie": ""}

# How to Use
* See p.py for an example
* When `aoc(ans, l=1)` is executed it submits the first problem of the day.
* If you have anything in your clipboard, that overrides and it uses that. This is for debugging.
* Call `./c` to clear what's in your clipboard.
* If the second day is `oac(None, l=2)` or any day has `None` it doesn't prompt you to submit that day.
* When prompted to submit, if you only want to submit for level 2, you type `n` for level 1 to skip.
* The main function for submission occurs in `utils/aoc.aoc_submit` so take a look to understand.
