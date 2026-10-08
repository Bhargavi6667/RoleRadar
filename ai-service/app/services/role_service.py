"""
Role-fit analysis.

Given only resume text, work out which job families the candidate suits best
(Frontend, Backend, Sales, ...), score the fit, grade the resume itself, and
produce concrete suggestions.

The scoring is deterministic (skill/keyword evidence), so it works with no API
key. If an OpenAI key is configured, the summary and suggestions are
additionally rewritten by the LLM for a more personal tone (see _llm_refine).
"""
import json
import re
from typing import Dict, List, Any

# --------------------------------------------------------------------------
# Skill catalogue: canonical name -> aliases that count as evidence
# --------------------------------------------------------------------------
SKILLS: Dict[str, List[str]] = {
    # Frontend / web
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "scss"],
    "JavaScript": ["javascript", "js", "es6", "ecmascript"],
    "TypeScript": ["typescript"],
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular", "angularjs"],
    "Vue": ["vue", "vue.js", "vuejs"],
    "Next.js": ["next.js", "nextjs"],
    "Redux": ["redux", "zustand", "context api"],
    "Tailwind / Bootstrap / MUI": ["tailwind", "bootstrap", "material ui", "material-ui", "mui", "chakra"],
    "Responsive Design": ["responsive design", "responsive layout", "mobile-first", "media queries"],
    "Web Accessibility": ["accessibility", "wcag", "aria"],
    "Vite / Webpack": ["vite", "webpack", "babel"],
    "Frontend Testing": ["jest", "cypress", "react testing library", "vitest", "playwright"],
    "Git": ["git", "github", "gitlab", "bitbucket"],
    "REST APIs": ["rest api", "rest apis", "restful", "api integration", "axios", "fetch api"],
    # Backend
    "Java": ["java"],
    "Spring Boot": ["spring boot", "spring framework", "spring mvc", "hibernate", "jpa"],
    "Python": ["python"],
    "Node.js": ["node.js", "nodejs", "node", "express", "express.js", "nestjs"],
    "Django / Flask / FastAPI": ["django", "flask", "fastapi"],
    ".NET / C#": [".net", "c#", "asp.net"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "oracle db", "sql server", "pl/sql"],
    "NoSQL": ["mongodb", "cassandra", "dynamodb", "nosql"],
    "Redis": ["redis", "memcached"],
    "Kafka / Messaging": ["kafka", "rabbitmq", "message queue", "activemq"],
    "Microservices": ["microservices", "microservice", "service-oriented"],
    "System Design": ["system design", "scalable", "scalability", "distributed systems"],
    "GraphQL": ["graphql"],
    "JUnit / Backend Testing": ["junit", "mockito", "pytest", "unit testing", "unit tests"],
    "Authentication / JWT": ["jwt", "oauth", "oauth2", "spring security", "authentication"],
    # DevOps / Cloud
    "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s", "helm", "eks", "aks"],
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "CI/CD": ["ci/cd", "ci cd", "jenkins", "github actions", "gitlab ci", "azure devops", "pipeline automation"],
    "Terraform / IaC": ["terraform", "ansible", "cloudformation", "infrastructure as code", "pulumi"],
    "Linux": ["linux", "ubuntu", "bash", "shell scripting", "unix"],
    "Monitoring": ["prometheus", "grafana", "datadog", "elk", "splunk", "cloudwatch"],
    # Data / ML
    "Pandas / NumPy": ["pandas", "numpy", "scipy"],
    "Machine Learning": ["machine learning", "scikit-learn", "sklearn", "xgboost", "random forest", "regression", "classification"],
    "Deep Learning": ["deep learning", "tensorflow", "pytorch", "keras", "neural network", "neural networks", "cnn", "lstm"],
    "NLP / LLMs": ["nlp", "natural language processing", "llm", "llms", "transformers", "langchain", "openai", "bert"],
    "Statistics": ["statistics", "statistical", "hypothesis testing", "a/b testing", "probability"],
    "Data Visualization": ["power bi", "tableau", "matplotlib", "seaborn", "data visualization", "looker", "plotly"],
    "Excel": ["excel", "ms excel", "advanced excel", "vlookup", "pivot table", "pivot tables"],
    "Data Cleaning / ETL": ["etl", "data cleaning", "data wrangling", "data pipeline", "data pipelines", "airflow", "spark", "pyspark"],
    # Mobile
    "Android": ["android", "android studio", "jetpack compose"],
    "Kotlin": ["kotlin"],
    "iOS / Swift": ["ios", "swift", "swiftui", "xcode", "objective-c"],
    "Flutter / React Native": ["flutter", "dart", "react native"],
    "Mobile App Publishing": ["play store", "app store", "firebase"],
    # QA
    "Manual Testing": ["manual testing", "test cases", "test case", "test plan", "test scenarios", "regression testing", "smoke testing", "uat"],
    "Test Automation": ["selenium", "automation testing", "test automation", "testng", "cucumber", "robot framework", "appium"],
    "API Testing": ["postman", "api testing", "rest assured", "soapui"],
    "Bug Tracking": ["jira", "bugzilla", "bug tracking", "defect tracking", "defect", "bug reports"],
    "SDLC / Agile": ["sdlc", "stlc", "agile", "scrum", "kanban", "sprint"],
    # Design
    "Figma": ["figma"],
    "Wireframing / Prototyping": ["wireframe", "wireframes", "wireframing", "prototype", "prototypes", "prototyping", "adobe xd", "sketch", "balsamiq"],
    "User Research": ["user research", "usability testing", "user interviews", "personas", "user testing"],
    "Design Systems": ["design system", "design systems", "style guide", "component library"],
    "Adobe Creative Suite": ["photoshop", "illustrator", "after effects", "indesign", "canva"],
    "UX Flows": ["user flow", "user flows", "information architecture", "user journey", "journey map", "ux", "ui/ux", "ui design"],
    # Sales
    "Lead Generation": ["lead generation", "lead gen", "prospecting", "cold calling", "cold calls", "cold emailing", "outbound sales"],
    "CRM Tools": ["crm", "salesforce", "hubspot", "zoho crm", "pipedrive", "zoho"],
    "Negotiation & Closing": ["negotiation", "negotiating", "closing deals", "deal closure", "closed deals"],
    "Sales Targets / Revenue": ["sales target", "sales targets", "quota", "revenue growth", "revenue", "exceeded target", "achieved target", "targets achieved"],
    "B2B / B2C Sales": ["b2b", "b2c", "enterprise sales", "inside sales", "field sales", "channel sales", "saas sales"],
    "Pipeline Management": ["sales pipeline", "pipeline management", "funnel", "sales funnel", "forecasting"],
    "Account Management": ["account management", "key accounts", "client relationship", "client relationships", "relationship management", "customer retention", "upselling", "cross-selling", "upsell"],
    "Market Research": ["market research", "competitor analysis", "market analysis", "competitive analysis"],
    "Presentation & Pitching": ["presentation", "presentations", "pitching", "product demo", "product demos", "demos", "proposal", "proposals"],
    # Marketing
    "SEO": ["seo", "search engine optimization", "on-page", "off-page", "keyword research", "backlinks"],
    "Paid Ads": ["google ads", "adwords", "facebook ads", "meta ads", "ppc", "paid campaigns", "linkedin ads"],
    "Analytics": ["google analytics", "ga4", "analytics", "mixpanel", "google search console"],
    "Social Media": ["social media", "instagram", "facebook", "linkedin", "twitter", "youtube", "community management"],
    "Content Marketing": ["content marketing", "content creation", "content strategy", "blogging", "blog", "copywriting", "copywriter"],
    "Email Marketing": ["email marketing", "mailchimp", "newsletter", "email campaigns", "drip campaigns", "marketing automation"],
    "Campaigns & Branding": ["campaign", "campaigns", "branding", "brand strategy", "brand awareness", "digital marketing", "performance marketing"],
    # HR
    "Recruitment": ["recruitment", "talent acquisition", "recruiting", "sourcing", "headhunting", "end-to-end recruitment", "screening"],
    "Interviewing": ["interviewing", "interview scheduling", "interview coordination", "candidate evaluation", "shortlisting"],
    "Onboarding": ["onboarding", "induction", "orientation", "joining formalities"],
    "Payroll": ["payroll", "salary processing", "compensation", "benefits administration", "compensation and benefits"],
    "Employee Engagement": ["employee engagement", "employee relations", "employee retention", "engagement activities", "grievance"],
    "HRIS": ["hris", "workday", "sap hr", "darwinbox", "keka", "greythr", "zoho people", "successfactors"],
    "Performance Management": ["performance management", "performance appraisal", "kpi", "kra", "appraisal", "performance reviews"],
    "HR Compliance": ["labour law", "labor law", "compliance", "pf", "esi", "statutory compliance", "hr policies", "hr policy"],
    # Finance
    "Accounting": ["accounting", "bookkeeping", "general ledger", "journal entries", "accounts payable", "accounts receivable", "ledger"],
    "Tally / ERP": ["tally", "tally erp", "tally prime", "sap", "sap fico", "quickbooks", "zoho books", "oracle financials", "erp"],
    "GST & Taxation": ["gst", "taxation", "tds", "income tax", "tax filing", "tax returns", "direct tax", "indirect tax"],
    "Financial Reporting": ["financial reporting", "financial statements", "balance sheet", "p&l", "profit and loss", "mis reports", "mis", "trial balance"],
    "Budgeting & Forecasting": ["budgeting", "budget", "forecasting", "variance analysis", "fp&a", "cost control"],
    "Audit": ["audit", "auditing", "internal audit", "statutory audit", "audit compliance"],
    "Reconciliation": ["reconciliation", "bank reconciliation", "reconciliations"],
    "Financial Analysis": ["financial analysis", "financial modeling", "financial modelling", "valuation", "ratio analysis", "dcf"],
    # Customer support
    "Customer Service": ["customer service", "customer support", "customer care", "client support", "customer queries", "customer satisfaction", "csat"],
    "Ticketing Tools": ["zendesk", "freshdesk", "servicenow", "ticketing", "helpdesk", "help desk", "intercom", "jira service desk"],
    "Communication": ["communication", "communication skills", "verbal communication", "written communication", "email support", "chat support"],
    "Troubleshooting": ["troubleshooting", "issue resolution", "problem solving", "problem-solving", "root cause", "technical support"],
    "Call Handling": ["call handling", "inbound calls", "outbound calls", "voice process", "call center", "call centre", "bpo", "telecalling"],
    "SLA & Escalation": ["sla", "escalation", "escalations", "first call resolution", "fcr", "aht", "ticket resolution"],
    "Complaint Handling": ["complaint handling", "complaints", "conflict resolution", "customer retention", "service recovery"],
}

