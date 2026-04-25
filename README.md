---
title: BharatBuildsEnv
emoji: 🇮🇳
colorFrom: orange
colorTo: green
sdk: docker
pinned: true
license: mit
app_port: 8000
base_path: /web
tags:
  - openenv
---

# 🇮🇳 BharatBuilds RL Environment

> *"McKinsey charges ₹5 crore to give a large company its strategy.  
> We're training an AI to be that thinking partner for someone with ₹500 in their pocket and an idea that could change their community."*

---

## The Problem

India has 1.4 billion people. A tiny fraction have access to the tacit knowledge that lives inside IIT incubators, Mumbai VC firms, and Bangalore accelerators — the kind of thinking partnership that turns a fuzzy idea into a real business.

The woman in Tier-3 Rajasthan who knows exactly what her community needs but has no idea what an MVP is. The farmer in Nashik who spotted a real problem in crop pricing. The student in Raipur who can't afford a mentor.

**BharatBuilds trains an LLM to be that co-founder for them.**

---

## The RL Environment

BharatBuildsEnv is an OpenEnv-compliant environment that simulates the journey of a first-time Indian founder across 7 phases:

```
Phase 0: IDEA_ARTICULATION  → Turn a vague idea into a clear problem statement
Phase 1: VALIDATION         → Talk to real people (threshold varies by founder relationship)
Phase 2: MVP_SCOPING        → Identify the smallest possible test
Phase 3: RESOURCE_MAPPING   → Find real, free Indian resources
Phase 4: BUILD_COMPANION    → Unblock daily progress
Phase 5: FIRST_CUSTOMER     → Coach through first outreach
Phase 6: SIGNAL_READING     → Pivot or persist — founder decides
```

The AI is the **agent**. The human founder is **simulated** — they have a probability of taking action, returning the next day, feeling judged, or dropping out, based on how well the AI responds.

### What Makes This Different

In a standard RL environment, the agent acts and the environment responds.  
Here, **the reward is whether a human took a meaningful step forward** — not whether the AI completed a task.

This inversion drives theory-of-mind reasoning:
- What does this person already know?  
- Are they overwhelmed or just unsure?  
- What one small step will they actually do?

### Relationship-Aware Validation

Validation threshold adapts to how close the founder is to their users:

| Relationship | Example | Threshold |
|---|---|---|
| `self` | Kamla the weaver building for weavers | 2 conversations |
| `close` | Priya building for her tailor mother | 3 conversations |
| `familiar` | Ravi building for nearby farmers | 4 conversations |
| `outsider` | Anjali (engineer) building for rural women | 6 conversations |

---

## Reward Design (6 Independent Verifiers + Human Signals)

Two non-overlapping reward sources prevent double penalties:

**Environment reward** (human engagement):
| Signal | Value |
|---|---|
| Human took the task | +10 |
| Human returned next session | +8 |
| Human felt unblocked | +6 |
| Phase progression | +20 |
| First customer | +30 |
| Journey complete | +50 |

**Verifier reward** (AI quality):
| Verifier | What it catches |
|---|---|
| **Safety** | Prompt injection, reward hacking (−50 if blocked) |
| **Autonomy** | AI deciding FOR the founder (−20), rewards questions (+5) |
| **Accessibility** | Unaffordable recommendations (−10), free resources (+8) |
| **Clarity** | Unexplained jargon for low-literacy founders (−10) |
| **Engagement** | Concrete action verbs (+5), right emotional tone (+3) |
| **Progress** | Phase-aligned responses (+8), misalignment (−6) |

---

## Founder Profiles (18 diverse personas)

Spanning tier3/rural, tier2, and metro with domains from handicrafts to SaaS:

| Name | Location | Tier | Domain | Literacy | Capital | Relationship |
|---|---|---|---|---|---|---|
| Priya | Jhansi, UP | tier3 | handicrafts | 0.3 | ₹5,000 | self |
| Kamla | Varanasi, UP | rural | handicrafts | 0.2 | ₹3,000 | self |
| Ravi | Nashik, MH | tier2 | agritech | 0.5 | ₹25,000 | close |
| Anjali | Pune, MH | metro | edtech | 0.9 | ₹1,00,000 | outsider |
| *...14 more* | | | | | | |

