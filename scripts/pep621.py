from batchpr import Updater
from peppyproject import PyProjectConfiguration
import os
import sys
from getpass import getpass
from pathlib import Path


class PEP621(Updater):
    def process_repo(self) -> bool:
        # This method should contain any code that you want to run inside
        # the repository to make the changes/updates. You can assume that
        # the current working directory is the repository being processed.
        # This method should return False if it was not able to make the
        # changes, and True if it was. This method should call self.add
        # to git add any files that have changed, but should not commit.

        filenames = [
            filename
            for filename in Path().cwd().iterdir()
            if filename.is_file() and filename in ["setup.cfg", "setup.py"]
        ]

        if len(filenames) > 0:
            try:
                configuration = PyProjectConfiguration.from_directory(".")
                configuration.to_file("pyproject.toml")
                self.add("pyproject.toml")

                if (
                    configuration._PyProjectConfiguration__tables.get("tool")
                    is not None
                ):
                    print(
                        "`flake8` does not support `pyproject.toml`; you should use `ruff` instead.\nTo keep the `flake8` configuration, move it to an INI file called `.flake8`",
                        file=sys.stderr,
                    )
                    return False
                os.remove("setup.cfg")
                self.add("setup.cfg")

                with open("setup.py", "r") as setup_py:
                    if "Extension" in setup_py.read():
                        print(
                            "`setup.py` contains `Extension`; you will need to set up a shim `setup.py` to handle extensions",
                            file=sys.stderr,
                        )
                        return False
                os.remove("setup.py")
                self.add("setup.py")
            except:
                return False
        else:
            return False

        return True

    @property
    def commit_message(self) -> str:
        # The commit message to use when making the changes
        return "apply PEP621 to consolidate configuration into `pyproject.toml`"

    @property
    def pull_request_title(self) -> str:
        # The title of the pull request
        return "[PEP621] consolidate build configuration into `pyproject.toml`"

    @property
    def pull_request_body(self) -> str:
        # The main body/description of the pull request
        return (
            "`setuptools` now supports the `[project]` table, which is defined by [PEP621](https://peps.python.org/pep-0621).\n"
            "\n"
            "Additionally, `setuptools` now supports its own entry in `pyproject.toml` called `[tool.setuptools]` (https://github.com/pypa/setuptools/issues/1688, https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#setuptools-specific-configuration)\n"
            "\n"
            "Reading `toml` is supported natively in Python 3.11 with `tomllib`\n"
            "\n"
            "Given this, we can consolidate the build configuration into a single `pyproject.toml` file that can possibly be read by other build systems in the future."
            "\n"
            "\n"
            "> [!NOTE]\n"
            "> This is an automated update made by the ``batchpr`` tool :robot: - feel free to close if it doesn't look good! You can report issues to @astrofrog."
        )

    @property
    def branch_name(self) -> str:
        # The name of the branch to use
        return "pep621"


if __name__ == "__main__":
    GITHUB_TOKEN = getpass(
        "enter GitHub token with permission to create forks, branches, and pull requests:"
    )

    helper = PEP621(token=GITHUB_TOKEN)

    repos = [
        "spacetelescope/jwst",
    ]

    helper.run(repos)
