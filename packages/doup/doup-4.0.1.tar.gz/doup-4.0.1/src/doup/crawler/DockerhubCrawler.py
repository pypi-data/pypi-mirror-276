import json

import requests

from doup.analyzer import TagAnalyzer


def getLatestTag(repository: str, tag: str, architecture: str) -> str:
    digest = getDigestOfTag(repository, tag, architecture)
    allTagsToDigest = getAllTagsToDigest(repository, digest)
    nextTag = TagAnalyzer.getLongestTag(allTagsToDigest)

    return nextTag


def getDigestOfTag(repository: str, tag: str, architecture: str):
    url = "https://hub.docker.com/v2/repositories/" + repository + "/tags/" + tag

    response = requests.get(url)
    bar = json.loads(response.text)
    images = bar["images"]

    digest = ""
    for image in images:
        if image["architecture"] == architecture:
            digest = image["digest"]

    return digest


def getAllTagsToDigest(repository: str, digest: str):
    url = (
        "https://hub.docker.com/v2/repositories/" + repository + "/tags/?page_size=1000"
    )

    response = json.loads(requests.get(url).text)
    tags = []
    for result in response["results"]:
        for image in result["images"]:
            tag_digest = image.get("digest")
            if tag_digest and tag_digest == digest:
                tags.append(result["name"])
    return tags
