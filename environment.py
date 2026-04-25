import random
from typing import Optional
from models import Phase, FounderProfile, StartupIdea, EngagementSignals, ResourceContext, EnvState

FOUNDERS = [
    FounderProfile("Priya",  "Jhansi, UP",      "tier3", "hinglish", "handicrafts", 0.3, 5000,   False, "excited"),
    FounderProfile("Ravi",   "Nashik, MH",       "tier2", "hinglish", "agritech",    0.5, 25000,  True,  "uncertain"),
    FounderProfile("Meera",  "Coimbatore, TN",   "tier2", "english",  "edtech",      0.7, 15000,  False, "determined"),
    FounderProfile("Suresh", "Raipur, CG",       "tier3", "hindi",    "healthtech",  0.2, 8000,   True,  "discouraged"),
    FounderProfile("Anjali", "Pune, MH",         "metro", "english",  "edtech",      0.9, 100000, False, "excited"),
]

IDEAS = {
    "handicrafts": "I want to help women in my village sell their handmade things online",
    "agritech":    "Farmers near me do not know the right price to sell crops",
    "edtech":      "There are no good tutors for competitive exams in small towns",
    "healthtech":  "Old people in my area cannot use health apps",
}

RESOURCES = {
    "handicrafts": {
        "schemes":     ["MUDRA Shishu Loan up to 50k free to apply", "WEP Women Entrepreneurship Platform free", "TRIFED Tribal Co-op"],
        "tools":       ["Meesho seller zero investment", "WhatsApp Catalog free", "Instagram Shop free"],
        "communities": ["DIC District Industries Centre", "Craftsvilla Seller Network"],
    },
    "agritech": {
        "schemes":     ["PM Kisan", "NABARD Rural Business Incubator free", "RKVY-RAFTAAR"],
        "tools":       ["WhatsApp Business free", "Google Forms free", "Canva free tier"],
        "communities": ["AgriStartup India", "ICAR Krishi Vigyan Kendra"],
    },
    "edtech": {
        "schemes":     ["Startup India Registration free", "NSDC Skill India grant", "AIM NITI Aayog"],
        "tools":       ["Google Classroom free", "YouTube free", "Zoom Basic free"],
        "communities": ["EdTech India Slack", "Teacher Innovator Network"],
    },
    "healthtech": {
        "schemes":     ["Ayushman Bharat Digital Mission free", "BIRAC BIG grant", "DST NIDHI"],
        "tools":       ["WhatsApp free", "Google Sheets free", "Practo free listing"],
        "communities": ["HealthTech India", "Apollo Healthco Ecosystem"],
    },
}

PHASE_GOALS = {
    Phase.IDEA_ARTICULATION: "Help founder turn a vague idea into a clear problem statement.",
    Phase.VALIDATION:        "Guide founder to talk to at least 5 real people.",
    Phase.MVP_SCOPING:       "Help founder identify the smallest possible test.",
    Phase.RESOURCE_MAPPING:  "Match founder to 3 accessible real resources.",
    Phase.BUILD_COMPANION:   "Unblock daily progress without deciding for them.",
    Phase.FIRST_CUSTOMER:    "Coach founder through first outreach.",
    Phase.SIGNAL_READING:    "Help founder make their own pivot or persist call.",
    Phase.DONE:              "Episode complete.",
}

