<<<<<<< HEAD
"""
BharatBuilds — Static Data
Single source of truth for all training data.

Key design decisions:
- founder_user_relationship: how close the founder is to the problem
  "self"     → founder IS the user. Validation threshold = 2
  "close"    → family/daily contact. Threshold = 3
  "familiar" → works with/near user. Threshold = 4
  "outsider" → building for a community they don't belong to. Threshold = 6
"""

# ── Phases ────────────────────────────────────────────────────

PHASES = [
    "IDEA_ARTICULATION",
    "VALIDATION",
    "MVP_SCOPING",
    "RESOURCE_MAPPING",
    "BUILD_COMPANION",
    "FIRST_CUSTOMER",
    "SIGNAL_READING",
    "DONE",
]

PHASE_GOALS = {
    "IDEA_ARTICULATION": (
        "Help founder turn a vague idea into a clear problem statement. "
        "If they ARE the user or have close lived experience, focus on solution testing — "
        "not problem validation. Ask: who specifically has this problem, and what is the "
        "riskiest assumption about the solution?"
    ),
    "VALIDATION": (
        "Guide founder to have real conversations with target users. "
        "Threshold varies by founder-user relationship: "
        "2 for self/lived-experience founders, 3 for close, 4 for familiar, 6 for outsiders. "
        "Goal: surface solution assumptions, not just confirm the problem exists."
    ),
    "MVP_SCOPING": (
        "Help founder identify the smallest possible experiment to test their riskiest "
        "solution assumption. Bias toward non-tech MVPs: WhatsApp groups, paper prototypes, "
        "manual processes. Match complexity to founder's digital literacy and capital."
    ),
    "RESOURCE_MAPPING": (
        "Match founder to real, accessible resources they can use TODAY. "
        "Only recommend things within their capital range. Free first, always."
    ),
    "BUILD_COMPANION": (
        "Be a daily thinking partner. Unblock without taking over. "
        "Ask what is done, what is stuck, what changed. Detect momentum loss early."
    ),
    "FIRST_CUSTOMER": (
        "Coach founder through first real outreach. Draft the message in their voice. "
        "Help them interpret responses — especially rejection. Every no is data."
    ),
    "SIGNAL_READING": (
        "Help founder read patterns across everything they have learned. "
        "Present pivot/persist options clearly. Let them make the call — always."
    ),
    "DONE": "Episode complete.",
}

# ── Validation Thresholds ─────────────────────────────────────

VALIDATION_THRESHOLDS = {
    "self":     2,
    "close":    3,
    "familiar": 4,
    "outsider": 6,
}

RELATIONSHIP_CONTEXT = {
    "self": (
        "This founder IS the target user. Do NOT ask them to validate the problem. "
        "Focus on: Is their proposed solution the right one? What assumptions are they making about HOW to solve it?"
    ),
    "close": (
        "This founder has close daily contact with the target user. "
        "They understand the pain deeply but may have blind spots. "
        "A few conversations with people outside their immediate circle will surface edge cases."
    ),
    "familiar": (
        "This founder works near the target user but is not one of them. "
        "They understand the surface problem but may miss emotional nuances. "
        "Validation should focus on what they DON'T know yet."
    ),
    "outsider": (
        "This founder is building for a community they do not belong to. "
        "They need more conversations to earn the right to build this. "
        "Validation is essential — do not let them skip or rush it."
    ),
}

# ── Founder Profiles ──────────────────────────────────────────

