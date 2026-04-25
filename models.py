from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

class Phase(IntEnum):
    IDEA_ARTICULATION = 0
    VALIDATION        = 1
    MVP_SCOPING       = 2
    RESOURCE_MAPPING  = 3
    BUILD_COMPANION   = 4
    FIRST_CUSTOMER    = 5
    SIGNAL_READING    = 6
    DONE              = 7

@dataclass
class FounderProfile:
    name: str
    location: str
    tier: str
    language: str
    domain: str
    digital_literacy: float
    capital_inr: float
    prior_attempt: bool
    emotional_state: str

@dataclass
class StartupIdea:
    raw_description: str
    problem_statement: Optional[str] = None
    target_user: Optional[str] = None
    validation_interviews_done: int = 0
    mvp_shipped: bool = False
    first_customer: bool = False

@dataclass
class EngagementSignals:
    total_sessions: int = 0
    tasks_completed: int = 0
    tasks_ignored: int = 0
    positive_feedback: int = 0
    negative_feedback: int = 0
    felt_judged: bool = False
    felt_unblocked: bool = False
    dropout_risk: float = 0.0

@dataclass
class ResourceContext:
    available_schemes: list = field(default_factory=list)
    recommended_tools: list = field(default_factory=list)
    nearby_communities: list = field(default_factory=list)

@dataclass
class EnvState:
    phase: Phase
    founder: FounderProfile
    idea: StartupIdea
    engagement: EngagementSignals
    resources: ResourceContext
    step_count: int = 0
    cumulative_reward: float = 0.0
    done: bool = False