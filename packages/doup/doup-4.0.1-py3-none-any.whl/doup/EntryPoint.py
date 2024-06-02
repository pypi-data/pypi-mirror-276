import argparse
import time

from doup.crawler import DirectoryCrawler, DockerhubCrawler
from doup.dto.DirectorySummary import DirectorySummary
from doup.services import FileService, OutputService


def getArgs():
    parser = argparse.ArgumentParser(
        prog="doup",
        description="a tool to find and update marked dockertags in project files.",
    )
    parser.add_argument("path", type=str, help="search for dockertags in this path")
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="show the status of dockertags but dont update files",
    )

    parser.add_argument(
        "-s",
        "--show-all",
        action="store_true",
        help="show all dockertags even when no new version is published",
    )

    parser.add_argument(
        "-f",
        "--show-fullpath",
        action="store_true",
        help="prints the full filepath and not the shortend version",
    )

    args = parser.parse_args()

    return args


# -----------------------------------------------------------------------------


def main():
    start_time = time.time()
    args = getArgs()

    path = args.path
    dry_run = args.dry_run
    show_all = args.show_all
    show_fullpath = args.show_fullpath

    directorySummary: DirectorySummary = DirectorySummary()
    dockerImages = DirectoryCrawler.getImageNamesInPath(path, directorySummary)

    for dockerImage in dockerImages:
        directorySummary.raiseCounter()
        dockerImage.setNextTag(
            DockerhubCrawler.getLatestTag(
                dockerImage.repository, dockerImage.tagToFollow, "amd64"
            )
        )

        if dockerImage.nextTag == dockerImage.currentTag and show_all:
            directorySummary.addDockerImage(dockerImage, show_fullpath)

        if dockerImage.nextTag != dockerImage.currentTag:
            directorySummary.addDockerImage(dockerImage, show_fullpath)
            if not dry_run:
                nextImageName = dockerImage.getNextImageName(dockerImage.nextTag)
                FileService.replaceString(
                    dockerImage.filename, dockerImage.imageName, nextImageName
                )

    end_time = time.time()
    duration = end_time - start_time
    OutputService.printSummary(directorySummary, duration)
