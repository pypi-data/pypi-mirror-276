import os
import click
import asyncio
from subprocess import Popen
from dotenv import load_dotenv, find_dotenv
from pinnacle_cli.constants import HOST, PYTHON_PORT

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

        async def run_python_dev_server():
            import uvicorn

            uvicorn.run(
                "pinnacle_cli.py.dev:app", host=HOST, port=PYTHON_PORT, reload=True
            )

        Popen(
            ["npm", "run", "start-dev", cwd],
            cwd=f"{os.path.dirname(os.path.abspath(__file__))}/js",
        )

        asyncio.run(run_python_dev_server())


if __name__ == "__main__":
    main()
