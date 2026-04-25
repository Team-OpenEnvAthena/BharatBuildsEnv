import uuid, time
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from environment import BharatBuildsEnv, FOUNDERS
from verifiers import run_all_verifiers

app = FastAPI(title="BharatBuilds", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SESSIONS = {}
MAX_SESSIONS, SESSION_TTL, MAX_STEPS = 100, 3600, 50

class ResetRequest(BaseModel):
    founder_name: Optional[str] = None
    seed: Optional[int] = None

class StepRequest(BaseModel):
    session_id: str
    action: dict

class StateRequest(BaseModel):
    session_id: str

@app.get("/")
def root():
    return {"environment": "BharatBuilds", "version": "1.0.0", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok", "active_sessions": len(SESSIONS)}

@app.post("/reset")
def reset(req: ResetRequest):
    _cleanup()
    if len(SESSIONS) >= MAX_SESSIONS:
        raise HTTPException(503, "Max sessions reached")
    founder = None
    if req.founder_name:
        matches = [f for f in FOUNDERS if f.name == req.founder_name]
        if matches: founder = matches[0]
    env = BharatBuildsEnv(founder=founder)
    obs = env.reset(seed=req.seed)
    sid = str(uuid.uuid4())
    SESSIONS[sid] = {"env": env, "created": time.time(), "last": time.time(), "steps": 0}
    return {"session_id": sid, "observation": obs}

@app.post("/step")
def step(req: StepRequest):
    session = _get(req.session_id)
    if session["steps"] >= MAX_STEPS:
        raise HTTPException(400, "Max steps reached. Call /reset.")
    action = _sanitize(req.action)
    env = session["env"]
    vr = run_all_verifiers(action, env.state())
    if vr.blocked:
        return {"observation": env.state(), "reward": vr.penalty,
                "terminated": False, "truncated": False,
                "info": {"blocked": True, "reason": vr.reason, "flags": vr.flags}}
    obs, reward, terminated, truncated, info = env.step(action)
    session["steps"] += 1
    session["last"] = time.time()
    info["verifier_scores"] = vr.scores
    info["verifier_flags"]  = vr.flags
    return {"observation": obs, "reward": reward,
            "terminated": terminated, "truncated": truncated, "info": info}

@app.post("/state")
def state(req: StateRequest):
    session = _get(req.session_id)
    return {"state": session["env"].state(), "steps": session["steps"]}

def _get(sid):
    if sid not in SESSIONS: raise HTTPException(404, "Session not found. Call /reset first.")
    s = SESSIONS[sid]
    if time.time() - s["last"] > SESSION_TTL:
        del SESSIONS[sid]; raise HTTPException(410, "Session expired.")
    return s

def _cleanup():
    now = time.time()
    for sid in [k for k,v in SESSIONS.items() if now - v["last"] > SESSION_TTL]:
        del SESSIONS[sid]

def _sanitize(action):
    return {
        "ai_response":             str(action.get("ai_response",""))[:2000],
        "suggested_task":          str(action.get("suggested_task",""))[:500],
        "task_rationale":          str(action.get("task_rationale",""))[:500],
        "used_jargon":             bool(action.get("used_jargon", False)),
        "made_decision_for_human": bool(action.get("made_decision_for_human", False)),
        "resource_recommended":    str(action.get("resource_recommended",""))[:200],
        "emotional_tone":          str(action.get("emotional_tone","encouraging"))[:50],
    }