# --------------------------------------------------------------------------
# Role profiles: core skills carry most of the score, nice-to-haves the rest
# --------------------------------------------------------------------------
ROLES: Dict[str, Dict[str, Any]] = {
    "frontend": {
        "label": "Frontend Developer",
        "core": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "REST APIs", "Git", "Responsive Design"],
        "nice": ["Angular", "Vue", "Next.js", "Redux", "Tailwind / Bootstrap / MUI", "Frontend Testing", "Web Accessibility", "Vite / Webpack"],
        "titles": ["frontend developer", "front-end developer", "front end developer", "ui developer", "react developer", "web developer", "frontend engineer"],
    },
    "backend": {
        "label": "Backend Developer",
        "core": ["SQL", "REST APIs", "Git", "Microservices", "Authentication / JWT"],
        "any_of": [["Java", "Spring Boot"], ["Python", "Django / Flask / FastAPI"], ["Node.js"], [".NET / C#"]],
        "nice": ["NoSQL", "Redis", "Kafka / Messaging", "Docker", "System Design", "JUnit / Backend Testing", "GraphQL", "AWS"],
        "titles": ["backend developer", "back-end developer", "back end developer", "java developer", "python developer", "software engineer", "api developer", "backend engineer", "node developer"],
    },
    "fullstack": {
        "label": "Full Stack Developer",
        "core": ["JavaScript", "React", "REST APIs", "SQL", "Git", "HTML", "CSS"],
        "any_of": [["Node.js", "Java", "Spring Boot", "Python", "Django / Flask / FastAPI", ".NET / C#"]],
        "nice": ["TypeScript", "Docker", "NoSQL", "Authentication / JWT", "Microservices", "AWS", "CI/CD", "Next.js"],
        "titles": ["full stack developer", "full-stack developer", "fullstack developer", "mern", "full stack engineer", "mean stack"],
    },
    "devops": {
        "label": "DevOps / Cloud Engineer",
        "core": ["Docker", "Kubernetes", "CI/CD", "Linux", "Git"],
        "any_of": [["AWS", "Azure", "GCP"]],
        "nice": ["Terraform / IaC", "Monitoring", "Python", "Microservices"],
        "titles": ["devops engineer", "cloud engineer", "site reliability", "sre", "platform engineer", "cloud administrator"],
    },
    "data": {
        "label": "Data Scientist / ML Engineer",
        "core": ["Python", "Pandas / NumPy", "Machine Learning", "SQL", "Statistics", "Data Visualization"],
        "nice": ["Deep Learning", "NLP / LLMs", "Data Cleaning / ETL", "Excel", "Git"],
        "titles": ["data scientist", "data analyst", "machine learning engineer", "ml engineer", "ai engineer", "data engineer", "business analyst"],
    },
    "mobile": {
        "label": "Mobile App Developer",
        "core": ["Git", "REST APIs", "Mobile App Publishing"],
        "any_of": [["Android", "Kotlin", "iOS / Swift", "Flutter / React Native"]],
        "nice": ["Kotlin", "Android", "iOS / Swift", "Flutter / React Native", "Java"],
        "titles": ["android developer", "ios developer", "mobile developer", "flutter developer", "react native developer", "mobile app developer"],
    },
    "qa": {
        "label": "QA / Test Engineer",
        "core": ["Manual Testing", "Test Automation", "Bug Tracking", "SDLC / Agile", "API Testing"],
        "nice": ["SQL", "Java", "Python", "CI/CD", "Git"],
        "titles": ["qa engineer", "test engineer", "software tester", "quality assurance", "sdet", "automation tester", "qa analyst"],
    },
    "uiux": {
        "label": "UI / UX Designer",
        "core": ["Figma", "Wireframing / Prototyping", "User Research", "UX Flows", "Design Systems"],
        "nice": ["Adobe Creative Suite", "HTML", "CSS", "Web Accessibility"],
        "titles": ["ui/ux designer", "ux designer", "ui designer", "product designer", "visual designer", "graphic designer", "interaction designer"],
    },
    "sales": {
        "label": "Sales / Business Development",
        "core": ["Lead Generation", "CRM Tools", "Negotiation & Closing", "Sales Targets / Revenue", "Pipeline Management", "Account Management"],
        "nice": ["B2B / B2C Sales", "Presentation & Pitching", "Market Research", "Communication", "Excel"],
        "titles": ["sales executive", "sales manager", "business development", "bdm", "bde", "account executive", "sales representative", "inside sales", "relationship manager", "sales associate"],
    },
    "marketing": {
        "label": "Digital Marketing",
        "core": ["SEO", "Paid Ads", "Analytics", "Social Media", "Content Marketing", "Campaigns & Branding"],
        "nice": ["Email Marketing", "Market Research", "Adobe Creative Suite", "Excel", "CRM Tools"],
        "titles": ["digital marketing", "marketing executive", "seo specialist", "content writer", "social media manager", "marketing manager", "performance marketer", "growth marketer"],
    },
    "hr": {
        "label": "HR / Talent Acquisition",
        "core": ["Recruitment", "Interviewing", "Onboarding", "Employee Engagement", "HRIS", "Performance Management"],
        "nice": ["Payroll", "HR Compliance", "Communication", "Excel"],
        "titles": ["hr executive", "hr manager", "hr generalist", "talent acquisition", "recruiter", "hr recruiter", "human resources", "hr associate"],
    },
    "finance": {
        "label": "Finance / Accounting",
        "core": ["Accounting", "Tally / ERP", "GST & Taxation", "Financial Reporting", "Reconciliation", "Excel"],
        "nice": ["Budgeting & Forecasting", "Audit", "Financial Analysis", "Analytics"],
        "titles": ["accountant", "finance executive", "financial analyst", "accounts executive", "auditor", "chartered accountant", "finance manager", "accounts assistant"],
    },
    "support": {
        "label": "Customer Support",
        "core": ["Customer Service", "Ticketing Tools", "Communication", "Troubleshooting", "SLA & Escalation", "Complaint Handling"],
        "nice": ["Call Handling", "CRM Tools", "Excel"],
        "titles": ["customer support", "customer service executive", "customer care", "support engineer", "technical support", "helpdesk", "customer success", "process associate"],
    },
}

