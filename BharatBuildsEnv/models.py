"""
Data models for the BharatBuilds Environment.

BharatBuilds trains an LLM to be an empathetic startup co-founder for
first-time Indian entrepreneurs from Tier 2/3 cities. The AI is rewarded
for helping the human take real steps — not for deciding for them.
"""

from typing import Dict, List, Optional
from pydantic import Field
from openenv.core.env_server.types import Action, Observation


class BharatAction(Action):
    """
    Action submitted by the AI co-founder agent each turn.

    The agent must craft a response that unblocks the founder without
    deciding for them, using accessible language and recommending
    only resources they can actually afford.
    """

    ai_response: str = Field(
        default="",
        description="Main conversational response from the AI co-founder",
    )
    suggested_task: str = Field(
        default="",
        description="One concrete, small action the founder can take next",
    )
    task_rationale: str = Field(
        default="",
        description="Brief explanation of why this task matters at this phase",
    )
    used_jargon: bool = Field(
        default=False,
        description="True if response contains unexplained technical/startup jargon",
    )
    made_decision_for_human: bool = Field(
        default=False,
        description="True if the AI decided something that the founder should decide",
    )
    resource_recommended: str = Field(
        default="",
        description="Name of a specific resource or scheme mentioned (empty if none)",
    )
    emotional_tone: str = Field(
        default="encouraging",
        description="Emotional register of the response: encouraging/neutral/concerned",
    )


class BharatObservation(Observation):
    """
    Observation returned after each step — the full state of the founder's journey.

    The AI agent uses this to decide how to respond next. Key signals are:
    - phase / phase_goal: what stage the founder is at
    - founder_* fields: who the founder is (literacy, capital, emotional state)
    - dropout_risk: urgency signal — high dropout demands immediate action
    - verifier_flags / verifier_scores: feedback on the last action's quality
    """

    # ── Phase ─────────────────────────────────────────────────────
    phase: str = Field(default="IDEA_ARTICULATION", description="Current startup phase")
    phase_number: int = Field(default=0, description="Phase index (0–7)")
    phase_goal: str = Field(default="", description="What the AI should help with now")

    # ── Founder profile ───────────────────────────────────────────
    founder_name: str = Field(default="", description="Founder's name")
    founder_location: str = Field(default="", description="City, State")
    founder_tier: str = Field(default="tier2", description="tier3/rural | tier2 | metro")
    founder_language: str = Field(default="hindi", description="Primary language")
    founder_domain: str = Field(default="edtech", description="Startup domain")
    founder_digital_literacy: float = Field(
        default=0.5, description="0.0 (none) to 1.0 (expert)"
    )
    founder_capital_inr: float = Field(default=10000.0, description="Available capital in INR")
    founder_prior_attempt: bool = Field(
        default=False, description="Has attempted a startup before"
    )
    founder_emotional_state: str = Field(
        default="excited", description="excited | uncertain | discouraged | determined"
    )
    founder_user_relationship: str = Field(
        default="familiar",
        description="self | close | familiar | outsider — proximity to the problem",
    )
    validation_threshold: int = Field(
        default=4,
        description="Number of validation conversations required before advancing",
    )

    # ── Idea & progress ───────────────────────────────────────────
    idea_description: str = Field(default="", description="Raw idea description")
    validation_interviews_done: int = Field(
        default=0, description="Number of validation conversations completed"
    )
    mvp_shipped: bool = Field(default=False, description="MVP has been launched")
    first_customer: bool = Field(default=False, description="First customer acquired")

    # ── Engagement signals ────────────────────────────────────────
    dropout_risk: float = Field(
        default=0.0, description="0.0 (engaged) to 1.0 (about to quit)"
    )
    tasks_completed: int = Field(default=0, description="Total tasks founder completed")
    tasks_ignored: int = Field(default=0, description="Total tasks founder skipped")
    felt_unblocked: bool = Field(default=False, description="Felt unblocked this step")
    felt_judged: bool = Field(default=False, description="Felt judged or talked down to")

    # ── Resources ─────────────────────────────────────────────────
    available_schemes: List[str] = Field(
        default_factory=list, description="Government/NGO schemes available"
    )
    available_tools: List[str] = Field(
        default_factory=list, description="Free tools suited to this founder"
    )
    available_communities: List[str] = Field(
        default_factory=list, description="Local communities or networks"
    )

    # ── Episode metadata ──────────────────────────────────────────
    step: int = Field(default=0, description="Current step number")
    done: bool = Field(default=False, description="Episode is over")
    reward: float = Field(default=0.0, description="Reward from last step")
    terminated: bool = Field(
        default=False, description="Episode ended naturally (journey complete / dropout)"
    )
    truncated: bool = Field(
        default=False, description="Episode ended by step limit"
    )

    # ── Verifier feedback ─────────────────────────────────────────
    verifier_flags: List[str] = Field(
        default_factory=list,
        description="Human-readable quality flags from the 6 verifiers",
    )
    verifier_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-verifier numeric scores",
    )
