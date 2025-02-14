#!/usr/bin/env python3

def evaluate(ln, on, result):
    i = 0
    while i < len(ln):
        if ln[i:i + 2].lower() == 'on':
            on = True
            i += 2
        elif ln[i:i + 3].lower() == 'off':
            on = False
            i += 3
        elif ln[i].isdigit():
            n = 0
            while i < len(ln) and ln[i].isdigit():
                n = n * 10 + int(ln[i])
                i += 1
            if on:
                result += n
        elif ln[i] == '=':
            print(result)
            i += 1
        else:
            i += 1  # Skip non-recognized characters

    return on, result


def main():
    on = True
    result = 0
    while True:
        try:
            ln = input()
        except (EOFError, KeyboardInterrupt):
            print(result)
            break

        on, result = evaluate(ln, on, result)


main()