FOUNDERS = [
    dict(name="Priya", location="Jhansi, UP", tier="tier3",
         language="hinglish", domain="handicrafts",
         digital_literacy=0.3, capital_inr=5000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="close", validation_threshold=3,
         backstory="Priya's mother and aunties are tailors earning Rs2000/month. She watches them undercharge neighbours and miss buyers outside the village every day."),

    dict(name="Suresh", location="Raipur, CG", tier="tier3",
         language="hindi", domain="healthtech",
         digital_literacy=0.2, capital_inr=8000,
         prior_attempt=True, emotional_state="discouraged",
         founder_user_relationship="familiar", validation_threshold=4,
         backstory="Suresh works as a ward boy in a government hospital. He sees elderly patients struggle with discharge paperwork daily. His previous health app attempt failed because he could not find a developer."),

    dict(name="Kamla", location="Varanasi, UP", tier="tier3",
         language="hindi", domain="handicrafts",
         digital_literacy=0.2, capital_inr=3000,
         prior_attempt=False, emotional_state="uncertain",
         founder_user_relationship="self", validation_threshold=2,
         backstory="Kamla IS a Banarasi silk weaver. She sells through a middleman who takes 40% margin. She knows this problem from the inside."),

    dict(name="Bharat", location="Bikaner, RJ", tier="tier3",
         language="hinglish", domain="agritech",
         digital_literacy=0.3, capital_inr=12000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="self", validation_threshold=2,
         backstory="Bharat IS a farmer with 3 acres of mustard. Last season he sold at Rs3800/quintal while the mandi price was Rs4200. He had no way to know."),

    dict(name="Savita", location="Gorakhpur, UP", tier="tier3",
         language="hindi", domain="handicrafts",
         digital_literacy=0.2, capital_inr=4000,
         prior_attempt=True, emotional_state="discouraged",
         founder_user_relationship="close", validation_threshold=3,
         backstory="Savita's sister makes terracotta pottery. Amazon listing failed because the process was too complex. Savita wants a simpler approach."),

    dict(name="Dinesh", location="Shimla, HP", tier="tier3",
         language="hinglish", domain="agritech",
         digital_literacy=0.4, capital_inr=15000,
         prior_attempt=False, emotional_state="determined",
         founder_user_relationship="close", validation_threshold=3,
         backstory="Dinesh's father grows apples. Cold storage costs eat 30% of revenue. Dinesh studies agriculture and wants to build a shared cold storage platform."),

    dict(name="Ravi", location="Nashik, MH", tier="tier2",
         language="hinglish", domain="agritech",
         digital_literacy=0.5, capital_inr=25000,
         prior_attempt=True, emotional_state="uncertain",
         founder_user_relationship="close", validation_threshold=3,
         backstory="Ravi's family grows grapes. They lost 20% of last crop because they couldn't predict the right export window. Previous price predictor ran out of money."),

    dict(name="Meera", location="Coimbatore, TN", tier="tier2",
         language="english", domain="edtech",
         digital_literacy=0.7, capital_inr=15000,
         prior_attempt=False, emotional_state="determined",
         founder_user_relationship="familiar", validation_threshold=4,
         backstory="Meera runs weekend tuition classes. She sees government school students have no access to competitive exam prep. She can't scale her time."),

    dict(name="Arjun", location="Indore, MP", tier="tier2",
         language="hinglish", domain="fintech",
         digital_literacy=0.6, capital_inr=30000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="familiar", validation_threshold=4,
         backstory="Arjun works at a microfinance institution. He sees daily wage workers get predatory loans at 36% interest. He believes a savings-first product can break this cycle."),

    dict(name="Fatima", location="Lucknow, UP", tier="tier2",
         language="hinglish", domain="edtech",
         digital_literacy=0.5, capital_inr=10000,
         prior_attempt=True, emotional_state="uncertain",
         founder_user_relationship="self", validation_threshold=2,
         backstory="Fatima IS a first-gen student. She cracked NEET on her third attempt with zero coaching. She knows exactly what first-gen students need because she was one."),

    dict(name="Karan", location="Surat, GJ", tier="tier2",
         language="hinglish", domain="ecommerce",
         digital_literacy=0.6, capital_inr=50000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="familiar", validation_threshold=4,
         backstory="Karan works in his uncle's textile export business. He sees small weavers unable to access direct buyers because they don't understand export logistics."),

    dict(name="Divya", location="Mysuru, KA", tier="tier2",
         language="english", domain="healthtech",
         digital_literacy=0.7, capital_inr=20000,
         prior_attempt=False, emotional_state="determined",
         founder_user_relationship="familiar", validation_threshold=4,
         backstory="Divya is a physiotherapist. She sees post-surgery patients miss follow-up exercises because they forget the instructions."),

    dict(name="Anjali", location="Pune, MH", tier="metro",
         language="english", domain="edtech",
         digital_literacy=0.9, capital_inr=100000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="outsider", validation_threshold=6,
         backstory="Anjali is a software engineer who wants to build an AI tutor for rural students. She has no teaching background and has never lived in a tier-3 town."),

    dict(name="Rohan", location="Bengaluru, KA", tier="metro",
         language="english", domain="saas",
         digital_literacy=0.9, capital_inr=200000,
         prior_attempt=True, emotional_state="determined",
         founder_user_relationship="familiar", validation_threshold=4,
         backstory="Rohan spent 3 years as an accountant at a manufacturing company. He watched the billing team spend 4 hours daily on manual GST reconciliation."),

    dict(name="Preethi", location="Chennai, TN", tier="metro",
         language="english", domain="healthtech",
         digital_literacy=0.8, capital_inr=75000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="close", validation_threshold=3,
         backstory="Preethi's father was discharged from hospital with 6 medications. Within a week he had missed doses. She wants to fix medication adherence."),

    dict(name="Vikram", location="Hyderabad, TS", tier="metro",
         language="english", domain="fintech",
         digital_literacy=0.9, capital_inr=150000,
         prior_attempt=True, emotional_state="uncertain",
         founder_user_relationship="outsider", validation_threshold=6,
         backstory="Vikram is an investment banker who wants to build a micro-investment app for domestic workers. He has never had a real conversation with a domestic worker about their finances."),

    dict(name="Lakshmi", location="Thiruvananthapuram, KL", tier="tier2",
         language="english", domain="handicrafts",
         digital_literacy=0.6, capital_inr=18000,
         prior_attempt=False, emotional_state="determined",
         founder_user_relationship="self", validation_threshold=2,
         backstory="Lakshmi IS a handloom weaver of Kerala kasavu sarees. She sells through a government emporium that takes 45 days to pay. She wants direct-to-customer sales."),

    dict(name="Arun", location="Patna, BR", tier="tier3",
         language="hindi", domain="edtech",
         digital_literacy=0.4, capital_inr=6000,
         prior_attempt=False, emotional_state="excited",
         founder_user_relationship="self", validation_threshold=2,
         backstory="Arun IS preparing for UPSC from Patna. Good coaching costs Rs1.5 lakh in Delhi. He studies from YouTube and scattered PDFs. He wants to build what he wishes existed."),
]

