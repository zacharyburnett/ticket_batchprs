from batchpr import Updater
from getpass import getpass
import tomllib
from pathlib import Path
import tomli_w


PINNED_PYTHON_MINOR_VERSION = 10


class BumpPythonMinorVersion(Updater):
    def process_repo(self):
        # This method should contain any code that you want to run inside
        # the repository to make the changes/updates. You can assume that
        # the current working directory is the repository being processed.
        # This method should return False if it was not able to make the
        # changes, and True if it was. This method should call self.add
        # to git add any files that have changed, but should not commit.

        required_python = None

        pyproject_toml = Path("pyproject.toml")

        if pyproject_toml.exists():
            with open("pyproject.toml", "rb") as pyproject_toml_file:
                pyproject_metadata = tomllib.load(pyproject_toml_file)

            required_python = pyproject_metadata["project"]["requires-python"].split(
                "."
            )

            if int(required_python[1]) <= PINNED_PYTHON_MINOR_VERSION - 1:
                required_python[1] = str(PINNED_PYTHON_MINOR_VERSION)
                pyproject_metadata["project"]["requires-python"] = ".".join(
                    required_python
                )

                with open("pyproject.toml", "wb") as pyproject_toml_file:
                    tomli_w.dump(pyproject_metadata, pyproject_toml_file)
                self.add('pyproject.toml')

                return True

        for filename in [Path("setup.cfg"), Path("setup.py")]:
            if filename.exists():
                with open(filename) as setup_file:
                    lines = setup_file.readlines()

                for index in range(len(lines)):
                    line = lines[index]
                    if "python_requires" in line:
                        line_parts = line.split("=", maxsplit=1)
                        required_python = line_parts[1].split(".")

                        if int(required_python[1]) <= PINNED_PYTHON_MINOR_VERSION - 1:
                            required_python[1] = str(PINNED_PYTHON_MINOR_VERSION)
                            line_parts[1] = ".".join(required_python)
                            lines[index] = "=".join(line_parts)

                            with open(filename, 'w') as setup_file:
                                setup_file.writelines(lines)
                            self.add(filename)

                            return True
                        return False
        return False

    @property
    def commit_message(self) -> str:
        # The commit message to use when making the changes
        return "require Python 3.10"

    @property
    def pull_request_title(self) -> str:
        # The title of the pull request
        return "[SCSB-145] require Python 3.10"

    @property
    def pull_request_body(self) -> str:
        # The main body/description of the pull request
        return (
            "resolves [SCSB-145](https://jira.stsci.edu/browse/SCSB-145)\n"
            "\n"
            "propagate Astropy's deprecation of Python 3.9 to downstream packages\n"
            "\n"
            "\n"
            "> [!NOTE]\n"
            "> This is an automated update made by the ``batchpr`` tool :robot: - feel free to close if it doesn't look good! You can report issues to @astrofrog."
        )

    @property
    def branch_name(self) -> str:
        # The name of the branch to use
        return "scsb145"


if __name__ == "__main__":
    GITHUB_TOKEN = getpass(
        "enter GitHub token with permission to create forks, branches, and pull requests:"
    )

    helper = BumpPythonMinorVersion(token=GITHUB_TOKEN)

    repos = [
        "spacetelescope/jwst",
    ]

    helper.run(repos)
