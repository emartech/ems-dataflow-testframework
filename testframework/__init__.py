from os import path

RESOURCES = full_path = path.abspath("testframework/resources")


def resource(resource_name: str):
    return path.join(RESOURCES, resource_name)
