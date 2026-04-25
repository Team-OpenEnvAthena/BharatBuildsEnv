from openenv.core import create_fastapi_app
from environment import BharatBuildsEnv, BharatAction, BharatObservation

# Verifiers are called inside BharatBuildsEnv.step() — not needed here
app = create_fastapi_app(BharatBuildsEnv, BharatAction, BharatObservation)
