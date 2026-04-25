import random
from typing import Optional, Any
from pydantic import BaseModel
from openenv.core import Environment, Observation, Action, State

# ── Pydantic Models ──────────────────────────────────────────

class BharatAction(Action):
    ai_response: str = ""
    suggested_task: str = ""
    task_rationale: str = ""
    used_jargon: bool = False
    made_decision_for_human: bool = False
    resource_recommended: str = ""
    emotional_tone: str = "encouraging"

class BharatObservation(Observation):
    phase: str = "IDEA_ARTICULATION"
    phase_number: int = 0
    phase_goal: str = ""
    founder_name: str = ""
    founder_location: str = ""
    founder_tier: str = ""
    founder_language: str = ""
    founder_domain: str = ""
    founder_digital_literacy: float = 0.5
    founder_capital_inr: float = 10000.0
    founder_prior_attempt: bool = False
    founder_emotional_state: str = "excited"
    idea_description: str = ""
    validation_interviews_done: int = 0
    mvp_shipped: bool = False
    first_customer: bool = False
    dropout_risk: float = 0.0
    tasks_completed: int = 0
    tasks_ignored: int = 0
    felt_unblocked: bool = False
    felt_judged: bool = False
    available_schemes: list = []
    available_tools: list = []
    available_communities: list = []
    step: int = 0
    done: bool = False
    reward: float = 0.0
    terminated: bool = False
    truncated: bool = False

class BharatState(State):
    phase: str = "IDEA_ARTICULATION"
    step_count: int = 0
    cumulative_reward: float = 0.0
    done: bool = False

# ── Founder Data ─────────────────────────────────────────────

FOUNDERS = [
    dict(name="Priya",  location="Jhansi, UP",      tier="tier3", language="hinglish", domain="handicrafts", digital_literacy=0.3, capital_inr=5000,   prior_attempt=False, emotional_state="excited"),
    dict(name="Ravi",   location="Nashik, MH",       tier="tier2", language="hinglish", domain="agritech",    digital_literacy=0.5, capital_inr=25000,  prior_attempt=True,  emotional_state="uncertain"),
    dict(name="Meera",  location="Coimbatore, TN",   tier="tier2", language="english",  domain="edtech",      digital_literacy=0.7, capital_inr=15000,  prior_attempt=False, emotional_state="determined"),
    dict(name="Suresh", location="Raipur, CG",       tier="tier3", language="hindi",    domain="healthtech",  digital_literacy=0.2, capital_inr=8000,   prior_attempt=True,  emotional_state="discouraged"),
    dict(name="Anjali", location="Pune, MH",         tier="metro", language="english",  domain="edtech",      digital_literacy=0.9, capital_inr=100000, prior_attempt=False, emotional_state="excited"),
]

IDEAS = {
    "handicrafts": "I want to help women in my village sell their handmade things online",
    "agritech":    "Farmers near me do not know the right price to sell crops",
    "edtech":      "There are no good tutors for competitive exams in small towns",
    "healthtech":  "Old people in my area cannot use health apps",
}

RESOURCES = {
    "handicrafts": dict(schemes=["MUDRA Shishu Loan up to 50k free","WEP Women Entrepreneurship Platform free","TRIFED Tribal Co-op"], tools=["Meesho seller zero investment","WhatsApp Catalog free","Instagram Shop free"], communities=["DIC District Industries Centre","Craftsvilla Seller Network"]),
    "agritech":    dict(schemes=["PM Kisan","NABARD Rural Business Incubator free","RKVY-RAFTAAR"], tools=["WhatsApp Business free","Google Forms free","Canva free tier"], communities=["AgriStartup India","ICAR Krishi Vigyan Kendra"]),
    "edtech":      dict(schemes=["Startup India Registration free","NSDC Skill India grant","AIM NITI Aayog"], tools=["Google Classroom free","YouTube free","Zoom Basic free"], communities=["EdTech India Slack","Teacher Innovator Network"]),
    "healthtech":  dict(schemes=["Ayushman Bharat Digital Mission free","BIRAC BIG grant","DST NIDHI"], tools=["WhatsApp free","Google Sheets free","Practo free listing"], communities=["HealthTech India","Apollo Healthco Ecosystem"]),
}

PHASES = ["IDEA_ARTICULATION","VALIDATION","MVP_SCOPING","RESOURCE_MAPPING","BUILD_COMPANION","FIRST_CUSTOMER","SIGNAL_READING","DONE"]

PHASE_GOALS = {
    "IDEA_ARTICULATION": "Help founder turn a vague idea into a clear problem statement.",
    "VALIDATION":        "Guide founder to talk to at least 5 real people.",
    "MVP_SCOPING":       "Help founder identify the smallest possible test.",
    "RESOURCE_MAPPING":  "Match founder to 3 accessible real resources.",
    "BUILD_COMPANION":   "Unblock daily progress without deciding for them.",
    "FIRST_CUSTOMER":    "Coach founder through first outreach.",
    "SIGNAL_READING":    "Help founder make their own pivot or persist call.",
    "DONE":              "Episode complete.",
}

MAX_STEPS = 50

# ── Environment ──────────────────────────────────────────────