SECTION_PATTERNS = {
    "summary": r"^\s*(professional\s+summary|summary|career\s+objective|objective|profile|about\s+me)\b",
    "skills": r"^\s*(technical\s+skills|key\s+skills|core\s+competencies|skills|skill\s+set|technologies)\b",
    "experience": r"^\s*(work\s+experience|professional\s+experience|experience|employment|internships?|work\s+history)\b",
    "education": r"^\s*(education|academics?|academic\s+qualifications?|qualifications?)\b",
    "projects": r"^\s*(projects?|academic\s+projects?|personal\s+projects?|key\s+projects?)\b",
    "certifications": r"^\s*(certifications?|certificates?|courses|achievements|awards)\b",
}

ACTION_VERBS = [
    "built", "developed", "designed", "led", "managed", "created", "implemented", "launched", "improved",
    "increased", "reduced", "achieved", "delivered", "optimized", "optimised", "automated", "negotiated",
    "generated", "coordinated", "analyzed", "analysed", "established", "streamlined", "closed", "handled",
    "resolved", "conducted", "organized", "organised", "trained", "mentored", "migrated", "integrated",
]


def _compile(aliases: List[str]) -> "re.Pattern":
    parts = []
    for a in aliases:
        esc = re.escape(a).replace(r"\ ", r"\s+")
        parts.append(esc)
    return re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(parts) + r")(?![A-Za-z0-9])", re.IGNORECASE)


