import re

from doup.analyzer import StringAnalyzer


def hasMajorVersionUpdate(currentVersion: str, nextTag: str):
    hasMajorVersionUpdate = False
    currentMajorVersion = getMajorVersionNumber(currentVersion)
    nextMajorVersion = getMajorVersionNumber(nextTag)

    if nextMajorVersion != currentMajorVersion:
        hasMajorVersionUpdate = True

    return hasMajorVersionUpdate


def getMajorVersionNumber(version: str):
    match = re.search("\\d+\\.\\d+\\.\\d+", version)
    versionNumber = ""
    majorVersion = ""
    if match:
        versionNumber = match.group(0)

    match = re.search("\\d+", versionNumber)
    if match:
        majorVersion = match.group(0)

    return majorVersion


def getLongestTag(tags: list):
    tagsToRemove = []
    for tag in tags:
        if not StringAnalyzer.hasNumbers(tag):
            tagsToRemove.append(tag)

    for tag in tagsToRemove:
        tags.remove(tag)

    latestVersion = StringAnalyzer.getLongest(tags)
    return latestVersion
