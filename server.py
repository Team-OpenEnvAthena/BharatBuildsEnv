from openenv.core import create_fastapi_app
from environment import BharatBuildsEnv, BharatAction, BharatObservation
from verifiers import run_all_verifiers

app = create_fastapi_app(BharatBuildsEnv, BharatAction, BharatObservation)