_SKILL_RE = {name: _compile(aliases) for name, aliases in SKILLS.items()}
_TITLE_RE = {rid: _compile(r["titles"]) for rid, r in ROLES.items()}
_SECTION_RE = {k: re.compile(v, re.IGNORECASE | re.MULTILINE) for k, v in SECTION_PATTERNS.items()}


def detect_skills(text: str) -> Dict[str, int]:
    """Return {skill: mention_count} for every catalogue skill found in the text."""
    found = {}
    for name, rx in _SKILL_RE.items():
        n = len(rx.findall(text))
        if n:
            found[name] = n
    return found


def _score_role(rid: str, found: Dict[str, int], text: str) -> Dict[str, Any]:
    prof = ROLES[rid]
    core = prof["core"]
    nice = prof["nice"]
    any_groups = prof.get("any_of", [])

    matched_core = [s for s in core if s in found]
    missing_core = [s for s in core if s not in found]

    # "any_of" groups: satisfied if at least one member is present (e.g. any backend language)
    group_hits = 0
    for group in any_groups:
        hit = [s for s in group if s in found]
        if hit:
            group_hits += 1
            if hit[0] not in matched_core:
                matched_core.append(hit[0])
        else:
            missing_core.append(" / ".join(group[:3]))
    core_total = len(core) + len(any_groups)
    core_cov = (len([s for s in core if s in found]) + group_hits) / core_total if core_total else 0

    matched_nice = [s for s in nice if s in found]
    nice_cov = len(matched_nice) / len(nice) if nice else 0

    title_hits = len(_TITLE_RE[rid].findall(text))
    title_part = min(title_hits, 3) / 3

    skills_part = 0.75 * core_cov + 0.25 * nice_cov
    raw = 0.8 * skills_part + 0.2 * title_part
    score = int(round(min(98, raw / 0.85 * 100)))

    # de-duplicate, keep order
    matched = list(dict.fromkeys(matched_core + matched_nice))
    return {
        "role_id": rid,
        "role": prof["label"],
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing_core,
        "missing_nice": [s for s in nice if s not in found],
    }


