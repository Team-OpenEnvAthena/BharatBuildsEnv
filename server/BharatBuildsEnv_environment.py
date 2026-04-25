"""
BharatBuilds — Core RL Environment

OpenEnv-compliant environment simulating a first-time Indian founder's
startup journey across 7 phases. The AI agent is rewarded for helping
the human take real steps — not for deciding for them.

Fixes applied vs v1:
  - action.dict() → action.model_dump() (Pydantic v2)
  - Validation threshold reads from founder profile (not hardcoded 5)
  - Double penalty removed: env_reward covers human signals only;
    verifiers cover quality signals only
  - Duplicate MAX_STEPS definition removed
  - Redundant reset fields removed
"""

import random
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import BharatAction, BharatObservation
except ImportError:
    from models import BharatAction, BharatObservation

try:
    from .data import FOUNDERS, IDEAS, PHASES, PHASE_GOALS, RESOURCES, VALIDATION_THRESHOLDS
    from .verifiers import run_all_verifiers
except ImportError:
    from data import FOUNDERS, IDEAS, PHASES, PHASE_GOALS, RESOURCES, VALIDATION_THRESHOLDS
    from verifiers import run_all_verifiers


MAX_STEPS = 50


class BharatBuildsEnvEnvironment(Environment):
    """
    Simulates a first-time Indian entrepreneur's startup journey.

    The AI agent acts as a co-founder. A simulated human (the founder)
    reacts to the AI's suggestions. The reward signal is whether the
    human took a meaningful step forward — not whether the AI completed
    a task.

    7 Phases:
        IDEA_ARTICULATION → VALIDATION → MVP_SCOPING → RESOURCE_MAPPING
        → BUILD_COMPANION → FIRST_CUSTOMER → SIGNAL_READING → DONE

    Two reward sources (non-overlapping):
        env_reward      — human engagement signals (tasks, retention, phase progression)
        verifier_reward — AI quality signals (jargon, autonomy, safety)

    Example:
        >>> env = BharatBuildsEnvEnvironment()
        >>> obs = env.reset(founder_name="Priya")
        >>> print(obs.phase, obs.founder_name)
        IDEA_ARTICULATION Priya
        >>> action = BharatAction(
        ...     ai_response="Tell me who this problem affects most.",
        ...     suggested_task="Talk to 2 people about the problem today.",
        ...     emotional_tone="encouraging",
        ... )
        >>> obs = env.step(action)
        >>> print(obs.reward, obs.dropout_risk)
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self, **kwargs):
        """Initialise the environment with a fresh episode."""
        self._episode_id = str(uuid4())
        self._reset_internal()

    def _reset_internal(self):
        self._f = None
        self._phase_idx = 0
        self._step_count = 0
        self._cumulative_reward = 0.0
        self._interviews = 0
        self._first_customer = False
        self._mvp_shipped = False
        self._dropout_risk = 0.0
        self._tasks_completed = 0
        self._tasks_ignored = 0
        self._felt_unblocked = False
        self._felt_judged = False
        self._last_verifier_flags = []
        self._last_verifier_scores = {}

    # ── OpenEnv interface ──────────────────────────────────────────────────

    def reset(self, founder_name: str = None, seed: int = None, **kwargs) -> BharatObservation:
        """
        Reset the environment for a new episode.

        Args:
            founder_name: Optional name to select a specific founder profile.
            seed:         Optional random seed for reproducibility.

        Returns:
            Initial BharatObservation.
        """
        if seed is not None:
            random.seed(seed)
        self._episode_id = str(uuid4())
        self._reset_internal()

        if founder_name:
            matches = [f for f in FOUNDERS if f["name"] == founder_name]
            self._f = matches[0] if matches else random.choice(FOUNDERS)
        else:
            self._f = random.choice(FOUNDERS)

        return self._observe(reward=0.0, terminated=False, truncated=False)

    def step(self, action: BharatAction, **kwargs) -> BharatObservation:
        """
        Execute one step: run verifiers, simulate human reaction, update state.

        Args:
            action: BharatAction from the AI agent.

        Returns:
            Updated BharatObservation with reward and flags.
        """
        # FIX: model_dump() not dict() for Pydantic v2
        action_dict = action.model_dump()
        verifier_state = self._verifier_state_dict()

        # Run verifiers (quality signals)
        vresult = run_all_verifiers(action_dict, verifier_state)
        self._last_verifier_flags = vresult.flags
        self._last_verifier_scores = vresult.scores

        if vresult.blocked:
            # Hard safety block — penalise strongly and continue
            reward = vresult.penalty
            self._cumulative_reward += reward
            self._step_count += 1
            return self._observe(
                reward=reward,
                terminated=False,
                truncated=self._step_count >= MAX_STEPS,
            )

        # Simulate human reaction
        reaction = self._simulate_human(action)
        self._update_state(reaction)

        # Combine env_reward (human signals) + verifier_reward (quality)
        # These are non-overlapping by design — no double penalty.
        env_reward = self._env_reward(action, reaction)
        verifier_reward = vresult.total
        reward = env_reward + verifier_reward

        self._cumulative_reward += reward
        self._step_count += 1

        terminated = (
            self._phase_idx >= len(PHASES) - 1 or self._dropout_risk >= 1.0
        )
        truncated = self._step_count >= MAX_STEPS

        return self._observe(reward=reward, terminated=terminated, truncated=truncated)

    @property
    def state(self) -> State:
        """Return the current episode state (episode_id + step_count)."""
        return State(
            episode_id=self._episode_id,
            step_count=self._step_count,
        )

    # ── Private helpers ────────────────────────────────────────────────────

    def _verifier_state_dict(self) -> dict:
        """Minimal state dict for verifiers — avoids circular imports."""
        f = self._f or FOUNDERS[0]
        return {
            "phase": PHASES[min(self._phase_idx, len(PHASES) - 1)],
            "founder": {
                "digital_literacy": f["digital_literacy"],
                "capital_inr": f["capital_inr"],
                "language": f["language"],
            },
            "engagement": {
                "dropout_risk": self._dropout_risk,
                "tasks_completed": self._tasks_completed,
            },
        }

    def _observe(
        self, reward: float = 0.0, terminated: bool = False, truncated: bool = False
    ) -> BharatObservation:
        """Build the full observation from current internal state."""
        f = self._f or FOUNDERS[0]
        phase = PHASES[min(self._phase_idx, len(PHASES) - 1)]
        res = RESOURCES.get(f["domain"], RESOURCES["edtech"])
        relation = f.get("founder_user_relationship", "familiar")
        threshold = f.get(
            "validation_threshold", VALIDATION_THRESHOLDS.get(relation, 4)
        )
        return BharatObservation(
            phase=phase,
            phase_number=self._phase_idx,
            phase_goal=PHASE_GOALS.get(phase, ""),
            founder_name=f["name"],
            founder_location=f["location"],
            founder_tier=f["tier"],
            founder_language=f["language"],
            founder_domain=f["domain"],
            founder_digital_literacy=f["digital_literacy"],
            founder_capital_inr=f["capital_inr"],
            founder_prior_attempt=f["prior_attempt"],
            founder_emotional_state=f["emotional_state"],
            founder_user_relationship=relation,
            validation_threshold=threshold,
            idea_description=IDEAS.get(f["domain"], "I have an idea"),
            validation_interviews_done=self._interviews,
            mvp_shipped=self._mvp_shipped,
            first_customer=self._first_customer,
            dropout_risk=self._dropout_risk,
            tasks_completed=self._tasks_completed,
            tasks_ignored=self._tasks_ignored,
            felt_unblocked=self._felt_unblocked,
            felt_judged=self._felt_judged,
            available_schemes=res["schemes"],
            available_tools=res["tools"],
            available_communities=res["communities"],
            step=self._step_count,
            done=terminated or truncated,
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            verifier_flags=self._last_verifier_flags,
            verifier_scores=self._last_verifier_scores,
        )

    def _simulate_human(self, action: BharatAction) -> dict:
        """
        Stochastically simulate how the founder reacts to the AI's response.

        Probability of taking action is influenced by:
            - Digital literacy (higher → easier to follow suggestions)
            - Emotional state (discouraged founders are harder to engage)
            - Jargon usage (jargon reduces compliance for low-literacy founders)
            - AI autonomy violations (being told what to do causes resistance)
        """
        f = self._f
        base = f["digital_literacy"] * 0.4 + 0.35
        if f["emotional_state"] == "discouraged":
            base -= 0.2
        if f["emotional_state"] == "excited":
            base += 0.1
        if action.used_jargon and f["digital_literacy"] < 0.5:
            base -= 0.25
        if action.made_decision_for_human:
            base -= 0.20
        base = max(0.1, min(0.95, base))

        did_task = random.random() < base
        returned = random.random() < base + 0.1
        felt_judged = action.made_decision_for_human or (
            action.used_jargon and f["digital_literacy"] < 0.4
        )
        felt_unblocked = did_task and not felt_judged
        gave_positive = did_task and random.random() < 0.6
        gave_negative = felt_judged or (not did_task and random.random() < 0.3)

        # FIX: use per-founder validation threshold (not hardcoded 5)
        relation = f.get("founder_user_relationship", "familiar")
        threshold = f.get(
            "validation_threshold", VALIDATION_THRESHOLDS.get(relation, 4)
        )

        progressed = False
        p = self._phase_idx
        if p == 0 and did_task:
            progressed = random.random() < 0.35
        elif p == 1:
            if did_task:
                self._interviews += random.randint(1, 2)
            progressed = self._interviews >= threshold  # FIX: was hardcoded >= 5
        elif p == 2 and did_task:
            progressed = random.random() < 0.4
        elif p == 3 and did_task:
            progressed = random.random() < 0.45
        elif p == 4 and did_task:
            progressed = random.random() < 0.3
        elif p == 5 and did_task:
            self._first_customer = random.random() < 0.4
            progressed = self._first_customer
        elif p == 6 and did_task:
            progressed = True

        return dict(
            did_task=did_task,
            returned=returned,
            felt_judged=felt_judged,
            felt_unblocked=felt_unblocked,
            gave_positive=gave_positive,
            gave_negative=gave_negative,
            phase_progressed=progressed,
            dropout_signal=not returned and gave_negative,
        )

    def _update_state(self, r: dict):
        """Apply the simulated human reaction to internal state."""
        if r["did_task"]:
            self._tasks_completed += 1
        else:
            self._tasks_ignored += 1
        self._felt_judged = r["felt_judged"]
        self._felt_unblocked = r["felt_unblocked"]

        # Drift dropout risk
        delta = 0.10 if not r["did_task"] else -0.05
        delta += 0.15 if r["felt_judged"] else 0.0
        delta += 0.10 if r["dropout_signal"] else 0.0
        self._dropout_risk = max(0.0, min(1.0, self._dropout_risk + delta))

        if r["phase_progressed"] and self._phase_idx < len(PHASES) - 1:
            self._phase_idx += 1
            # Emotional state evolves with each phase transition
            self._f = dict(
                self._f,
                emotional_state=random.choice(["excited", "determined", "uncertain"]),
            )

    def _env_reward(self, action: BharatAction, r: dict) -> float:
        """
        Environment reward — human engagement signals only.

        Quality checks (jargon, autonomy, accessibility) are handled
        exclusively by verifiers to avoid double penalties.
        """
        reward = 0.0

        # Positive engagement signals
        if r["did_task"]:
            reward += 10.0
        if r["returned"]:
            reward += 8.0
        if r["felt_unblocked"]:
            reward += 6.0
        if r["gave_positive"]:
            reward += 5.0
        if r["phase_progressed"]:
            reward += 20.0
        if action.resource_recommended:
            reward += 8.0

        # Milestone bonuses
        f = self._f
        threshold = f.get(
            "validation_threshold",
            VALIDATION_THRESHOLDS.get(f.get("founder_user_relationship", "familiar"), 4),
        )
        if self._interviews >= threshold:
            reward += 15.0
        if self._first_customer:
            reward += 30.0
        if self._phase_idx >= len(PHASES) - 1:
            reward += 50.0

        # Human-signal penalties (quality penalties are in verifiers)
        if r["felt_judged"]:
            reward -= 15.0
        if r["gave_negative"]:
            reward -= 8.0
        if r["dropout_signal"]:
            reward -= 25.0
        if self._dropout_risk > 0.8:
            reward -= 20.0

        return reward
