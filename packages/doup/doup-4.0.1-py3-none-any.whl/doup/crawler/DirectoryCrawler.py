import glob
import re

from doup.analyzer import StringAnalyzer
from doup.dto.DirectorySummary import DirectorySummary
from doup.dto.DockerImage import DockerImage


def getImageNamesInPath(path: str, directorySummary: DirectorySummary):
    files = glob.iglob(path + "/**/*", recursive=True)
    dockerImages: list[DockerImage] = []
    numberOfFiles = 0
    for file in files:
        directorySummary.numberOfFiles += 1
        dockerImages.extend(getImageNamesInFile(file))
        numberOfFiles += 1

    return dockerImages


def getImageNamesInFile(filepath: str) -> list[DockerImage]:
    dockerImages = []

    try:
        with open(filepath, "r") as currentFile:
            previousLine = ""
            for line in currentFile:
                if containsDockerImageAndMarker(line, previousLine):
                    dockerImage = getDockerImage(line, previousLine, filepath)
                    dockerImages.append(dockerImage)
                previousLine = line
    except UnicodeDecodeError:
        pass
    except IsADirectoryError:
        pass

    return dockerImages


def containsDockerImageAndMarker(line: str, previousLine: str) -> bool:
    hasDockerImage = False

    version = getImageName(line)
    tag = getDockerImagetag(previousLine)

    if version and tag:
        hasDockerImage = True

    return hasDockerImage


def getDockerImage(line: str, previousLine: str, filepath: str):
    version = getImageName(line)
    tag = getDockerImagetag(previousLine)

    return DockerImage(version, tag, filepath)


def getImageName(string: str) -> str:
    pattern = "\\s[\\w\\-]+[/\\w\\-]+:[\\w\\-\\.]+$"
    isMatch = re.search(pattern, string)
    version = ""

    if isMatch:
        matchGroup = isMatch.group()
        if isValidDockerImage(matchGroup):
            version = matchGroup

    return version.strip()


def isValidDockerImage(matchGroup: str) -> bool:
    containsLetters = StringAnalyzer.hasLetters(matchGroup)
    containsNumbers = StringAnalyzer.hasNumbers(matchGroup)

    if containsNumbers and containsLetters and len(matchGroup) < 60:
        return True

    return False


def getDockerImagetag(line: str) -> str:
    pattern = "doup:.*"
    isMatch = re.search(pattern, line)
    tag = ""

    if isMatch:
        tag = isMatch.group().split(":")[1]

    return tag