def grade_resume(text: str) -> Dict[str, Any]:
    """Score the resume document itself (structure, contact info, impact), 0-100."""
    words = len(text.split())
    has = {k: bool(rx.search(text)) for k, rx in _SECTION_RE.items()}
    email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
    phone = any(10 <= len(re.sub(r"\D", "", m)) <= 13 for m in re.findall(r"\+?\d[\d\s().-]{8,}\d", text))
    links = bool(re.search(r"linkedin\.com|github\.com|portfolio|behance\.net", text, re.IGNORECASE))
    numbers = len(re.findall(r"\d+\s?%|\$\s?\d|₹\s?\d|\b\d+\+?\s?(?:users|clients|customers|leads|projects|members|candidates|tickets|hires|accounts)\b|\b\d{2,}\b", text))
    verbs = sum(1 for v in ACTION_VERBS if re.search(r"\b" + v + r"\b", text, re.IGNORECASE))

    checks = [
        ("Email address", email, 8, "Add a professional email address at the top."),
        ("Phone number", phone, 5, "Add a phone number so recruiters can reach you."),
        ("LinkedIn / GitHub / portfolio link", links, 7, "Add your LinkedIn (and GitHub or portfolio, if relevant)."),
        ("Summary / objective", has["summary"], 10, "Add a 2-3 line summary that names your target role and strongest skills."),
        ("Skills section", has["skills"], 15, "Add a dedicated Skills section so recruiters and ATS filters can find your keywords."),
        ("Experience / internships", has["experience"], 15, "Add an Experience or Internships section, even short ones, with what you did and achieved."),
        ("Education", has["education"], 10, "Add an Education section with degree, institution and year."),
        ("Projects", has["projects"], 10, "Add 2-3 projects with the technologies used and the outcome."),
        ("Quantified results", numbers >= 4, 10, "Quantify your impact: numbers, percentages, targets hit, users served."),
        ("Action verbs", verbs >= 5, 5, "Start bullets with strong verbs like Built, Led, Reduced, Delivered."),
        ("Reasonable length", 150 <= words <= 1100, 5, "Aim for 1-2 pages. Yours looks " + ("too short" if words < 150 else "too long") + "."),
    ]
    total = sum(w for _, _, w, _ in checks)
    earned = sum(w for _, ok, w, _ in checks if ok)
    return {
        "score": int(round(100 * earned / total)),
        "checks": [{"label": l, "passed": bool(ok), "tip": "" if ok else tip} for l, ok, _, tip in checks],
        "word_count": words,
    }


