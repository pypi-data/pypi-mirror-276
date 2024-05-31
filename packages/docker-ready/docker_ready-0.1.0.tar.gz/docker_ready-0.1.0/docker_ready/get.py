from pathlib import Path

from docker_ready.project import Project

PROJECTS_DIR = Path(__file__).parent.joinpath("projects").absolute()


def get_all_projects() -> list[Project]:
    return [Project(child) for child in PROJECTS_DIR.iterdir() if child.is_dir()]


def get_project_by_name(name: str) -> Project | None:
    for child in PROJECTS_DIR.iterdir():
        if child.name == name and child.is_dir():
            return Project(child)


__all__ = ["get_all_projects", "get_project_by_name"]