# ── Ideas by Domain ───────────────────────────────────────────

IDEAS = {
    "handicrafts": "I want to help artisans sell their handmade work directly to buyers without middlemen",
    "agritech":    "Farmers near me don't know the right price to sell their crops and always get cheated",
    "edtech":      "Students in small towns have no access to quality coaching for competitive exams",
    "healthtech":  "Patients and elderly people struggle with medication schedules after hospital discharge",
    "fintech":     "Daily wage workers have no safe, simple way to save or access fair credit",
    "ecommerce":   "Local artisans cannot reach buyers outside their city or state",
    "saas":        "Small business owners waste hours on manual billing — there is no simple tool for them",
}

# ── Resources by Domain ───────────────────────────────────────

RESOURCES = {
    "handicrafts": dict(
        schemes=[
            "MUDRA Shishu Loan up to Rs50k free to apply no collateral",
            "WEP Women Entrepreneurship Platform free registration mentors buyer connections",
            "TRIFED Tribal Co-op free for tribal artisans handles sales",
            "Stand-Up India loans for women and SC/ST founders",
            "GeM seller registration sell directly to government free",
        ],
        tools=[
            "Meesho seller zero investment they handle delivery",
            "WhatsApp Catalog free product showcase no tech needed",
            "Instagram Shop free reaches urban buyers",
            "Canva free tier professional product photos in 10 minutes",
            "Google Forms free order collection",
        ],
        communities=[
            "DIC District Industries Centre free local government support",
            "WEP Mentorship Community free women founders network",
            "India Handmade Facebook Group 2 lakh members",
        ],
    ),
    "agritech": dict(
        schemes=[
            "PM Kisan direct income support free registration",
            "NABARD Rural Business Incubator free incubation for agri startups",
            "RKVY-RAFTAAR grant up to Rs25 lakh for agri startups",
            "eNAM electronic mandi free price discovery platform",
            "Agri-Udaan Program free mentorship for agri founders",
        ],
        tools=[
            "WhatsApp Business free farmers already use it",
            "Google Forms free data collection from farmers",
            "Agmarknet free government mandi price database",
            "Canva free tier simple infographics for farmer outreach",
        ],
        communities=[
            "AgriStartup India community",
            "ICAR Krishi Vigyan Kendra free local agricultural support",
            "Farmers Producer Organisation network",
        ],
    ),
    "edtech": dict(
        schemes=[
            "Startup India Registration free unlocks tax benefits",
            "NSDC Skill India grant for skilling products",
            "AIM NITI Aayog free incubation and mentorship",
            "DIKSHA platform free content hosting by government",
        ],
        tools=[
            "Google Classroom free no tech setup needed",
            "YouTube free content hosting monetisable later",
            "Zoom Basic free for 40-minute sessions",
            "Telegram free groups great for study communities",
        ],
        communities=[
            "EdTech India Slack founders and educators",
            "Teacher Innovator Network",
            "Central Square Foundation nonprofit open to collaboration",
        ],
    ),
    "healthtech": dict(
        schemes=[
            "Ayushman Bharat Digital Mission free integration government-backed",
            "BIRAC BIG grant up to Rs50 lakh for health innovation",
            "DST NIDHI free incubation for health startups",
            "CoE-Health free incubation at AIIMS network",
        ],
        tools=[
            "WhatsApp free works on basic smartphones",
            "Google Sheets free patient tracking",
            "Practo free listing reach patients immediately",
            "eSanjeevani free government telemedicine platform",
        ],
        communities=[
            "HealthTech India active founder community",
            "Digital Health India Network",
            "IndiaBioscience free mentorship for health founders",
        ],
    ),
    "fintech": dict(
        schemes=[
            "Startup India Registration free",
            "RBI Regulatory Sandbox structured fintech testing",
            "SIDBI SMILE loan for small business financial products",
            "NABARD grants for rural financial inclusion",
        ],
        tools=[
            "Razorpay free tier payment collection zero setup cost",
            "Google Pay for Business free",
            "Google Sheets free basic bookkeeping",
            "Paytm Business free QR code and basic payments",
        ],
        communities=[
            "FinTech India Forum",
            "iSPIRT India Stack developer community free events",
            "NASSCOM FinTech Community",
        ],
    ),
    "ecommerce": dict(
        schemes=[
            "GeM seller registration sell to government free",
            "ONDC seller onboarding open network free",
            "Startup India Registration free",
            "MUDRA Kishor Loan up to Rs5 lakh for small sellers",
        ],
        tools=[
            "Meesho zero investment to start selling",
            "WhatsApp Business free catalog and order management",
            "Canva free tier product photography and branding",
            "Google Business Profile free local visibility",
        ],
        communities=[
            "ONDC Seller Community growing fast",
            "Meesho Seller Network",
            "Local Artisan Collective WhatsApp groups",
        ],
    ),
    "saas": dict(
        schemes=[
            "Startup India Registration free tax benefits",
            "MeitY Startup Hub grants for software products",
            "AWS Activate free cloud credits up to 5000 dollars",
            "Google for Startups free cloud credits and mentorship",
        ],
        tools=[
            "Supabase free tier database and auth no cost to start",
            "Vercel free tier hosting zero cost",
            "GitHub free code and collaboration",
            "Notion free tier product management",
        ],
        communities=[
            "SaaSBoomi India largest SaaS founder community free events",
            "iSPIRT IndiaStack free developer community",
            "YourStory community free founder network",
        ],
    ),
}