class BharatBuildsEnv(Environment[BharatAction, BharatObservation, BharatState]):
    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self, founder_name: str = None, **kwargs):
        super().__init__(**kwargs)
        self._founder_name = founder_name
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

    def reset(self, seed=None, episode_id=None, founder_name=None, **kwargs) -> BharatObservation:
        if seed is not None:
            random.seed(seed)
        name = founder_name or self._founder_name
        if name:
            matches = [f for f in FOUNDERS if f["name"] == name]
            self._f = matches[0] if matches else random.choice(FOUNDERS)
        else:
            self._f = random.choice(FOUNDERS)
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
        return self._observe(reward=0.0, terminated=False, truncated=False)

    def step(self, action: BharatAction, timeout_s=None, **kwargs) -> BharatObservation:
        reaction = self._simulate_human(action)
        self._update_state(reaction)
        reward = self._reward(action, reaction)
        self._cumulative_reward += reward
        self._step_count += 1
        terminated = self._phase_idx >= len(PHASES)-1 or self._dropout_risk >= 1.0
        truncated  = self._step_count >= MAX_STEPS
        return self._observe(reward=reward, terminated=terminated, truncated=truncated)

    @property
    def state(self) -> BharatState:
        return BharatState(
            phase=PHASES[min(self._phase_idx, len(PHASES)-1)],
            step_count=self._step_count,
            cumulative_reward=self._cumulative_reward,
            done=self._phase_idx >= len(PHASES)-1 or self._dropout_risk >= 1.0,
        )

    # ── Private ──────────────────────────────────────────────

    def _observe(self, reward=0.0, terminated=False, truncated=False) -> BharatObservation:
        f = self._f or FOUNDERS[0]
        phase = PHASES[min(self._phase_idx, len(PHASES)-1)]
        res = RESOURCES.get(f["domain"], RESOURCES["edtech"])
        return BharatObservation(
            phase=phase, phase_number=self._phase_idx,
            phase_goal=PHASE_GOALS.get(phase,""),
            founder_name=f["name"], founder_location=f["location"],
            founder_tier=f["tier"], founder_language=f["language"],
            founder_domain=f["domain"], founder_digital_literacy=f["digital_literacy"],
            founder_capital_inr=f["capital_inr"], founder_prior_attempt=f["prior_attempt"],
            founder_emotional_state=f["emotional_state"],
            idea_description=IDEAS.get(f["domain"],"I have an idea"),
            validation_interviews_done=self._interviews,
            mvp_shipped=self._mvp_shipped, first_customer=self._first_customer,
            dropout_risk=self._dropout_risk,
            tasks_completed=self._tasks_completed, tasks_ignored=self._tasks_ignored,
            felt_unblocked=self._felt_unblocked, felt_judged=self._felt_judged,
            available_schemes=res["schemes"], available_tools=res["tools"],
            available_communities=res["communities"],
            step=self._step_count, done=terminated or truncated,
            reward=reward, terminated=terminated, truncated=truncated,
        )

    def _simulate_human(self, action: BharatAction) -> dict:
        f = self._f
        base = f["digital_literacy"] * 0.4 + 0.35
        if f["emotional_state"] == "discouraged": base -= 0.2
        if f["emotional_state"] == "excited":     base += 0.1
        if action.used_jargon and f["digital_literacy"] < 0.5: base -= 0.25
        if action.made_decision_for_human:                      base -= 0.20
        base = max(0.1, min(0.95, base))
        did_task      = random.random() < base
        returned      = random.random() < base + 0.1
        felt_judged   = action.made_decision_for_human or (action.used_jargon and f["digital_literacy"] < 0.4)
        felt_unblocked = did_task and not felt_judged
        gave_positive  = did_task and random.random() < 0.6
        gave_negative  = felt_judged or (not did_task and random.random() < 0.3)
        progressed = False
        p = self._phase_idx
        if p == 0 and did_task:   progressed = random.random() < 0.35
        elif p == 1:
            if did_task: self._interviews += random.randint(1,2)
            progressed = self._interviews >= 5
        elif p == 2 and did_task: progressed = random.random() < 0.4
        elif p == 3 and did_task: progressed = random.random() < 0.45
        elif p == 4 and did_task: progressed = random.random() < 0.3
        elif p == 5 and did_task:
            self._first_customer = random.random() < 0.4
            progressed = self._first_customer
        elif p == 6 and did_task: progressed = True
        return dict(did_task=did_task, returned=returned, felt_judged=felt_judged,
                    felt_unblocked=felt_unblocked, gave_positive=gave_positive,
                    gave_negative=gave_negative, phase_progressed=progressed,
                    dropout_signal=not returned and gave_negative)

    def _update_state(self, r: dict):
        if r["did_task"]: self._tasks_completed += 1
        else:             self._tasks_ignored   += 1
        self._felt_judged    = r["felt_judged"]
        self._felt_unblocked = r["felt_unblocked"]
        delta  =  0.10 if not r["did_task"]       else -0.05
        delta +=  0.15 if r["felt_judged"]         else 0.0
        delta +=  0.10 if r["dropout_signal"]      else 0.0
        self._dropout_risk = max(0.0, min(1.0, self._dropout_risk + delta))
        if r["phase_progressed"] and self._phase_idx < len(PHASES)-1:
            self._phase_idx += 1
            self._f = dict(self._f, emotional_state=random.choice(["excited","determined","uncertain"]))

    def _reward(self, action: BharatAction, r: dict) -> float:
        reward = 0.0
        if r["did_task"]:        reward += 10.0
        if r["returned"]:        reward +=  8.0
        if r["felt_unblocked"]:  reward +=  6.0
        if r["gave_positive"]:   reward +=  5.0
        if r["phase_progressed"]: reward += 20.0
        if action.resource_recommended: reward += 8.0
        if self._interviews >= 5:    reward += 15.0
        if self._first_customer:     reward += 30.0
        if self._phase_idx >= len(PHASES)-1: reward += 50.0
        if action.used_jargon and self._f["digital_literacy"] < 0.5: reward -= 10.0
        if action.made_decision_for_human: reward -= 20.0
        if r["felt_judged"]:     reward -= 15.0
        if r["gave_negative"]:   reward -=  8.0
        if r["dropout_signal"]:  reward -= 25.0
        if self._dropout_risk > 0.8: reward -= 20.0
        return reward