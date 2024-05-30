import subprocess
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from foundry_dev_tools.utils.repo import get_repo, git_toplevel_dir

if TYPE_CHECKING:
    import py.path


@pytest.mark.parametrize(
    "use_git", [False]
)  # only False, as we test use_git=True with test_get_repo
def test_git_toplevel_dir(use_git: bool, tmpdir: "py.path.LocalPath", git_env: dict):
    toplevel = Path(tmpdir)
    subprocess.check_call(["git", "init"], cwd=toplevel)
    git_dir = git_toplevel_dir(Path(tmpdir.mkdir("subdireectory")), use_git=use_git)
    assert git_dir == toplevel
    with tmpdir.mkdir("second_subdirectory").as_cwd():
        git_dir_cwd = git_toplevel_dir(use_git=use_git)
    assert git_dir_cwd == toplevel

    # Test if git submodules can be recognized as toplevel_dir
    # First create an empty local repository and initialize it
    subprocess.check_call(["git", "init", "dummy_repo"], cwd=toplevel, env=git_env)
    subprocess.check_call(
        [
            "git",
            "commit",
            "--allow-empty",
            "-m",
            "Initialize",
        ],
        cwd=toplevel.joinpath("dummy_repo"),
        env=git_env,
    )

    # Add local repository as submodule to toplevel repo
    subprocess.check_call(
        [
            "git",
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "add",
            "./dummy_repo",
            "dummy_submodule",
        ],
        cwd=toplevel,
    )
    toplevel_submodule = toplevel.joinpath("dummy_submodule")
    git_dir_submodule = git_toplevel_dir(
        Path(tmpdir.mkdir("dummy_submodule", "submodule_subdirectory")), use_git=use_git
    )
    assert git_dir_submodule == toplevel_submodule


def test_get_repo(tmpdir: "py.path.LocalPath", git_env: dict):
    repo_rid = f"ri.stemma.main.repository{uuid.uuid4()}"
    git_dir = Path(tmpdir)
    subprocess.check_call(["git", "init"], cwd=git_dir)
    with git_dir.joinpath("gradle.properties").open("w+") as gradle_prop:
        gradle_prop.write(f"transformsRepoRid = {repo_rid}")

    subprocess.check_call(["git", "add", "gradle.properties"], cwd=git_dir, env=git_env)
    subprocess.check_call(
        ["git", "commit", "-m", "initial commit"], cwd=git_dir, env=git_env
    )
    assert get_repo(git_dir)[0] == repo_rid
    with tmpdir.as_cwd():
        get_repo_out = get_repo()
        assert get_repo_out[0] == repo_rid
        assert get_repo_out[3] == git_dir
