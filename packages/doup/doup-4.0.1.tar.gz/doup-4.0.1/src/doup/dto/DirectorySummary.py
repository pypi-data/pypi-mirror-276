from doup.dto.DockerImage import DockerImage


class DirectorySummary:
    numberOfFiles: int
    numberOfDockerImages: int
    imageTable: list[list[str]]
    imageTableHeader = [
        "Filename",
        "Repository",
        "Tag",
        "Next",
        "hasMajorVersionUpdate",
    ]

    dockerImages: list[list[str]]

    def __init__(self):
        self.numberOfFiles = 0
        self.numberOfDockerImages = 0
        self.imageTable = []

    def raiseCounter(self):
        self.numberOfDockerImages += 1

    def addDockerImage(self, dockerImage: DockerImage, show_fullpath: bool):
        filename = dockerImage.filename

        if not show_fullpath:
            parts = dockerImage.filename.split("/")
            length = len(parts)
            filename = parts[length - 2] + "/" + parts[length - 1]

        tableEntry = [
            filename,
            dockerImage.repository,
            dockerImage.currentTag,
            dockerImage.nextTag,
            str(dockerImage.hasMajorVersionUpdate),
        ]
        self.imageTable.append(tableEntry)