def _fit_label(score: int) -> str:
    if score >= 75:
        return "Strong fit"
    if score >= 55:
        return "Good fit"
    if score >= 35:
        return "Partial fit"
    return "Weak fit"


def _build_suggestions(best: Dict, second: Dict, quality: Dict, found: Dict[str, int]) -> List[Dict[str, str]]:
    sugg: List[Dict[str, str]] = []
    role = best["role"]

    if best["score"] < 35:
        sugg.append({
            "category": "Positioning", "priority": "High",
            "text": "Your resume doesn't clearly signal any one role yet. Add a headline and a 2-3 line summary naming the role you're targeting, "
                    "and list the tools and skills for it in a Skills section."
        })

    if best["missing_skills"]:
        miss = ", ".join(best["missing_skills"][:5])
        sugg.append({
            "category": "Skills gap", "priority": "High",
            "text": f"For {role} roles, these core skills aren't visible in your resume: {miss}. "
                    "If you've used any of them, add them to your Skills section and to project or experience bullets. "
                    "If not, they're the best things to learn next."
        })

    if best.get("missing_nice"):
        nice = ", ".join(best["missing_nice"][:4])
        sugg.append({
            "category": "Stand out", "priority": "Medium",
            "text": f"Nice-to-have skills that would strengthen your {role} profile: {nice}."
        })

    for chk in quality["checks"]:
        if not chk["passed"]:
            pri = "High" if chk["label"] in ("Skills section", "Experience / internships", "Quantified results", "Summary / objective") else "Medium"
            sugg.append({"category": "Resume quality", "priority": pri, "text": chk["tip"]})

    if second and second["score"] >= 40 and best["score"] - second["score"] <= 10:
        sugg.append({
            "category": "Alternate path", "priority": "Low",
            "text": f"You're almost as strong a match for {second['role']} ({second['score']}%). "
                    "Keep a tailored version of your resume for each role and lead with the matching skills."
        })

    # skills mentioned only once are weakly evidenced
    thin = [s for s in best["matched_skills"] if found.get(s, 0) == 1][:4]
    if thin:
        sugg.append({
            "category": "Evidence", "priority": "Medium",
            "text": f"{', '.join(thin)} appear only once in your resume. Back them up with a project or work bullet showing how you used them."
        })

    order = {"High": 0, "Medium": 1, "Low": 2}
    sugg.sort(key=lambda s: order[s["priority"]])
    return sugg


