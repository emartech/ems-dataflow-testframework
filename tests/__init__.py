from os import path

TEST_RESOURCES = full_path = path.abspath("tests/resources")


def resource(resource_name: str):
    return path.join(TEST_RESOURCES, resource_name)