---

## Training Results

![Training Results](bharat_builds_results.png)

| Metric | Random Baseline | GRPO Trained |
|---|---|---|
| Avg Cumulative Reward | −45 to −80 | +35 to +90 |
| Jargon violations | High | Near zero |
| Made decisions for human | Frequent | Rare |
| Phase progression rate | ~5% | ~35% |

**Before training:** *"You must raise venture capital and optimize your CAC/ARR ratio."*

**After training:** *"Priya, aapka idea bahut achha hai! Kya aap kal 2 logon se — apni dost ya padosi — ye pooch sakti hain: kya unhe ye problem hoti hai? WhatsApp pe bhi kar sakti hain."*

---

## Quick Start

```python
from BharatBuildsEnv import BharatBuildsClient, BharatAction

# Connect to a running server
with BharatBuildsClient(base_url="http://localhost:8000") as client:
    result = client.reset(founder_name="Priya")
    print(result.observation.phase, result.observation.founder_name)

    action = BharatAction(
        ai_response="Priya, tell me who feels this problem most.",
        suggested_task="Talk to 2 neighbours about the problem today.",
        emotional_tone="encouraging",
    )
    result = client.step(action)
    print(result.reward, result.observation.dropout_risk)
```

### Run Locally

```bash
git clone https://huggingface.co/spaces/athena-openenv/bharatbuilds-env
cd bharatbuilds-env
uv sync
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t bharatbuilds-env:latest -f server/Dockerfile .
docker run -p 8000:8000 bharatbuilds-env:latest
```

---

## Training Script

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/athena-openenv/BharatBuildsEnv/blob/main/bharat_builds_training.ipynb)

Uses: `Qwen2.5-1.5B-Instruct` + `Unsloth` + `TRL GRPO`

Key design choices:
- **GRPO** — no value model, efficient on T4
- **4-bit quantization** via Unsloth
- **Multi-reward** combining 6 verifiers + environment simulation
- **JSON format reward** — model must output valid structured action

---

## Links

- 🤗 **HuggingFace Space:** [athena-openenv/bharatbuilds-env](https://huggingface.co/spaces/athena-openenv/bharatbuilds-env)
- 📓 **Training Notebook:** [Colab](https://colab.research.google.com/github/athena-openenv/BharatBuildsEnv/blob/main/bharat_builds_training.ipynb)
- 🤗 **Trained Model:** Coming soon
- 📝 **Blog Post:** Coming soon
- 🎥 **Demo Video:** Coming soon

---

## File Structure

```
BharatBuildsEnv/
├── __init__.py                    # Package exports (client + models)
├── models.py                      # BharatAction, BharatObservation
├── client.py                      # BharatBuildsClient (EnvClient)
├── data.py                        # (imported by server — see server/data.py)
├── generate_data.py               # Training data generator
├── openenv.yaml                   # OpenEnv manifest
├── pyproject.toml                 # Project metadata
├── bharat_builds_training.ipynb   # GRPO training notebook
├── sft_data.jsonl                 # Generated SFT training data
├── grpo_prompts.jsonl             # Generated GRPO prompts
└── server/
    ├── __init__.py                # Server exports
    ├── BharatBuildsEnv_environment.py  # Core RL environment
    ├── app.py                     # FastAPI app
    ├── verifiers.py               # 6 independent reward verifiers
    ├── data.py                    # Static founder profiles + training data
    ├── Dockerfile                 # Multi-stage container build
    └── requirements.txt           # Server dependencies
```

---

## Hackathon Theme

**Theme #5 — Wild Card** (also touching #3.2 Personalized Tasks, #2 Long-Horizon Planning)

> *20 years from now, no one should feel they can't build something just because they don't have the resources.*

*Built for the Meta PyTorch OpenEnv Hackathon, India 2026*  
*Team: Isha Khatana, Garima Mahato (Team Athena)*
