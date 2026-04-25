"""
BharatBuilds Client
Compatible with create_fastapi_app from openenv.core.
reward, terminated, truncated are embedded inside the observation dict.
"""
import httpx

class BharatBuildsClient:
    def __init__(self, base_url="http://localhost:7860"):
        self.base = base_url.rstrip("/")
        self.session_id = None

    def reset(self, founder_name=None, seed=None) -> dict:
        r = httpx.post(f"{self.base}/reset",
                       json={"founder_name": founder_name, "seed": seed},
                       timeout=30)
        r.raise_for_status()
        data = r.json()
        self.session_id = data.get("session_id")
        return data.get("observation", data)

    def step(self, action: dict, session_id: str = None) -> tuple:
        """
        Returns: (observation, reward, terminated, truncated, info)
        reward/terminated/truncated extracted from observation since
        create_fastapi_app embeds them there.
        """
        sid = session_id or self.session_id
        r = httpx.post(f"{self.base}/step",
                       json={"session_id": sid, "action": action},
                       timeout=30)
        r.raise_for_status()
        d = r.json()
        obs = d.get("observation", d)
        # Extract from observation (embedded by OpenEnv)
        reward     = obs.get("reward", 0.0)
        terminated = obs.get("terminated", False)
        truncated  = obs.get("truncated", False)
        info = {
            "verifier_flags":  obs.get("verifier_flags", []),
            "verifier_scores": obs.get("verifier_scores", {}),
            "phase":           obs.get("phase", ""),
            "step":            obs.get("step", 0),
        }
        return obs, reward, terminated, truncated, info

    def state(self, session_id: str = None) -> dict:
        sid = session_id or self.session_id
        r = httpx.post(f"{self.base}/state",
                       json={"session_id": sid},
                       timeout=30)
        r.raise_for_status()
        return r.json().get("state", r.json())

    def health(self) -> dict:
        return httpx.get(f"{self.base}/health", timeout=10).json()