def analyze_role_fit(text: str, llm_client=None, model: str = "") -> Dict[str, Any]:
    found = detect_skills(text)
    scored = sorted((_score_role(rid, found, text) for rid in ROLES), key=lambda r: r["score"], reverse=True)
    best, second = scored[0], scored[1]
    quality = grade_resume(text)

    suggestions = _build_suggestions(best, second, quality, found)
    low_signal = best["score"] < 15
    if low_signal:
        summary = ("We couldn't find enough role-specific skills or keywords to place this resume confidently. "
                   f"The closest match was {best['role']}, but treat that score as low-confidence.")
    else:
        summary = (
            f"Your resume is a {_fit_label(best['score']).lower()} for {best['role']} roles ({best['score']}%). "
            + (f"Strongest evidence: {', '.join(best['matched_skills'][:5])}." if best["matched_skills"] else "")
        )

    result = {
        "best_role_id": best["role_id"],
        "best_role": best["role"],
        "overall_score": best["score"],
        "fit_label": _fit_label(best["score"]),
        "summary": summary,
        "low_signal": low_signal,
        "role_scores": [
            {k: r[k] for k in ("role_id", "role", "score", "matched_skills", "missing_skills")} for r in scored[:6]
        ],
        "matched_skills": best["matched_skills"],
        "missing_skills": best["missing_skills"],
        "detected_skills": sorted(found, key=lambda s: -found[s]),
        "resume_quality_score": quality["score"],
        "quality_checks": quality["checks"],
        "suggestions": suggestions,
        "ai_enhanced": False,
    }

    if llm_client is not None:
        _llm_refine(result, text, llm_client, model)
    return result


def _llm_refine(result: Dict[str, Any], text: str, client, model: str) -> None:
    """Optionally rewrite summary + suggestions with the LLM. Never raises."""
    try:
        prompt = (
            "You are a career coach. A rule-based engine analysed a resume.\n"
            f"Best-fit role: {result['best_role']} ({result['overall_score']}%).\n"
            f"Matched skills: {result['matched_skills']}\nMissing core skills: {result['missing_skills']}\n"
            f"Resume quality score: {result['resume_quality_score']}/100.\n\n"
            "Using ONLY facts present in the resume text below, return JSON: "
            '{"summary": "2 sentences", "suggestions": [{"category": "...", "priority": "High|Medium|Low", "text": "..."}]} '
            "with 5-7 specific, actionable suggestions. Do not invent experience.\n\nRESUME:\n" + text[:9000]
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "Return only valid JSON."}, {"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        data = json.loads(resp.choices[0].message.content)
        sugg = [
            s for s in data.get("suggestions", [])
            if isinstance(s, dict) and s.get("text") and s.get("priority") in ("High", "Medium", "Low")
        ]
        if data.get("summary") and sugg:
            result["summary"] = data["summary"]
            result["suggestions"] = [{"category": s.get("category", "Tip"), "priority": s["priority"], "text": s["text"]} for s in sugg]
            result["ai_enhanced"] = True
    except Exception:
        pass  # keep rule-based output
