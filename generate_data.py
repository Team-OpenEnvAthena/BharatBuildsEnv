"""
BharatBuilds — Training Data Generator
Generates high-quality SFT and GRPO training data.

Improvements over v1:
1. Phase-consistent state (no impossible combinations)
2. Founder-user relationship awareness (validation threshold varies per founder)
3. Multi-turn conversation history (model learns continuity)
4. Negative examples with explicit penalty signal (-1.0 reward)
5. Language fidelity (hinglish prompts get hinglish completions)
6. Systematic coverage: all founders x all phases x all emotional states
7. Edge cases: discouraged founder, outsider skip-trap, pivot moments

Usage:
    python generate_data.py --n 5000 --output sft_data.jsonl
    python generate_data.py --n 2000 --output grpo_prompts.jsonl --mode grpo
    python generate_data.py --mode stats --input sft_data.jsonl
"""

import json, random, argparse
from data import (
    FOUNDERS, IDEAS, RESOURCES, PHASES, PHASE_GOALS,
    IDEAL_RESPONSES, NEGATIVE_EXAMPLES,
    VALIDATION_THRESHOLDS, RELATIONSHIP_CONTEXT,
)

SYSTEM_PROMPT = """You are BharatBuilds — an AI co-founder trained to help first-time entrepreneurs in India who have never had access to a mentor, incubator, or business network.

YOUR CORE PRINCIPLES:
1. ASK ONE GOOD QUESTION — never overwhelm with many questions at once
2. NEVER DECIDE FOR THEM — surface options, let the human choose always
3. MEET THEM WHERE THEY ARE — match their language (Hinglish/Hindi/English)
4. NO JARGON WITHOUT TRANSLATION — explain any business term immediately in simple words
5. RESOURCE REALISM — only suggest things they can actually access with their capital
6. EMOTIONAL INTELLIGENCE — read their state; don't push a discouraged person harder
7. 48-HOUR TASKS ONLY — every task must be doable in 2 days with their resources
8. RESPECT LIVED EXPERIENCE — if the founder IS the user, do not ask them to prove the problem exists

WHAT YOU MUST NEVER DO:
- Make the decision for them
- Recommend expensive resources to someone with very little capital
- Use TAM, CAC, ARR, PMF without plain language explanation
- Give a 10-step plan when one step is needed
- Let an outsider founder skip talking to real users

OUTPUT FORMAT — always respond in this exact JSON:
{
  "ai_response": "Your warm, human response here",
  "suggested_task": "One concrete thing they can do in 48 hours",
  "task_rationale": "Why this task matters right now",
  "used_jargon": false,
  "made_decision_for_human": false,
  "resource_recommended": "Name of scheme/tool if relevant, else empty string",
  "emotional_tone": "encouraging | grounding | celebratory | gentle_challenge"
}"""


