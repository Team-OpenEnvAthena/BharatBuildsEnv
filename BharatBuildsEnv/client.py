"""
BharatBuilds Environment Client.

Uses a persistent WebSocket connection to the environment server for
low-latency, multi-step interactions. Each client instance gets its own
dedicated environment session on the server.

Example (Docker):
    >>> client = BharatBuildsClient.from_docker_image("bharatbuilds-env:latest")
    >>> try:
    ...     result = client.reset(founder_name="Priya")
    ...     print(result.observation.phase, result.observation.founder_name)
    ...
    ...     action = BharatAction(
    ...         ai_response="Priya, tell me more about who is facing this problem.",
    ...         suggested_task="Talk to 2 neighbours about the problem today.",
    ...         emotional_tone="encouraging",
    ...     )
    ...     result = client.step(action)
    ...     print(result.reward, result.observation.dropout_risk)
    ... finally:
    ...     client.close()

Example (running server):
    >>> with BharatBuildsClient(base_url="http://localhost:8000") as client:
    ...     result = client.reset()
    ...     result = client.step(BharatAction(ai_response="Hello!"))
"""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import BharatAction, BharatObservation


class BharatBuildsClient(EnvClient[BharatAction, BharatObservation, State]):
    """
    Client for the BharatBuilds RL Environment.

    The client maintains a WebSocket connection for efficient multi-step
    rollouts. The server isolates state per session, so multiple clients
    can run concurrent episodes.
    """

    def _step_payload(self, action: BharatAction) -> Dict:
        """
        Serialize a BharatAction into the JSON payload sent to the server.

        Args:
            action: BharatAction containing the AI co-founder's response.

        Returns:
            Dictionary with all action fields.
        """
        return action.model_dump()

    def _parse_result(self, payload: Dict) -> StepResult[BharatObservation]:
        """
        Deserialize the server's step/reset response into a StepResult.

        The server returns:
            {
              "observation": { ...all BharatObservation fields... },
              "reward": float,
              "done": bool,
              "truncated": bool,
              ...
            }

        Args:
            payload: Raw JSON dict from the server.

        Returns:
            StepResult wrapping the parsed BharatObservation.
        """
        obs_data = payload.get("observation", payload)

        # Build the observation — all fields have defaults so missing keys are safe
        observation = BharatObservation(
            phase=obs_data.get("phase", "IDEA_ARTICULATION"),
            phase_number=obs_data.get("phase_number", 0),
            phase_goal=obs_data.get("phase_goal", ""),
            founder_name=obs_data.get("founder_name", ""),
            founder_location=obs_data.get("founder_location", ""),
            founder_tier=obs_data.get("founder_tier", "tier2"),
            founder_language=obs_data.get("founder_language", "hindi"),
            founder_domain=obs_data.get("founder_domain", "edtech"),
            founder_digital_literacy=obs_data.get("founder_digital_literacy", 0.5),
            founder_capital_inr=obs_data.get("founder_capital_inr", 10000.0),
            founder_prior_attempt=obs_data.get("founder_prior_attempt", False),
            founder_emotional_state=obs_data.get("founder_emotional_state", "excited"),
            founder_user_relationship=obs_data.get("founder_user_relationship", "familiar"),
            validation_threshold=obs_data.get("validation_threshold", 4),
            idea_description=obs_data.get("idea_description", ""),
            validation_interviews_done=obs_data.get("validation_interviews_done", 0),
            mvp_shipped=obs_data.get("mvp_shipped", False),
            first_customer=obs_data.get("first_customer", False),
            dropout_risk=obs_data.get("dropout_risk", 0.0),
            tasks_completed=obs_data.get("tasks_completed", 0),
            tasks_ignored=obs_data.get("tasks_ignored", 0),
            felt_unblocked=obs_data.get("felt_unblocked", False),
            felt_judged=obs_data.get("felt_judged", False),
            available_schemes=obs_data.get("available_schemes", []),
            available_tools=obs_data.get("available_tools", []),
            available_communities=obs_data.get("available_communities", []),
            step=obs_data.get("step", 0),
            done=payload.get("done", obs_data.get("done", False)),
            reward=payload.get("reward", obs_data.get("reward", 0.0)),
            terminated=obs_data.get("terminated", False),
            truncated=obs_data.get("truncated", False),
            verifier_flags=obs_data.get("verifier_flags", []),
            verifier_scores=obs_data.get("verifier_scores", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward", obs_data.get("reward", 0.0)),
            done=payload.get("done", obs_data.get("done", False)),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Deserialize the server's state response.

        Args:
            payload: Raw JSON dict from the server.

        Returns:
            State object with episode_id and step_count.
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )
