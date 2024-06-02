def getRepository(imageName: str) -> str:
    stringArray = imageName.split(":")[0].split("/")

    if len(stringArray) == 2:
        repository = stringArray[0] + "/" + stringArray[1]
    else:
        repository = "library/" + stringArray[0]

    return repository.strip()


def getTag(imageName: str) -> str:
    return imageName.split(":")[1].strip()
