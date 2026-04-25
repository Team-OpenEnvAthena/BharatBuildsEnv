"""
FastAPI application for the BharatBuilds Environment.

Exposes the BharatBuildsEnvEnvironment over HTTP and WebSocket endpoints,
compatible with the BharatBuildsClient (EnvClient).

Endpoints:
    POST /reset          — Start a new episode (returns initial observation)
    POST /step           — Execute one action
    GET  /state          — Get current episode state
    GET  /schema         — Action/observation schemas
    WS   /ws             — Persistent WebSocket for low-latency episodes
    GET  /web            — Interactive UI (README-powered)
    GET  /health         — Health check
    GET  /docs           — Swagger UI

Usage:
    # Development (auto-reload):
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

    # Production:
    uvicorn server.app:app --host 0.0.0.0 --port 8000

    # Or directly:
    python -m server.app
"""

try:
    from openenv.core.env_server.http_server import create_app
except ImportError as e:
    raise ImportError(
        "openenv is required. Install with:\n    uv sync\n"
    ) from e

try:
    from server.models import BharatAction, BharatObservation
    from .BharatBuildsEnv_environment import BharatBuildsEnvEnvironment
except ModuleNotFoundError:
    from models import BharatAction, BharatObservation
    from server.BharatBuildsEnv_environment import BharatBuildsEnvEnvironment


# Create the FastAPI app with web UI and concurrent session support.
# Increase max_concurrent_envs for parallel training rollouts.
app = create_app(
    BharatBuildsEnvEnvironment,
    BharatAction,
    BharatObservation,
    env_name="BharatBuildsEnv",
    max_concurrent_envs=4,  # Allow 4 concurrent WebSocket sessions
)


def main(host: str = "0.0.0.0", port: int = 8000):
    """
    Entry point for direct execution.

        uv run --project . server
        python -m server.app
        uvicorn server.app:app --workers 4

    Args:
        host: Host to bind (default: 0.0.0.0)
        port: Port to listen on (default: 8000)
    """
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(port=args.port)
