import httpx

class BharatBuildsClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base = base_url.rstrip("/")
        self.session_id = None

    def reset(self, founder_name=None, seed=None):
        r = httpx.post(f"{self.base}/reset", json={"founder_name": founder_name, "seed": seed})
        r.raise_for_status()
        data = r.json()
        self.session_id = data["session_id"]
        return data["observation"]

    def step(self, action, session_id=None):
        sid = session_id or self.session_id
        r = httpx.post(f"{self.base}/step", json={"session_id": sid, "action": action})
        r.raise_for_status()
        d = r.json()
        return d["observation"], d["reward"], d["terminated"], d["truncated"], d["info"]

    def state(self, session_id=None):
        sid = session_id or self.session_id
        r = httpx.post(f"{self.base}/state", json={"session_id": sid})
        r.raise_for_status()
        return r.json()["state"]