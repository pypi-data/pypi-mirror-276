import os
import click
from dotenv import load_dotenv, find_dotenv
from pinnacle_cli.constants import HOST, PORT

cwd = os.getcwd()
env_path = os.path.join(cwd, ".env")
found_dotenv = find_dotenv(env_path)
if found_dotenv:
    load_dotenv(env_path, override=True)


@click.command()
@click.argument("mode", required=True, type=click.Choice(["dev", "prod"]))
def main(mode: str) -> None:
    if mode == "dev":
        click.echo("Running in development mode")

        import uvicorn

        uvicorn.run("pinnacle_cli.python.dev:app", host=HOST, port=PORT, reload=True)


if __name__ == "__main__":
    main()
