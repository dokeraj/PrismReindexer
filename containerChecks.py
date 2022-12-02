import docker
import sys
import configInit
import time


def checkPhotoprismValidity(container):
    if "photoprism" in container.attrs["Config"]["Image"]:
        return True
    else:
        return False


def checkPhotoprismAvailability(dockerClient, config):
    try:
        container = dockerClient.containers.get(config.photoprismContainerName)
        if str(container.status).lower() == "running":
            return True, container
        else:
            return False, None
    except Exception as e:
        return False, None


def mainChecks():
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    except Exception as e:
        print("ERROR: Cannot find docker server! Now exiting!")
        sys.exit(0)

    print("Reading the config from the YAML file...")
    config = configInit.initConfig()

    print("Checking the availability and validity of Photoprism container...")
    available, container = checkPhotoprismAvailability(client, config)

    if not available:
        print(
            f"WARN: The container name {config.photoprismContainerName} is not valid or the container is stopped - trying again in 5 minutes")
        time.sleep(300)
        return mainChecks()

    if not checkPhotoprismValidity(container):
        print(f"ERROR: The container with name {config.photoprismContainerName} is not created from the photoprism image! Please use a container that it is the Photoprism! Now exiting!")
        sys.exit(0)

    print("SUCCESS: The specified container is currently running and is in fact Photoprism container!")
    return container, config
