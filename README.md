# BharatBuilds RL Environment

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
Phase 1: VALIDATION         → Talk to 5 real people (not skip this step)
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

---

## Reward Design (6 Independent Verifiers)

| Verifier | What it catches |
|---|---|
| **Safety** | Prompt injection, reward hacking attempts |
| **Autonomy** | Did the AI decide FOR the founder? (−20 penalty) |
| **Accessibility** | Recommending resources the founder can't afford? |
| **Clarity** | Using unexplained jargon for low-literacy founders? |
| **Engagement** | Concrete verb in the task? Right emotional tone? |
| **Progress** | Is the response aligned with the current phase? |

Plus environment rewards: task completion (+10), retention (+8), phase progression (+20), first customer (+30), journey complete (+50).

Anti-cheating: Multiple independent verifiers make it hard to optimize one signal while ignoring the rest.

---

## Founder Profiles

Five diverse Indian founder personas are built in:

| Name | Location | Tier | Domain | Literacy | Capital |
|---|---|---|---|---|---|
| Priya | Jhansi, UP | Tier 3 | Handicrafts | 0.3 | ₹5,000 |
| Ravi | Nashik, MH | Tier 2 | Agritech | 0.5 | ₹25,000 |
| Meera | Coimbatore | Tier 2 | EdTech | 0.7 | ₹15,000 |
| Suresh | Raipur, CG | Tier 3 | Healthtech | 0.2 | ₹8,000 |
| Anjali | Pune, MH | Metro | EdTech | 0.9 | ₹1,00,000 |

The human simulation adjusts dropout probability based on: digital literacy, emotional state, whether jargon was used, and whether the AI decided for them.

---

## Training Results

![Training Results](bharat_builds_results.png)

| Metric | Random Baseline | GRPO Trained |
|---|---|---|
| Avg Cumulative Reward | −45 to −80 | +35 to +90 |
| Jargon violations | High | Near zero |
| Made decisions for human | Frequent | Rare |
| Phase progression rate | ~5% | ~35% |

**Before training:** model says *"You must raise venture capital and optimize your CAC/ARR ratio."*  
**After training:** model says *"Priya, aapka idea bahut achha hai! Kya aap kal 2 logon se — apni dost ya padosi — ye pooch sakti hain: kya unhe ye problem hoti hai? WhatsApp pe bhi kar sakti hain."*

---

## Quick Start

```bash
# Run locally
git clone https://huggingface.co/spaces/YOUR_USERNAME/BharatBuildsEnv
cd BharatBuildsEnv
pip install -r requirements.txt
uvicorn server:app --port 8000

# Test with client
python -c "
from client import BharatBuildsClient
c = BharatBuildsClient()
obs = c.reset(founder_name='Priya')
print(obs['phase'], obs['idea_description'])
"
```

Or pull the Docker container:
```bash
docker pull registry.hf.space/YOUR_USERNAME-BharatBuildsEnv:latest
docker run -p 7860:7860 registry.hf.space/YOUR_USERNAME-BharatBuildsEnv:latest
```

---

## Training Script

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/BharatBuildsEnv/blob/main/bharat_builds_training.ipynb)

Uses: `Qwen2.5-1.5B-Instruct` + `Unsloth` + `TRL GRPO`

Key design choices:
- **GRPO** (Group Relative Policy Optimization) — no value model needed, efficient on T4
- **4-bit quantization** via Unsloth — fits in free Colab
- **Multi-reward** combining 6 verifiers + environment simulation
- **JSON format reward** — model must output valid structured action

---

## Links

- 📓 **Training Notebook:** [Colab Link](https://colab.research.google.com/...)
- 🤗 **Trained Model:** [HuggingFace Hub](https://huggingface.co/YOUR_USERNAME/bharat-builds-rl)
- 📊 **Training Logs:** [Weights & Biases](https://wandb.ai/...)
- 🎥 **Demo Video:** [YouTube](https://youtube.com/...)
- 📝 **Blog Post:** [HuggingFace Blog](https://huggingface.co/blog/...)

---

## File Structure

```
BharatBuildsEnv/
├── environment.py          # Core RL environment (OpenEnv compliant)
├── verifiers.py            # 6 independent reward verifiers
├── models.py               # Pydantic / dataclass models
├── server.py               # FastAPI server
├── client.py               # Python client
├── openenv.yaml            # OpenEnv manifest
├── requirements.txt
├── Dockerfile
├── bharat_builds_training.ipynb  # Full GRPO training notebook
└── README.md
```

---

## Hackathon Theme

**Theme #5 — Wild Card** (also touching #3.2 Personalized Tasks)

> *20 years from now, no one should feel they can't build something just because they don't have the resources.*

---

*Built for the OpenEnv Hackathon, India 2026*