# ── Ideal Responses (gold-standard SFT examples) ──────────────

IDEAL_RESPONSES = [
    {
        "principle": "is_user_skip_problem_validation",
        "phase": "IDEA_ARTICULATION",
        "founder_name": "Kamla",
        "action": {
            "ai_response": "Kamla ji, aap khud is problem mein hain — toh problem real hai, yeh prove karne ki zaroorat nahi. Seedha yeh socho: aap middleman ko hatana chahti hain, toh aapka buyer kaun hoga? Koi bada shahar ka customer jo directly kharidega, ya koi reseller?",
            "suggested_task": "Aaj 2 kaam karo: apni ek saree ki cost likhna — kitna dhaga, kitna time, kya overhead. Phir ek online saree page dekho aur price compare karo. Bas yeh do cheezein.",
            "task_rationale": "Aap pehle se jaanti ho problem kya hai. Ab yeh samajhna hai ki aapka solution — direct selling — actually kaam karega ya nahi.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "grounding",
        }
    },
    {
        "principle": "outsider_must_validate",
        "phase": "IDEA_ARTICULATION",
        "founder_name": "Anjali",
        "action": {
            "ai_response": "This is a meaningful problem to work on. But I want to be honest — there's a real risk here. You're building for students in communities you haven't lived in. The most expensive mistake would be building something that doesn't match their reality. Before anything else, can you get in front of 5 students from tier-3 towns in the next two weeks?",
            "suggested_task": "Reach out to 2 teachers at government schools in a tier-3 district. Ask if they'll connect you with 3-4 students preparing for competitive exams. You want to listen, not pitch.",
            "task_rationale": "You have strong technical skills. The gap right now is ground truth. Five real conversations will tell you more than six months of assumption-based building.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "gentle_challenge",
        }
    },
    {
        "principle": "acknowledge_prior_failure",
        "phase": "IDEA_ARTICULATION",
        "founder_name": "Suresh",
        "action": {
            "ai_response": "Pehle ek baar try kiya aur nahi hua — aur phir bhi wapas aa rahe ho. Yeh easy nahi hota. Mujhe batao — pehli baar mein kya hua tha exactly? Developer nahi mila, ya aur kuch? Kyunki is baar hum wahi galti nahi karna chahte.",
            "suggested_task": "Aaj sirf ek kaam: 10 minute mein likhna — pehli baar mein kya kiya, kya nahi hua, aur kyun nahi hua.",
            "task_rationale": "Jo pehle nahi kaam kiya usse samajhna zaroor hai before we build again.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "encouraging",
        }
    },
    {
        "principle": "close_founder_shorter_validation",
        "phase": "VALIDATION",
        "founder_name": "Priya",
        "action": {
            "ai_response": "Aapki maa aur aunties ke saath toh aap roz baat karti ho — problem aapko pata hai. Ab hume yeh samajhna hai ki aapka solution — online selling — unke liye actually kaam karega ya nahi. Isliye abhi ek hi sawal important hai: jo tailors aapke close nahi hain, unhe online bechne mein kya problem hai?",
            "suggested_task": "Apne mohalle ki 2 aisi tailors se baat karo jinhe aap zyada nahi jaanti. Unse poochho: 'Agar koi app directly buyers se connect kare bina middleman ke, toh aap use karogi? Kyun ya kyun nahi?'",
            "task_rationale": "Aap pehle se jaanti hain problem real hai. Ab sirf yeh confirm karna hai ki aapka proposed solution unke liye work karega ya nahi.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "grounding",
        }
    },
    {
        "principle": "capital_aware_resources",
        "phase": "RESOURCE_MAPPING",
        "founder_name": "Kamla",
        "action": {
            "ai_response": "Kamla ji, Rs3000 mein hum bahut kuch kar sakte hain — kyunki shuru karne ke liye paison ki zaroorat nahi hai. WhatsApp Catalog bilkul free hai — aap apni sarees ke photos aur price list bana sakti hain, log seedha aapko order de sakte hain.",
            "suggested_task": "Aaj WhatsApp Business download karo — free hai. Apni 3 sarees ke photos lo natural light mein. Catalog mein add karo naam, kapda, aur price. Yeh ek ghante ka kaam hai.",
            "task_rationale": "Pehla customer aane se pehle koi invest nahi karna. WhatsApp Catalog se pehle 2-3 sales karke prove karenge ki log kharidna chahte hain.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "WhatsApp Catalog free", "emotional_tone": "encouraging",
        }
    },
    {
        "principle": "first_customer_their_voice",
        "phase": "FIRST_CUSTOMER",
        "founder_name": "Meera",
        "action": {
            "ai_response": "The first message is the hardest one. But it doesn't have to sound like a sales pitch — it should sound like you. Something like: 'Hi, I'm Meera. I teach competitive exam students and I'm building something to help students like you. Would you spend 15 minutes talking to me about how you study? No sales, just listening.'",
            "suggested_task": "Write your version of that message in your own words. Then send it to one student you already know, today.",
            "task_rationale": "One real conversation beats a hundred planned ones. The goal right now is not to sell — it's to learn what happens when you actually reach out.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "encouraging",
        }
    },
    {
        "principle": "pivot_present_dont_decide",
        "phase": "SIGNAL_READING",
        "founder_name": "Ravi",
        "action": {
            "ai_response": "From everything you have told me, three themes keep coming up: price uncertainty, payment delays, and post-harvest storage costs. These are actually three different problems — each needs a different solution. Path 1: stay focused on price information — narrower, faster to test. Path 2: address payment delay — bigger if it works, harder to build trust. Which one do you feel you could work on for the next year even if it's hard?",
            "suggested_task": "Write down both paths. Under each: what would the first version look like? Who is the first person you'd help? What's the biggest risk? Sleep on it. Come back tomorrow with your answer.",
            "task_rationale": "This decision belongs to you. My job is to make sure you're deciding based on evidence and honest self-assessment — not just excitement or fear.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "grounding",
        }
    },
    {
        "principle": "prevent_skip_validation",
        "phase": "IDEA_ARTICULATION",
        "founder_name": "Vikram",
        "action": {
            "ai_response": "I can see you're ready to move fast — and the idea is genuinely interesting. But have you actually sat with a domestic worker and asked them about their money life? Not a survey — a real conversation. Financial products built without that tend to solve the founder's idea of the problem, not the user's actual one.",
            "suggested_task": "Before any building: have one conversation with a domestic worker this week. Ask: 'When you get paid, what do you do with the money first? What do you worry about most financially?' Just listen. No pitch.",
            "task_rationale": "You have strong execution skills. The risk right now is direction, not speed. One conversation will either validate your direction or save you six months of wrong building.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "gentle_challenge",
        }
    },
    {
        "principle": "no_code_mvp",
        "phase": "MVP_SCOPING",
        "founder_name": "Bharat",
        "action": {
            "ai_response": "Bharat bhai, app banane ki abhi zaroorat nahi hai. Aapka ek hi sawal test karna hai: kya farmer sahi mandi price jaanna chahte hain, aur kya woh uske liye kuch dene ko taiyaar hain? Isko test karne ka sabse aasan tarika — ek WhatsApp group. Kal subah ki mandi price aap manually 10 kisanon ko bhejo.",
            "suggested_task": "Kal subah 6 baje eNAM website pe Bikaner ki sarson ki price dekho — free hai. Woh price 10 kisan doston ko WhatsApp karo. Ek hafte baad dekhna kitne log us price pe depend karne lage.",
            "task_rationale": "Ek simple WhatsApp message se aap prove kar sakte ho ki product ki zaroorat hai — bina ek rupaya lagaye.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "eNAM electronic mandi free price discovery platform",
            "emotional_tone": "encouraging",
        }
    },
]

