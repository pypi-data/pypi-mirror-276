import time

import typer

app = typer.Typer()

with typer.progressbar(length=4, label="Creating project structure") as bar:
    for value in bar:
        time.sleep(0.5)
        print(value)
        bar.label = "generating files"
        bar.update(value)