class BharatBuildsEnv:
    MAX_STEPS = 50

    def __init__(self, founder=None):
        self._founder = founder
        self._state = None

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
        founder = self._founder or random.choice(FOUNDERS)
        res = RESOURCES.get(founder.domain, RESOURCES["edtech"])
        self._state = EnvState(
            phase=Phase.IDEA_ARTICULATION,
            founder=founder,
            idea=StartupIdea(raw_description=IDEAS.get(founder.domain, "I have an idea")),
            engagement=EngagementSignals(),
            resources=ResourceContext(available_schemes=res["schemes"], recommended_tools=res["tools"], nearby_communities=res["communities"]),
        )
        return self._observe()

    def step(self, action):
        assert self._state is not None
        s = self._state
        reaction = self._simulate_human(action)
        self._update_state(reaction)
        reward = self._reward(action, reaction)
        s.cumulative_reward += reward
        s.step_count += 1
        terminated = s.phase == Phase.DONE or s.engagement.dropout_risk >= 1.0
        truncated  = s.step_count >= self.MAX_STEPS
        s.done = terminated or truncated
        return self._observe(), reward, terminated, truncated, {
            "reaction": reaction, "phase": s.phase.name,
            "step": s.step_count, "cumulative_reward": s.cumulative_reward,
        }

    def state(self):
        assert self._state is not None
        s = self._state
        return {
            "phase": s.phase.name,
            "phase_number": int(s.phase),
            "founder": {
                "name": s.founder.name, "location": s.founder.location,
                "tier": s.founder.tier, "language": s.founder.language,
                "domain": s.founder.domain, "digital_literacy": s.founder.digital_literacy,
                "capital_inr": s.founder.capital_inr, "prior_attempt": s.founder.prior_attempt,
                "emotional_state": s.founder.emotional_state,
            },
            "idea": {
                "description": s.idea.raw_description,
                "problem_statement": s.idea.problem_statement,
                "validation_interviews_done": s.idea.validation_interviews_done,
                "mvp_shipped": s.idea.mvp_shipped,
                "first_customer": s.idea.first_customer,
            },
            "engagement": {
                "dropout_risk": s.engagement.dropout_risk,
                "tasks_completed": s.engagement.tasks_completed,
                "tasks_ignored": s.engagement.tasks_ignored,
                "felt_unblocked": s.engagement.felt_unblocked,
                "felt_judged": s.engagement.felt_judged,
            },
            "resources": {
                "schemes": s.resources.available_schemes,
                "tools": s.resources.recommended_tools,
                "communities": s.resources.nearby_communities,
            },
            "step": s.step_count, "done": s.done,
            "phase_goal": PHASE_GOALS.get(s.phase, ""),
        }

    def _observe(self):
        return self.state()

    def _simulate_human(self, action):
        s = self._state
        f = s.founder
        base = f.digital_literacy * 0.4 + 0.35
        if f.emotional_state == "discouraged": base -= 0.2
        if f.emotional_state == "excited":     base += 0.1
        if action.get("used_jargon") and f.digital_literacy < 0.5:    base -= 0.25
        if action.get("made_decision_for_human"):                       base -= 0.20
        base = max(0.1, min(0.95, base))
        did_task      = random.random() < base
        returned      = random.random() < base + 0.1
        felt_judged   = action.get("made_decision_for_human", False) or                         (action.get("used_jargon", False) and f.digital_literacy < 0.4)
        felt_unblocked = did_task and not felt_judged
        gave_positive  = did_task and random.random() < 0.6
        gave_negative  = felt_judged or (not did_task and random.random() < 0.3)
        progressed = False
        p = s.phase
        if p == Phase.IDEA_ARTICULATION and did_task:
            progressed = random.random() < 0.35
        elif p == Phase.VALIDATION:
            if did_task: s.idea.validation_interviews_done += random.randint(1, 2)
            progressed = s.idea.validation_interviews_done >= 5
        elif p == Phase.MVP_SCOPING and did_task:
            progressed = random.random() < 0.4
        elif p == Phase.RESOURCE_MAPPING and did_task:
            progressed = random.random() < 0.45
        elif p == Phase.BUILD_COMPANION and did_task:
            progressed = random.random() < 0.3
        elif p == Phase.FIRST_CUSTOMER and did_task:
            s.idea.first_customer = random.random() < 0.4
            progressed = s.idea.first_customer
        elif p == Phase.SIGNAL_READING and did_task:
            progressed = True
        return {
            "did_task": did_task, "returned": returned,
            "felt_judged": felt_judged, "felt_unblocked": felt_unblocked,
            "gave_positive": gave_positive, "gave_negative": gave_negative,
            "phase_progressed": progressed,
            "dropout_signal": not returned and gave_negative,
        }

    def _update_state(self, reaction):
        s = self._state
        e = s.engagement
        if reaction["did_task"]: e.tasks_completed += 1
        else:                    e.tasks_ignored   += 1
        if reaction["gave_positive"]: e.positive_feedback += 1
        if reaction["gave_negative"]: e.negative_feedback += 1
        e.felt_judged    = reaction["felt_judged"]
        e.felt_unblocked = reaction["felt_unblocked"]
        e.total_sessions += 1
        delta  =  0.10 if not reaction["did_task"]  else -0.05
        delta +=  0.15 if reaction["felt_judged"]   else 0.0
        delta +=  0.10 if reaction["dropout_signal"] else 0.0
        e.dropout_risk = max(0.0, min(1.0, e.dropout_risk + delta))
        if reaction["phase_progressed"] and s.phase < Phase.DONE:
            s.phase = Phase(int(s.phase) + 1)
            s.founder.emotional_state = random.choice(["excited", "determined", "uncertain"])

    def _reward(self, action, reaction):
        s = self._state
        r = 0.0
        if reaction["did_task"]:        r += 10.0
        if reaction["returned"]:        r +=  8.0
        if reaction["felt_unblocked"]:  r +=  6.0
        if reaction["gave_positive"]:   r +=  5.0
        if reaction["phase_progressed"]: r += 20.0
        if action.get("resource_recommended"): r += 8.0
        if s.idea.validation_interviews_done >= 5: r += 15.0
        if s.idea.first_customer:               r += 30.0
        if s.phase == Phase.DONE:               r += 50.0
        if action.get("used_jargon") and s.founder.digital_literacy < 0.5: r -= 10.0
        if action.get("made_decision_for_human"): r -= 20.0
        if reaction["felt_judged"]:    r -= 15.0
        if reaction["gave_negative"]:  r -=  8.0
        if reaction["dropout_signal"]: r -= 25.0
        if s.engagement.dropout_risk > 0.8: r -= 20.0
        return r