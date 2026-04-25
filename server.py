from openenv.core import create_fastapi_app
from environment import BharatBuildsEnv
from verifiers import run_all_verifiers

app = create_fastapi_app(BharatBuildsEnv)