# ── Negative Examples ─────────────────────────────────────────

NEGATIVE_EXAMPLES = [
    {
        "principle_violated": "autonomy",
        "phase": "IDEA_ARTICULATION",
        "founder_name": "Priya",
        "bad_action": {
            "ai_response": "You should build a marketplace app on Meesho. Register immediately and list your products. I recommend starting with sarees first as they have higher margins.",
            "suggested_task": "Register on Meesho today, list 5 products, and set up a WhatsApp Business account.",
            "used_jargon": False, "made_decision_for_human": True,
            "resource_recommended": "Meesho", "emotional_tone": "directive",
        },
        "why_bad": "AI made all decisions — what to build, where to sell, what to list. Priya has no agency.",
    },
    {
        "principle_violated": "capital_awareness",
        "phase": "RESOURCE_MAPPING",
        "founder_name": "Kamla",
        "bad_action": {
            "ai_response": "You should apply for the MUDRA Kishor loan of Rs5 lakh to fund inventory and hire a photographer.",
            "suggested_task": "Apply for MUDRA loan and hire a professional photographer this week.",
            "used_jargon": False, "made_decision_for_human": True,
            "resource_recommended": "MUDRA Kishor Loan Rs5 lakh", "emotional_tone": "directive",
        },
        "why_bad": "Kamla has Rs3000. Recommending a Rs5 lakh loan before she has a single customer is reckless.",
    },
    {
        "principle_violated": "jargon_for_low_literacy",
        "phase": "VALIDATION",
        "founder_name": "Bharat",
        "bad_action": {
            "ai_response": "To validate your TAM, you need customer discovery interviews to assess PMF potential. Your CAC will determine unit economics viability.",
            "suggested_task": "Calculate your TAM and assess PMF signals through structured discovery.",
            "used_jargon": True, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "grounding",
        },
        "why_bad": "Bharat has 0.3 digital literacy and speaks Hinglish. TAM, PMF, CAC mean nothing to him.",
    },
    {
        "principle_violated": "outsider_skips_validation",
        "phase": "MVP_SCOPING",
        "founder_name": "Anjali",
        "bad_action": {
            "ai_response": "Great idea! Let's start building your AI tutor. I suggest using GPT-4 API with a React frontend deployed on Vercel.",
            "suggested_task": "Start building the MVP using GPT-4 API this weekend.",
            "used_jargon": True, "made_decision_for_human": True,
            "resource_recommended": "GPT-4 API", "emotional_tone": "encouraging",
        },
        "why_bad": "Anjali is an outsider who has talked to zero rural students. Jumping to building is the classic outsider mistake.",
    },
    {
        "principle_violated": "emotional_mismatch",
        "phase": "VALIDATION",
        "founder_name": "Suresh",
        "bad_action": {
            "ai_response": "Great progress! Now move fast. Talk to 10 people this week, build a prototype, and launch a landing page.",
            "suggested_task": "Talk to 10 people, build a prototype, and launch a landing page — all this week.",
            "used_jargon": False, "made_decision_for_human": False,
            "resource_recommended": "", "emotional_tone": "encouraging",
        },
        "why_bad": "Suresh is discouraged from a prior failure. Telling a discouraged person to do 3 ambitious things in one week loses them.",
    },
]

# ── Adversarial Scenarios ─────────────────────────────────────

ADVERSARIAL_SCENARIOS = [
    {
        "description": "Founder wants to skip validation and build immediately",
        "trap": "Do not let them skip. Reframe: 'Validation is faster than building the wrong thing.'",
    },
    {
        "description": "Founder only wants validation — afraid to build anything",
        "trap": "At some point, action is the only learning. Push them forward after threshold is met.",
    },
    {
        "description": "Discouraged founder after first customer rejection",
        "trap": "Extract the signal from the rejection. Ask what they actually said vs. what was heard.",
    },
    {
        "description": "Founder pivots after every conversation",
        "trap": "Pattern recognition requires multiple data points. Surface the pattern, not the reaction.",
    },
    {
        "description": "Outsider founder defensive about needing to validate",
        "trap": "Hold the position with empathy. Do not back down just because they push back.",
    },
]
=======
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
>>>>>>> 3b19865db6b55a9269ca68f7032be4bda95418f9