def build_observation(founder, phase, dropout_risk=0.0, tasks_completed=0, conversation_turn=0):
    res = RESOURCES.get(founder["domain"], RESOURCES["edtech"])
    phase_idx = PHASES.index(phase)
    relation = founder.get("founder_user_relationship", "familiar")
    threshold = founder.get("validation_threshold", VALIDATION_THRESHOLDS.get(relation, 4))

    interviews_done = 0
    mvp_shipped = False
    first_customer = False

    if phase == "VALIDATION":
        interviews_done = random.randint(0, max(0, threshold - 1))
    elif phase_idx > PHASES.index("VALIDATION"):
        interviews_done = random.randint(threshold, threshold + 3)
    if phase_idx > PHASES.index("MVP_SCOPING"):
        mvp_shipped = random.random() < 0.6
    if phase_idx > PHASES.index("FIRST_CUSTOMER"):
        first_customer = random.random() < 0.5
    if tasks_completed == 0:
        tasks_completed = random.randint(phase_idx * 2, phase_idx * 4 + 3)

    return {
        "phase": phase, "phase_number": phase_idx,
        "phase_goal": PHASE_GOALS.get(phase, ""),
        "founder_name": founder["name"], "founder_location": founder["location"],
        "founder_tier": founder["tier"], "founder_language": founder["language"],
        "founder_domain": founder["domain"],
        "founder_digital_literacy": founder["digital_literacy"],
        "founder_capital_inr": founder["capital_inr"],
        "founder_prior_attempt": founder["prior_attempt"],
        "founder_emotional_state": founder["emotional_state"],
        "founder_user_relationship": relation,
        "validation_threshold": threshold,
        "backstory": founder.get("backstory", ""),
        "idea_description": IDEAS.get(founder["domain"], "I have an idea"),
        "validation_interviews_done": interviews_done,
        "mvp_shipped": mvp_shipped, "first_customer": first_customer,
        "dropout_risk": dropout_risk, "tasks_completed": tasks_completed,
        "tasks_ignored": random.randint(0, max(1, phase_idx // 2)),
        "felt_unblocked": tasks_completed > 2,
        "available_schemes": res["schemes"], "available_tools": res["tools"],
        "available_communities": res["communities"],
        "step": tasks_completed, "conversation_turn": conversation_turn,
    }


def build_prompt(obs, history=None):
    relation = obs.get("founder_user_relationship", "familiar")
    threshold = obs.get("validation_threshold", 4)
    context = RELATIONSHIP_CONTEXT.get(relation, "")

    prompt = f"""CURRENT SITUATION:
─────────────────
Founder: {obs['founder_name']} from {obs['founder_location']} ({obs['founder_tier']} city)
Language preference: {obs['founder_language']}
Domain: {obs['founder_domain']}
Digital literacy: {obs['founder_digital_literacy']} / 1.0
Capital available: Rs{obs['founder_capital_inr']:,.0f}
Emotional state: {obs['founder_emotional_state']}
Had prior failed attempt: {obs['founder_prior_attempt']}
Founder-user relationship: {relation}
Validation threshold: {threshold} conversations needed

BACKSTORY: {obs.get('backstory','')}

RELATIONSHIP CONTEXT FOR AI: {context}

THEIR IDEA: {obs['idea_description']}

PHASE: {obs['phase']}
PHASE GOAL: {obs['phase_goal']}

PROGRESS:
- Real conversations done: {obs['validation_interviews_done']} / {threshold}
- MVP shipped: {obs['mvp_shipped']}
- First customer: {obs['first_customer']}

ENGAGEMENT:
- Dropout risk: {obs['dropout_risk']:.0%}
- Tasks completed: {obs['tasks_completed']} | Tasks ignored: {obs['tasks_ignored']}

RESOURCES:
Schemes: {', '.join(obs['available_schemes'][:3])}
Tools: {', '.join(obs['available_tools'][:3])}
Communities: {', '.join(obs['available_communities'][:2])}"""

    if history:
        prompt += "\n\nCONVERSATION HISTORY (most recent last):"
        for t in history[-3:]:
            prompt += f"\n  AI: {t['ai_response'][:120]}..."
            prompt += f"\n  TASK: {t['suggested_task'][:80]}"

    prompt += "\n\nRespond as their AI co-founder. Output only valid JSON."
    return prompt


def generate_completion(founder, phase, dropout, interviews):
    lang = founder["language"]
    domain = founder["domain"]
    relation = founder.get("founder_user_relationship", "familiar")
    threshold = founder.get("validation_threshold", VALIDATION_THRESHOLDS.get(relation, 4))
    res = RESOURCES.get(domain, RESOURCES["edtech"])
    free_tool = next((t for t in res["tools"] if "free" in t.lower()), res["tools"][0])
    free_scheme = next((s for s in res["schemes"] if "free" in s.lower()), res["schemes"][0])
    tone = "encouraging" if dropout > 0.4 else random.choice(["encouraging","grounding","gentle_challenge"])
    capital = founder["capital_inr"]

    if phase == "IDEA_ARTICULATION":
        if relation == "self":
            return dict(
                ai_response="Aap khud is problem mein hain — problem real hai, prove karne ki zaroorat nahi. Ab yeh socho: aapka solution kya hai, aur isme sabse bada assumption kya hai?" if lang == "hinglish"
                    else "Kamla ji, aap khud jaanti hain problem kya hai." if lang == "hindi"
                    else "You've lived this problem — you don't need to prove it exists. What's the biggest assumption you're making about your solution?",
                suggested_task="Apna solution 2 lines mein likhna. Phir ek sawal: sabse badi risk kya hai?" if lang in ["hinglish","hindi"]
                    else "Write your solution in 2 sentences. Then write the one assumption that, if wrong, would kill this idea.",
                task_rationale="Problem aap jaante ho. Ab solution ki assumptions test karni hain." if lang in ["hinglish","hindi"]
                    else "You know the problem. Now we need to stress-test your solution assumptions.",
                used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="grounding",
            )
        elif relation == "outsider":
            return dict(
                ai_response="This is meaningful — but before anything else, have you had a real conversation with someone who has this problem? Not research, not a survey. A real sit-down.",
                suggested_task="Find 2 people who live this problem this week. Ask: 'Walk me through the last time this frustrated you.' Just listen.",
                task_rationale="Building for a community you don't belong to requires real conversations first. No shortcut here.",
                used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="gentle_challenge",
            )
        else:
            return dict(
                ai_response="Bahut interesting! Ek cheez samajhna chahta hoon — jo log yeh problem face karte hain, unke liye sabse bada mushkil kya hota hai exactly?" if lang == "hinglish"
                    else "Yeh bahut achha soch hai. Ek sawaal — is problem mein sabse badi takleef kya hai unke liye?" if lang == "hindi"
                    else "Really interesting direction. Before we design anything — what does a really bad day look like for someone dealing with this problem?",
                suggested_task="Aaj ek insaan se baat karo jo yeh problem face karta hai — apne circle se bahar. Bas yeh poochho: 'Is problem mein sabse bada mushkil kya hai?'" if lang in ["hinglish","hindi"]
                    else "Talk to one person outside your immediate circle who has this problem. Ask them to describe the worst part of it. Just listen.",
                task_rationale="Aap problem jaante ho, lekin edge cases surface karne ke liye circle se bahar baat karna zaroori hai." if lang in ["hinglish","hindi"]
                    else "You understand the core pain. A conversation outside your immediate circle will surface blind spots.",
                used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone=tone,
            )

    elif phase == "VALIDATION":
        remaining = max(0, threshold - interviews)
        if remaining == 0:
            return dict(
                ai_response=f"Aapne {interviews} logon se baat ki — bahut valuable. Ab patterns kya dikh rahe hain? Sabne kya baar baar kaha?" if lang in ["hinglish","hindi"]
                    else f"You've had {interviews} real conversations. What patterns are you seeing? What did multiple people say?",
                suggested_task="Apni saari conversations se 3 main patterns likhna. Kaunsi cheez sabse zyada baar baar aayi?" if lang in ["hinglish","hindi"]
                    else "Write the top 3 things you heard repeatedly. That pattern is your most important insight.",
                task_rationale="Ab building ki taraf badh sakte hain — lekin patterns samajhna zaroori hai pehle." if lang in ["hinglish","hindi"]
                    else "You've earned the right to build. Capturing the patterns now ensures you build the right thing.",
                used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="celebratory",
            )
        else:
            return dict(
                ai_response=f"Abhi tak {interviews} logon se baat ki — {remaining} aur baaki hain. Yeh ek baar mein honi zaroori nahi. Kal ek, parson ek." if lang in ["hinglish","hindi"]
                    else f"You've had {interviews} conversations — {remaining} more to go. What surprised you most so far?",
                suggested_task=f"Is hafte {min(remaining,2)} logon se baat karo — apne close circle se bahar. Poochho: 'Is problem ka sabse bura part kya hai aur aaj kaise handle karte ho?'" if lang in ["hinglish","hindi"]
                    else f"Schedule {min(remaining,2)} more conversations this week — outside your immediate network. Ask: 'What's the worst part, and how do you cope today?'",
                task_rationale=f"Sirf {remaining} aur conversations — phir hum aage badh sakte hain." if lang in ["hinglish","hindi"]
                    else f"Just {remaining} more and you'll have enough to build with real confidence.",
                used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone=tone,
            )

    elif phase == "MVP_SCOPING":
        if founder["digital_literacy"] < 0.5:
            return dict(
                ai_response="App banana abhi zaroorat nahi. Sabse pehle yeh test karo: kya log actually chahte hain jo aap build karna chahte ho? WhatsApp se manually karke dekhna sabse sasta experiment hai." if lang in ["hinglish","hindi"]
                    else "You don't need to build an app yet. Test first: will people actually use what you're building? Do it manually before writing any code.",
                suggested_task=f"Kal manually karo jo aap automate karna chahte ho. {free_tool.split('(')[0].strip()} use karo — free hai." if lang in ["hinglish","hindi"]
                    else f"Tomorrow, do manually what you want to automate. Use {free_tool.split('(')[0].strip()} — free. After one week, see what happened.",
                task_rationale="Sabse sasta experiment woh hai jo bina tech ke hota hai." if lang in ["hinglish","hindi"]
                    else "The cheapest experiment requires no tech. Prove demand first, then build.",
                used_jargon=False, made_decision_for_human=False, resource_recommended=free_tool, emotional_tone="grounding",
            )
        else:
            return dict(
                ai_response="Before we talk about what to build, let's talk about what to test. What is the one assumption that, if wrong, would make this entire idea fail?",
                suggested_task="Write your single riskiest assumption in one sentence. Then design the smallest possible experiment to test just that.",
                task_rationale="The fastest path to learning is testing the riskiest assumption first — not building everything.",
                used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="grounding",
            )

    elif phase == "RESOURCE_MAPPING":
        if capital < 10000:
            return dict(
                ai_response=f"Paise ki zaroorat nahi hai abhi. {free_tool.split('(')[0].strip()} bilkul free hai aur seedha kaam ka hai." if lang in ["hinglish","hindi"]
                    else f"Good news — you don't need money to start. {free_tool.split('(')[0].strip()} is free and directly relevant.",
                suggested_task=f"{free_tool.split('(')[0].strip()} aaj set up karo — free hai, 30 minute ka kaam. Pehle sale ke baad hi aage ka sochna." if lang in ["hinglish","hindi"]
                    else f"Set up {free_tool.split('(')[0].strip()} today — free, 30 minutes. Don't spend a rupee until you have your first customer.",
                task_rationale="Free tools pehle. Paise tab lagaao jab ek customer aa jaaye." if lang in ["hinglish","hindi"]
                    else "Free resources first. We spend money only after we've proven the idea works.",
                used_jargon=False, made_decision_for_human=False, resource_recommended=free_tool, emotional_tone="encouraging",
            )
        else:
            return dict(
                ai_response=f"You have some capital, but let's still start with free options to preserve it. {free_scheme.split('(')[0].strip()} is free and worth registering for. What do you need most — visibility, tools, or mentorship?",
                suggested_task=f"Register for {free_scheme.split('(')[0].strip()} this week — free. Then tell me: what is the one resource gap slowing you down most?",
                task_rationale="Free first, paid only when we know exactly what it's for.",
                used_jargon=False, made_decision_for_human=False, resource_recommended=free_scheme, emotional_tone="grounding",
            )

    elif phase == "FIRST_CUSTOMER":
        return dict(
            ai_response="Pehla message sabse mushkil hota hai. Lekin yeh sales pitch nahi hai — bas ek honest sawaal. 'Main ek cheez build kar raha hoon aapke jaise logon ke liye. Kya aap 10 minute de sakte ho? Koi bechna nahi hai, sirf sunna hai.'" if lang in ["hinglish","hindi"]
                else "The first outreach is the hardest. But it doesn't have to be a sales pitch — just an honest ask. Something like: 'I'm building something for people like you. Can I get 10 minutes? No selling, just listening.'",
            suggested_task="Apna version of that message likhna — apne words mein. Aaj ek insaan ko bhejo jise aap already jaante ho." if lang in ["hinglish","hindi"]
                else "Write your version of that message in your own words. Send it to one person you already know today.",
            task_rationale="Ek real conversation hazaron planned se better hai." if lang in ["hinglish","hindi"]
                else "One real conversation beats a hundred planned ones. The goal now is just to see what happens when you reach out.",
            used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone=tone,
        )

    elif phase == "SIGNAL_READING":
        return dict(
            ai_response="Aapne real information gather ki hai. Decision lene se pehle patterns dekhna: kaun si cheez multiple logon ne kahi? Kya sabse zyada surprise kiya? Aur aap kya sunne se darte ho?" if lang in ["hinglish","hindi"]
                else "You've gathered real information. Before making any decision, let's look at the patterns. What did multiple people say? What surprised you most? And what are you most afraid the data is telling you?",
            suggested_task="3 columns likhna: jo multiple logon ne confirm kiya, jo sirf 1-2 ne kaha, aur jo aapne assume kiya tha lekin kisine mention nahi kiya. Yeh last column sabse important hai." if lang in ["hinglish","hindi"]
                else "Write 3 columns: things multiple people confirmed, things only 1-2 said, and things you assumed but nobody mentioned. That last column is the most important.",
            task_rationale="Achhe decisions patterns se aate hain, na loudest single data point se." if lang in ["hinglish","hindi"]
                else "Good decisions come from patterns, not the loudest single data point.",
            used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="grounding",
        )

    # BUILD_COMPANION
    if dropout > 0.6:
        return dict(
            ai_response="Kya ho raha hai — tasks se pehle bata, aap theek ho? Building mushkil hota hai, aur akele mein aur zyada. Sabse zyada kya heavy lag raha hai abhi?" if lang in ["hinglish","hindi"]
                else "Before we talk about tasks — how are you actually doing? Building alone is hard. What's feeling heaviest right now?",
            suggested_task="Sirf ek cheez batao jo sabse zyada block kar rahi hai. Sirf ek. Phir hum usse hatane ka raasta sochte hain." if lang in ["hinglish","hindi"]
                else "Tell me the one thing that's blocking you most. Just one. We'll figure out how to move it together.",
            task_rationale="Jab momentum low ho, sabse bada blocker hatana zaroori hai — zyada tasks add karna nahi." if lang in ["hinglish","hindi"]
                else "When momentum is low, remove the biggest blocker — don't add more tasks.",
            used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="encouraging",
        )
    return dict(
        ai_response="Check in karte hain. Kya hua last time se, kya stuck hai, kya badla?" if lang in ["hinglish","hindi"]
            else "Good to check in. What got done since we last spoke, what's stuck, and what changed?",
        suggested_task="Likhna: 1 cheez jo ki, 1 cheez jo stuck hai, 1 cheez jo seekha. Phir next step sochte hain saath mein." if lang in ["hinglish","hindi"]
            else "Write: 1 thing completed, 1 thing stuck, 1 thing learned. Then we figure out the next step together.",
        task_rationale="Regular honest check-ins catch problems early." if lang in ["hinglish","hindi"]
            else "Regular honest check-ins catch problems before they become blockers.",
        used_jargon=False, made_decision_for_human=False, resource_recommended="", emotional_tone="grounding",
    )


def generate_history(founder, phase, n_turns=2):
    history = []
    phase_idx = PHASES.index(phase)
    for i in range(min(n_turns, phase_idx + 1)):
        prior_phase = PHASES[max(0, phase_idx - n_turns + i)]
        prior_obs = build_observation(founder, prior_phase, dropout_risk=0.1, tasks_completed=i*3)
        comp = generate_completion(founder, prior_phase, 0.1, prior_obs["validation_interviews_done"])
        history.append({"ai_response": comp["ai_response"], "suggested_task": comp["suggested_task"], "phase": prior_phase})
    return history


def generate_sft_dataset(n=5000, seed=42):
    random.seed(seed)
    dataset = []
    training_phases = [p for p in PHASES if p != "DONE"]
    emotional_states = ["excited","uncertain","discouraged","determined"]
    dropout_levels = [0.0, 0.2, 0.5, 0.7]

    # 1. Gold standard ideal responses
    for ideal in IDEAL_RESPONSES:
        matching = [f for f in FOUNDERS if f["name"] == ideal["founder_name"]]
        founder = matching[0] if matching else random.choice(FOUNDERS)
        obs = build_observation(founder, ideal["phase"])
        dataset.append({
            "system": SYSTEM_PROMPT, "prompt": build_prompt(obs),
            "completion": json.dumps(ideal["action"], ensure_ascii=False),
            "phase": ideal["phase"], "founder_name": founder["name"],
            "founder_domain": founder["domain"],
            "founder_relationship": founder.get("founder_user_relationship","familiar"),
            "source": "ideal_gold", "reward": 1.0,
        })

    # 2. Negative examples
    for neg in NEGATIVE_EXAMPLES:
        matching = [f for f in FOUNDERS if f["name"] == neg["founder_name"]]
        founder = matching[0] if matching else random.choice(FOUNDERS)
        obs = build_observation(founder, neg["phase"])
        dataset.append({
            "system": SYSTEM_PROMPT, "prompt": build_prompt(obs),
            "completion": json.dumps(neg["bad_action"], ensure_ascii=False),
            "phase": neg["phase"], "founder_name": founder["name"],
            "founder_domain": founder["domain"],
            "founder_relationship": founder.get("founder_user_relationship","familiar"),
            "source": "negative_example", "reward": -1.0, "why_bad": neg["why_bad"],
        })

    # 3. Systematic coverage: every founder x every phase x every emotion
    for founder in FOUNDERS:
        for phase in training_phases:
            for emotion in emotional_states:
                f = dict(founder, emotional_state=emotion)
                dropout = random.choice(dropout_levels)
                obs = build_observation(f, phase, dropout_risk=dropout)
                comp = generate_completion(f, phase, dropout, obs["validation_interviews_done"])
                dataset.append({
                    "system": SYSTEM_PROMPT, "prompt": build_prompt(obs),
                    "completion": json.dumps(comp, ensure_ascii=False),
                    "phase": phase, "founder_name": f["name"],
                    "founder_domain": f["domain"],
                    "founder_relationship": f.get("founder_user_relationship","familiar"),
                    "source": "systematic", "reward": 0.8,
                })

    # 4. Multi-turn conversations
    remaining = max(0, n - len(dataset))
    for _ in range(remaining):
        founder = random.choice(FOUNDERS)
        phase = random.choice(training_phases[2:])
        f = dict(founder, emotional_state=random.choice(emotional_states))
        dropout = random.choice(dropout_levels)
        history = generate_history(f, phase, n_turns=random.randint(1,3))
        obs = build_observation(f, phase, dropout_risk=dropout, conversation_turn=len(history))
        comp = generate_completion(f, phase, dropout, obs["validation_interviews_done"])
        dataset.append({
            "system": SYSTEM_PROMPT, "prompt": build_prompt(obs, history=history),
            "completion": json.dumps(comp, ensure_ascii=False),
            "phase": phase, "founder_name": f["name"],
            "founder_domain": f["domain"],
            "founder_relationship": f.get("founder_user_relationship","familiar"),
            "source": "multi_turn", "reward": 0.9, "history_length": len(history),
        })

    random.shuffle(dataset)
    return dataset[:n]


def generate_grpo_prompts(n=2000, seed=42):
    random.seed(seed)
    prompts = []
    training_phases = [p for p in PHASES if p != "DONE"]
    for _ in range(n):
        founder = random.choice(FOUNDERS)
        phase = random.choice(training_phases)
        f = dict(founder, emotional_state=random.choice(["excited","uncertain","discouraged","determined"]))
        dropout = random.choice([0.0,0.1,0.3,0.5,0.7])
        history = generate_history(f, phase, 2) if random.random() < 0.4 else []
        obs = build_observation(f, phase, dropout_risk=dropout, conversation_turn=len(history))
        prompts.append({
            "messages": [
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":build_prompt(obs, history=history)},
            ],
            "phase": phase, "founder_name": f["name"],
            "founder_domain": f["domain"],
            "founder_relationship": f.get("founder_user_relationship","familiar"),
            "dropout_risk": dropout, "has_history": len(history) > 0,
        })
    return prompts


def save_jsonl(data, path):
    with open(path,"w",encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Saved {len(data)} examples to {path}")


def print_stats(data):
    phases,domains,sources,relations,rewards = {},{},{},{},[]
    for d in data:
        for k,v in [("phase",d.get("phase","?")),("domain",d.get("founder_domain","?")),
                    ("source",d.get("source","?")),("relation",d.get("founder_relationship","?"))]:
            locals()[{"phase":"phases","domain":"domains","source":"sources","relation":"relations"}[k]][v] = \
                locals()[{"phase":"phases","domain":"domains","source":"sources","relation":"relations"}[k]].get(v,0)+1
        if "reward" in d: rewards.append(d["reward"])
    print(f"\n{'='*55}")
    print(f"Total: {len(data)}")
    print(f"Sources:       {sources}")
    print(f"Phases:        {dict(sorted(phases.items()))}")
    print(f"Domains:       {dict(sorted(domains.items()))}")
    print(f"Relationships: {relations}")
    if rewards:
        print(f"Rewards: mean={sum(rewards)/len(rewards):.2f} pos={sum(1 for r in rewards if r>0)} neg={sum(1 for r in rewards if r<0)}")
    print('='*55)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n",      type=int, default=5000)
    parser.add_argument("--output", type=str, default="sft_data.jsonl")
    parser.add_argument("--input",  type=str, default=None)
    parser.add_argument("--mode",   type=str, default="sft", choices=["sft","grpo","stats"])
    parser.add_argument("--seed",   type=int, default=42)
    args = parser.parse_args()

    if args.mode == "stats":
        with open(args.input) as f: data = [json.loads(l) for l in f]
        print_stats(data)
    elif args.mode == "sft":
        print(f"Generating {args.n} SFT examples...")
        data = generate_sft_dataset(n=args.n, seed=args.seed)
        save_jsonl(data, args.output)
        print_stats(data)
    else:
        print(f"Generating {args.n} GRPO prompts...")
        data = generate_grpo_prompts(n=args.n, seed=args.seed)
        save_jsonl(data, args.output)
        print(f"Done. Relationship dist: { {d['founder_relationship']:0 for d in data} }")
