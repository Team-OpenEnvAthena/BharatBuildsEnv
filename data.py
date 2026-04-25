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