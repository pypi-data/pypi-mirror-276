# 🚀 doup

A command line tool to find and update dockertags in project files.

[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
[![pipeline main](https://gitlab.com/doup1/doup/badges/main/pipeline.svg)](https://gitlab.com/doup1/doup/blob/feature/update_readme/README.md)

## Why you should use doup

The version of docker images should not set to `latest` to avoid upgrade nightmares and ensure the stability of your environment.
But containers should also be upgraded regulary to get new features and fixes of security issues.

You have to check for each container individually if a new version is published or not.
`doup` can save you a lot of time and is taking this task from you.

### Example

```bash
  ~/dev/repos/best_repo_ever (main)
 > doup --dry-run .

Finished in 20 seconds.
Searched in 11547 files and found 17 managed docker images.

| Filename          | Repository                   | Tag                        | Next                      | hasMajorVersionUpdate   |
|-------------------|------------------------------|----------------------------|---------------------------|-------------------------|
| all/vars.yml      | plantuml/plantuml-server     | jetty-v1.2022.14           | jetty-v1.2023.0           | False                   |
| all/vars.yml      | louislam/uptime-kuma         | 1.19.2-alpine              | 1.19.4-alpine             | False                   |
| all/jellyfin.yml  | jellyfin/jellyfin            | 20221230.11-unstable-amd64 | 20230114.9-unstable-amd64 | False                   |
| all/container.yml | homeassistant/home-assistant | 2023.1.1                   | 2023.1.4                  | False                   |
```

## Prepare your project for doup

Each dockerimage has to be marked in the previous line:

```yml
# doup:latest
haproxy_docker_image: haproxy:2.6.2-bullseye
```

- `doup`: doup is looking for lines which contains `doup:*`
- `latest`: the tag on dockerhub which is used to get the latest concrete tag

## QuickSetup

`doup` is published on PyPi and can be installed with `pip install doup`.
Afterwards you should mark some Docker-Version-Strings in your project and run `doup --dry-run`.

## Incoming features

- add output: release date of docker image
- add command: `doup list images`
  - list marked dockertags
- add command:`doup find images`
  - finds not marked dockertags
