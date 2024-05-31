import os
import sys
import importlib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pinnacle_python.endpoints import endpoints
from pinnacle_cli.constants import HOST, PYTHON_PORT, DIRECTORY

app = FastAPI()

sys.path.append(os.getcwd())

for filename in os.listdir(DIRECTORY):
    if filename.endswith(".py"):
        module_name = os.path.splitext(filename)[0]
        module_parent = (
            DIRECTORY[2:] if DIRECTORY.startswith("./") else DIRECTORY
        ).replace("/", ".")
        importlib.import_module(f"{module_parent}.{module_name}")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
available_routes = []


def route_factory(endpoint):
    route_name = endpoint.__name__
    params = endpoint.__annotations__.items()

    @app.api_route(f"/{route_name}", methods=["POST"])
    async def route_handler(request: Request):
        params = await request.json()

        params_dict = {}

        for param, _ in params.items():
            if param != "return":
                params_dict[param] = params[param]

        return JSONResponse(content={"data": endpoint(**params_dict)})

    return (route_name, params)


for endpoint in endpoints:
    route_name, params = route_factory(endpoint)

    print(f"http://{HOST}:{PYTHON_PORT}/{route_name}")
