from tabulate import tabulate
from termcolor import colored

from doup.dto.DirectorySummary import DirectorySummary


def printSummary(directorySummary: DirectorySummary, duration: float):
    print("")
    print("Finished in " + colored(str(int(duration)), "yellow") + " seconds.")
    print(
        "Searched in "
        + colored(str(directorySummary.numberOfFiles), "yellow")
        + " files and found "
        + colored(str(directorySummary.numberOfDockerImages), "yellow")
        + " managed docker images."
    )
    print("")
    print(
        tabulate(
            directorySummary.imageTable,
            headers=directorySummary.imageTableHeader,
            tablefmt="github",
        )
    )
