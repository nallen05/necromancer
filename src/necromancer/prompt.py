# prompt.py

from pathlib import Path
import os

import pyprojroot

from jinja2 import Environment, FileSystemLoader


# --------------- jinja setup ---------------------

PROJECT_DIR = pyprojroot.here()

TEMPLATE_DIR = Path(PROJECT_DIR / "templates" / "necromancer")

print(f"Template dir: {TEMPLATE_DIR}")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def _validate_template_file(name: str) -> bool:
    if os.path.exists(Path(TEMPLATE_DIR / (name + ".txt"))):
        return True
    else:
        raise ValueError(f"Template file does not exist: {name}")


def _render_template(name: str, context: dict) -> str:
    template = env.get_template(name + ".txt")
    return template.render(context)


# --------------- known roles & jobs ---------------------

ROLES = {"architect", "dev", "sre", "staff"}

JOBS = {
    "code": "code",
    "review": "marukdown",
    "context_overview": "markdown",
    "context_sanitycheck": "markdown",
    "context_tool": "markdown",
    "plan": "markdown",
    "sketch": "pseudocode",
}


# --------------- API ---------------------


class Prompt:
    def __init__(self, role: str, job: str, annotation: str, preamble: str):
        if role in ROLES:
            self.role = role
            _validate_template_file("role_" + role)
        else:
            raise ValueError(f"Invalid role: {role}")

        if job in JOBS:
            self.response_type = JOBS[job]
            self.job = job
            _validate_template_file("job_" + job)
        else:
            raise ValueError(f"Invalid job: {job}")

        self.annotation = annotation
        self.preamble = preamble

    def build(self):
        context = {
            "goal": [],
            "task": [],
            "response_type": self.response_type,
            "data": self.preamble,
        }
        self.system_prompt = _render_template("role_" + self.role, context)
        self.user_prompt = _render_template("job_" + self.job, context)
