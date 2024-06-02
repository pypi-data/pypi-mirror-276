def replaceString(filename: str, oldValue: str, newValue: str) -> bool:
    data = getUpdatedData(filename, oldValue, newValue)
    updateFile(filename, data)

    return True


def getUpdatedData(filename: str, oldValue: str, newValue: str) -> str:
    file = open(filename, "rt")
    data = file.read()
    data = data.replace(oldValue, newValue)
    file.close()

    return data


def updateFile(filename: str, data: str):
    file = open(filename, "wt")
    file.write(data)
    file.close()
