import re


def hasLetters(string: str):
    pattern = "[a-zA-Z]"
    hasLetters = False

    if re.findall(pattern, string):
        hasLetters = True

    return hasLetters


def hasNumbers(string: str):
    pattern = "[0-9]"
    answer = False

    if re.findall(pattern, string):
        answer = True

    return answer


def getLongest(strings: list):
    previousString = ""
    longestString = ""
    for currentString in strings:
        if not previousString:
            longestString = currentString
            previousString = currentString
            continue

        if len(currentString) > len(longestString):
            longestString = currentString

        previousString = currentString

    return longestString
