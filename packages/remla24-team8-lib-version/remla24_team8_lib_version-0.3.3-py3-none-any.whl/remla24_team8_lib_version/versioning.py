import os

class VersionUtil:
    def __init__(self):
        self.version = self.get_version()

    @staticmethod
    def get_version():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        pyproject_toml = os.path.join(current_dir, "..", "..", "pyproject.toml")
        if os.path.exists(pyproject_toml):
            with open(pyproject_toml, "r") as f:
                for line in f:
                    if "version = " in line:
                        version = line.split("=")[1].strip().replace('"', "")
                        return version
        return "0.0.0"
