import os

HOST = os.getenv("PINNACLE_HOST", default="localhost")
PORT = int(os.getenv("PINNACLE_PORT", default=8000))
DIRECTORY = os.getenv("PINNACLE_DIRECTORY", default="./pinnacle")
PYTHON_PORT = int(PORT + 1)
