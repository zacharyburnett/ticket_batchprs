from batchpr import Updater
from peppyproject import PyProjectConfiguration
import sys
import os


class BumpPython(Updater):
    def process_repo(self):
        # This method should contain any code that you want to run inside
        # the repository to make the changes/updates. You can assume that
        # the current working directory is the repository being processed.
        # This method should return False if it was not able to make the
        # changes, and True if it was. This method should call self.add
        # to git add any files that have changed, but should not commit.

        pyproject_toml = Path("pyproject.toml")
        if pyproject_toml.exists():
            with open("pyproject.toml", "rb") as pyproject_toml_file:
                pyproject_metadata = tomllib.read(pyproject_toml_file)

        setup_cfg = Path("setup.cfg")
        if setup_cfg.exists():
            pass

    def process_repo(self):
        # This method should contain any code that you want to run inside
        # the repository to make the changes/updates. You can assume that
        # the current working directory is the repository being processed.
        # This method should return False if it was not able to make the
        # changes, and True if it was. This method should call self.add
        # to git add any files that have changed, but should not commit.
        configuration = PyProjectConfiguration.from_directory(".")
        configuration.to_file("pyproject.toml")

        if configuration._PyProjectConfiguration__tables.get("tool") is not None:
            print(
                "`flake8` does not support `pyproject.toml`; you should use `ruff` instead.\nTo keep the `flake8` configuration, move it to an INI file called `.flake8`",
                file=sys.stderr,
            )

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

    helper = BumpPython(token=GITHUB_TOKEN)

    repos = [
        "spacetelescope/jwst",
    ]

    helper.run(repos)
