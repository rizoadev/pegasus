import typer
from api.events.config import Config

app = typer.Typer()
config = Config.load()


@app.command()
def install():
    typer.echo(f"install")


@app.command()
def migrate():
    typer.echo(f"migrate")


if __name__ == "__main__":
    app()