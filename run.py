# % preamble > python3 necromancer.py --role role --job job --annotation "annotation"

import typer
import sys

import random
import time

from necromancer.dispatcher import Dispatcher

app = typer.Typer()


@app.command()
def dispatch(
    role: str = typer.Option(..., help="Agent role (eg: dev, sre, etc)"),
    job: str = typer.Option(..., help="Agent job (eg: code, document, etc)"),
    annotation: str = typer.Option(..., help="Additional job context"),
) -> None:
    preamble = sys.stdin.read()
    d = Dispatcher(role, job, annotation, preamble)
    d.dispatch()


if __name__ == "__main__":
    app()
