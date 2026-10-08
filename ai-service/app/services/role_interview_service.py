"""
Role-based interview practice.

* generate_questions(): curated questions for the role, plus questions built from
  the skills found / missing in the person's resume. If an OpenAI client is
  available, tailored AI questions are added on top.
* evaluate_answer(): AI feedback when a client is available, otherwise a basic
  checklist (length, structure, specifics, results). The fallback does NOT judge
  technical correctness, and the UI says so.
"""
import json
import re
from typing import Any, Dict, List

from app.services.role_service import ROLES, detect_skills

# (category, difficulty, question, tip)
T, S = "Technical", "Scenario"
E, M, H = "Easy", "Medium", "Hard"

BANK: Dict[str, List[tuple]] = {
    "frontend": [
        (T, E, "What is the difference between `let`, `const` and `var` in JavaScript?", "Cover scope, hoisting and reassignment, with a short example."),
        (T, M, "Explain the CSS box model and how `box-sizing: border-box` changes it.", "Mention content, padding, border, margin and why border-box simplifies layouts."),
        (T, M, "How does the virtual DOM work in React, and why does it help performance?", "Explain diffing and batching, and that it avoids unnecessary real-DOM updates."),
        (T, M, "When would you use `useEffect`, `useMemo` and `useCallback`?", "Give one real use for each and mention dependency arrays."),
        (T, M, "How do you make a web page responsive?", "Media queries, flexbox/grid, relative units, mobile-first approach."),
        (T, H, "How would you improve the load time of a slow React application?", "Code splitting, lazy loading, memoisation, image optimisation, bundle analysis."),
        (S, M, "A page works in Chrome but the layout breaks in Safari. How do you debug it?", "Reproduce, check DevTools, vendor prefixes, feature support (caniuse), then fix and test."),
        (T, M, "What is the difference between state and props, and where should shared state live?", "Lifting state up, context, or a state library depending on scale."),
    ],
    "backend": [
        (T, E, "What is the difference between PUT and PATCH in a REST API?", "Full replacement vs partial update, and idempotency."),
        (T, M, "How do database indexes work, and when can they hurt performance?", "Faster reads, slower writes, extra storage, low-selectivity columns."),
        (T, M, "How would you secure a REST API?", "Authentication (JWT/OAuth), authorisation, HTTPS, input validation, rate limiting."),
        (T, M, "Explain the N+1 query problem and how to fix it.", "Describe the symptom, then joins/fetch joins/batching."),
        (T, H, "How would you design a URL shortener that handles millions of requests a day?", "ID generation, storage, caching, read-heavy scaling, collisions."),
        (T, M, "What are the pros and cons of microservices compared with a monolith?", "Scaling and independence vs operational complexity and network failures."),
        (S, M, "An API endpoint suddenly becomes slow in production. How do you investigate?", "Metrics/logs, slow query analysis, profiling, recent changes, caching."),
        (T, M, "What is a database transaction, and what do ACID properties mean?", "Atomicity, consistency, isolation, durability with a bank-transfer example."),
    ],
    "fullstack": [
        (T, M, "Walk me through what happens from a user clicking 'Submit' in a form to data being saved in the database.", "Frontend event, API call, validation, backend logic, DB write, response, UI update."),
        (T, M, "How do you handle authentication end to end in a full stack app?", "Login, token/session storage, protected routes, backend verification."),
        (T, M, "How do you manage CORS issues between a React frontend and an API?", "Explain the browser rule and server-side allowed origins or a proxy."),
        (T, M, "When would you choose SQL over NoSQL for a project?", "Relational data and transactions vs flexible schema and horizontal scale."),
        (T, H, "How would you structure a project so frontend and backend can be developed and deployed independently?", "API contracts, environment config, CI/CD, versioning."),
        (S, M, "Users report data on screen is stale after an update. Where do you look?", "Caching, state management, API response, race conditions."),
        (T, E, "What is REST, and how is it different from GraphQL?", "Resource endpoints vs single query endpoint and flexible fields."),
    ],
    "devops": [
        (T, E, "What is the difference between a Docker image and a container?", "Image is the template, container is a running instance."),
        (T, M, "Explain what a CI/CD pipeline does and the stages you would include.", "Build, test, scan, package, deploy, with approvals and rollbacks."),
        (T, M, "How does Kubernetes keep an application available when a pod crashes?", "Deployments, ReplicaSets, health probes, self-healing."),
        (T, M, "What is Infrastructure as Code and why is it useful?", "Repeatability, versioning, review, drift detection (Terraform example)."),
        (S, H, "Production is down after a deployment. What are your first steps?", "Roll back first, communicate, check logs/metrics, then do a post-mortem."),
        (T, M, "How do you monitor a service, and what would you alert on?", "Metrics, logs, traces; latency, error rate, saturation; avoid noisy alerts."),
        (T, M, "How do you manage secrets such as database passwords?", "Secret managers, environment injection, never in Git, rotation."),
    ],
    "data": [
        (T, E, "What is the difference between supervised and unsupervised learning?", "Labelled vs unlabelled data with one example of each."),
        (T, M, "How do you handle missing values in a dataset?", "Understand why they are missing, then drop, impute or flag, and explain the trade-offs."),
        (T, M, "Explain overfitting and how you would prevent it.", "Train vs validation gap; regularisation, more data, cross-validation, simpler model."),
        (T, M, "Which metrics would you use for an imbalanced classification problem?", "Precision, recall, F1, PR-AUC instead of plain accuracy."),
        (T, M, "Write or describe a SQL query to find the top 3 customers by revenue per region.", "Aggregation plus a window function such as RANK or ROW_NUMBER."),
        (S, H, "Your model performs well offline but poorly in production. Why might that be?", "Data drift, leakage, training/serving skew, monitoring."),
        (T, M, "How do you explain a model's results to a non-technical stakeholder?", "Business outcome first, simple visuals, uncertainty and limits."),
    ],
    "mobile": [
        (T, E, "What is the Android Activity lifecycle (or iOS view controller lifecycle)?", "Name the main callbacks and what to do in each."),
        (T, M, "How do you handle different screen sizes and orientations?", "Responsive layouts, constraints, resource qualifiers, testing on devices."),
        (T, M, "How would you store data locally and sync it with a server?", "Local DB/cache, sync strategy, conflict handling, offline mode."),
        (T, M, "How do you avoid memory leaks in a mobile app?", "Lifecycle awareness, weak references, cancelling work, profiling tools."),
        (T, H, "How would you design an app that works offline and syncs when back online?", "Local-first storage, queue of changes, retries, conflict resolution."),
        (S, M, "Users say the app is slow to start. How do you improve startup time?", "Profile, defer heavy work, lazy init, reduce main-thread work."),
    ],
    "qa": [
        (T, E, "What is the difference between smoke, sanity and regression testing?", "Define each with when you would run it."),
        (T, M, "How do you decide which test cases to automate?", "Repetitive, stable, high-value, data-driven tests; avoid unstable UI."),
        (T, M, "Write test cases for a login page.", "Valid/invalid input, empty fields, lockout, boundary, security, accessibility."),
        (S, M, "You find a bug the developer says is 'not a bug'. What do you do?", "Reproduce, check requirements, show evidence and impact, discuss calmly."),
        (T, M, "What makes a good bug report?", "Title, steps, expected vs actual, environment, severity, evidence."),
        (T, H, "How would you design a test automation framework from scratch?", "Structure (page objects), data handling, reporting, CI integration, maintainability."),
        (T, M, "How do you test an API?", "Status codes, payloads, auth, edge cases, performance, tools like Postman."),
    ],
    "uiux": [
        (T, E, "Walk me through your design process from problem to final design.", "Research, define, ideate, prototype, test, iterate."),
        (T, M, "How do you conduct user research when you have a small budget?", "Interviews, quick surveys, usability tests with 5 users, analytics."),
        (T, M, "How do you make a design accessible?", "Contrast, text size, keyboard use, alt text, don't rely on colour alone."),
        (S, M, "A stakeholder dislikes your design but users tested well. What do you do?", "Use evidence, listen to concerns, align on goals, propose a test."),
        (T, M, "What is a design system and why use one?", "Consistency, speed, shared components and tokens."),
        (T, H, "How would you redesign the checkout flow of an e-commerce app to reduce drop-offs?", "Find drop-off points, reduce steps and friction, test variants, measure."),
    ],
    "sales": [
        (S, E, "Sell me this pen.", "Ask about their needs first, then link features to a benefit."),
        (T, M, "How do you qualify a lead?", "Budget, authority, need, timeline (BANT) or a similar framework."),
        (S, M, "A prospect says your price is too high. How do you respond?", "Understand the objection, restate value, compare cost of inaction, offer options."),
        (T, M, "Describe your sales process from first contact to closing.", "Prospecting, discovery, demo/pitch, objection handling, close, follow-up."),
        (S, H, "You are far behind your monthly target with two weeks left. What do you do?", "Prioritise the pipeline, follow up warm leads, ask for referrals, be realistic."),
        (T, M, "How do you keep customers after closing the deal?", "Onboarding, regular check-ins, upselling, solving problems early."),
        (T, E, "Which CRM tools have you used, and how did you use them day to day?", "Name the tool, pipeline stages, reminders, reports."),
    ],
    "marketing": [
        (T, E, "What is the difference between SEO and SEM?", "Organic vs paid search, with when you would use each."),
        (T, M, "How do you measure the success of a campaign?", "Goal-linked KPIs: CTR, conversion rate, CAC, ROAS, revenue."),
        (T, M, "How would you plan a social media campaign for a new product launch?", "Audience, channels, content plan, schedule, budget, metrics."),
        (S, M, "Your ad campaign has a high click rate but few conversions. What do you check?", "Landing page, targeting, offer match, tracking, page speed."),
        (T, M, "How do you do keyword research?", "Tools, intent, volume vs difficulty, competitor gaps."),
        (T, H, "You have a limited budget. How do you split it across channels?", "Test small, double down on what works, track cost per result."),
    ],
    "hr": [
        (T, E, "Walk me through the end-to-end recruitment process you follow.", "Requirement, sourcing, screening, interviews, offer, onboarding."),
        (S, M, "A hiring manager rejects every candidate you send. What do you do?", "Clarify requirements, calibrate with examples, get feedback, adjust sourcing."),
        (T, M, "How do you source candidates for hard-to-fill roles?", "LinkedIn, referrals, communities, talent pools, employer branding."),
        (S, M, "An employee complains about a manager. How do you handle it?", "Listen, confidentiality, document, investigate fairly, follow policy."),
        (T, M, "How do you improve employee engagement and retention?", "Surveys, recognition, growth paths, feedback, exit interviews."),
        (T, M, "What basic labour-law and compliance points should an HR executive know?", "Contracts, PF/ESI, leave, termination process, record keeping."),
    ],
    "finance": [
        (T, E, "What is the difference between a balance sheet and a profit and loss statement?", "Position at a point in time vs performance over a period."),
        (T, M, "How do you perform a bank reconciliation, and what do you do with differences?", "Match entries, find timing differences and errors, adjust, document."),
        (T, M, "Explain GST input tax credit with a simple example.", "Tax paid on purchases offsets tax collected on sales, with conditions."),
        (T, M, "How do you ensure accuracy when closing the month-end books?", "Checklists, reconciliations, accruals, review, variance analysis."),
        (S, H, "You find a large unexplained difference in the ledger right before an audit. What do you do?", "Trace transactions, involve seniors, document, correct properly, never hide it."),
        (T, M, "Which accounting software and Excel functions do you use most?", "Tally/SAP, VLOOKUP/XLOOKUP, pivot tables, with a real example."),
    ],
    "support": [
        (S, E, "A customer is angry about a delayed order. How do you respond?", "Listen, apologise, take ownership, give a clear next step and timeline."),
        (S, M, "You do not know the answer to a customer's question. What do you do?", "Be honest, find the answer or escalate, follow up as promised."),
        (T, M, "How do you prioritise when you have many tickets open at once?", "Severity and SLA, customer impact, quick wins, clear communication."),
        (T, M, "What does a good first-contact resolution look like?", "Understand fully, solve or document, confirm resolution."),
        (S, H, "A customer keeps contacting you about the same issue. What now?", "Find the root cause, escalate to the right team, give one owner, follow up."),
        (T, E, "Which ticketing or helpdesk tools have you used?", "Name the tool, how you tracked, tagged and closed tickets."),
    ],
}

# Questions every candidate may be asked
BEHAVIOURAL = [
    ("Behavioural", E, "Tell me about yourself.", "Keep it to about a minute: present role/studies, key skills, why this role."),
    ("Behavioural", E, "Why do you want this role, and why this company?", "Link your skills and goals to the role; show you researched the company."),
    ("Behavioural", M, "Tell me about a time you faced a difficult problem and how you solved it.", "Use STAR: Situation, Task, Action, Result, and include numbers if you can."),
    ("Behavioural", M, "Describe a time you disagreed with a teammate or manager.", "Show respect, listening and a constructive outcome."),
    ("Behavioural", M, "Tell me about a mistake you made and what you learned.", "Own it, explain the fix, and what you now do differently."),
    ("Behavioural", M, "Describe a time you worked under a tight deadline.", "How you prioritised, communicated, and what you delivered."),
    ("Behavioural", E, "What are your strengths and weaknesses?", "Pick real ones; for weaknesses explain what you are doing to improve."),
    ("Behavioural", E, "Where do you see yourself in three years?", "Show growth in the same field, not a vague answer."),
]


def _qid(prefix: str, i: int) -> str:
    return f"{prefix}-{i + 1}"


def _skill_questions(role: str, matched: List[str], missing: List[str]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    trivial = {"Git", "HTML", "CSS", "Excel", "Communication", "SDLC / Agile", "Linux"}
    ordered = [s for s in matched if s not in trivial] + [s for s in matched if s in trivial]
    for s in ordered[:4]:
        out.append({
            "category": "From your resume", "difficulty": M,
            "question": f"You list {s} on your resume. Describe a project where you used it and one challenge you faced.",
            "tip": "Pick one real project: what you built, your part, a problem, how you solved it, and the result.",
        })
    for s in missing[:3]:
        out.append({
            "category": "Skill gap", "difficulty": M,
            "question": f"{s} is commonly expected for {role} roles but isn't on your resume. How would you get up to speed on it?",
            "tip": "Be honest. Name a learning plan, related experience you already have, and a quick first project.",
        })
    return out


def _fallback_questions(role_id: str, role: str, matched: List[str], missing: List[str]) -> List[Dict[str, str]]:
    rows = [{"category": c, "difficulty": d, "question": q, "tip": t} for c, d, q, t in BANK.get(role_id, [])]
    rows = _skill_questions(role, matched, missing) + rows + [
        {"category": c, "difficulty": d, "question": q, "tip": t} for c, d, q, t in BEHAVIOURAL
    ]
    return rows


def generate_questions(role_id: str, role: str, matched: List[str], missing: List[str],
                       resume_text: str = "", client=None, model: str = "") -> Dict[str, Any]:
    role = role or ROLES.get(role_id, {}).get("label", role_id)
    rows = _fallback_questions(role_id, role, matched or [], missing or [])
    ai_used = False

    if client is not None:
        try:
            prompt = (
                f"Generate 8 interview questions for a {role} candidate. Mix technical, scenario and behavioural. "
                f"Skills on their resume: {matched}. Skills they lack: {missing}. "
                "Make at least 3 questions refer to the candidate's own listed skills or projects. "
                'Return JSON: {"questions": [{"category": "Technical|Scenario|Behavioural|From your resume|Skill gap", '
                '"difficulty": "Easy|Medium|Hard", "question": "...", "tip": "one-sentence hint on how to answer"}]}\n\n'
                "RESUME (excerpt):\n" + (resume_text or "")[:6000]
            )
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": "Return only valid JSON."}, {"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.6,
            )
            data = json.loads(resp.choices[0].message.content)
            ai_rows = [
                {"category": str(q.get("category", "Technical")), "difficulty": q.get("difficulty", M) if q.get("difficulty") in (E, M, H) else M,
                 "question": str(q["question"]), "tip": str(q.get("tip", ""))}
                for q in data.get("questions", []) if isinstance(q, dict) and q.get("question")
            ]
            if ai_rows:
                seen = {r["question"].lower() for r in ai_rows}
                rows = ai_rows + [r for r in rows if r["question"].lower() not in seen]
                ai_used = True
        except Exception:
            pass

    questions = [{"id": _qid("q", i), **r} for i, r in enumerate(rows)]
    return {"role_id": role_id, "role": role, "questions": questions, "ai_generated": ai_used}


# ---------------------------------------------------------------- evaluation
_STAR = {
    "situation": r"\b(situation|context|background|when i was|at my|during)\b",
    "task": r"\b(task|goal|responsib|objective|needed to|had to|asked to)\b",
    "action": r"\b(i (built|created|led|wrote|designed|decided|implemented|fixed|analy[sz]ed|organi[sz]ed|set up|started|reached|contacted|worked))\b",
    "result": r"\b(result|outcome|as a result|improved|reduced|increased|saved|achieved|resolved|delivered|learned)\b",
}
_HEDGES = re.compile(r"\b(i think maybe|not sure|i don't know|i dont know|i guess|kind of|sort of|maybe)\b", re.IGNORECASE)


def _heuristic_feedback(role_id: str, question: str, answer: str) -> Dict[str, Any]:
    words = len(answer.split())
    low = answer.lower()
    star_hits = [k for k, rx in _STAR.items() if re.search(rx, low)]
    has_numbers = bool(re.search(r"\d+\s?%|\b\d{2,}\b|\b\d+\s?(users|clients|customers|hours|days|weeks|months|times|x)\b", low))
    skills = detect_skills(answer)
    hedges = len(_HEDGES.findall(answer))

    score = 2.0
    strengths: List[str] = []
    improve: List[str] = []

    if words >= 120:
        score += 2.5; strengths.append("Good level of detail.")
    elif words >= 60:
        score += 1.5; strengths.append("Reasonable length.")
    elif words >= 30:
        score += 0.5; improve.append("Add more detail: aim for 60-150 words with a specific example.")
    else:
        improve.append("Your answer is very short. Explain your reasoning and give an example.")

    if len(star_hits) >= 3:
        score += 2.0; strengths.append("Clear structure (situation, action, result).")
    elif len(star_hits) >= 1:
        score += 1.0
        improve.append("Structure it as Situation, Task, Action, Result so the interviewer can follow it.")
    else:
        improve.append("Use a clear structure such as STAR (Situation, Task, Action, Result).")

    if has_numbers:
        score += 1.5; strengths.append("You quantified your impact.")
    else:
        improve.append("Add numbers or concrete results (%, time saved, users, targets).")

    if skills:
        score += min(1.5, 0.5 * len(skills))
        strengths.append("Mentions relevant tools/skills: " + ", ".join(list(skills)[:4]) + ".")
    elif role_id in BANK and any(c == T for c, *_ in BANK[role_id]):
        improve.append("Name the specific tools, concepts or methods you would use.")

    if hedges >= 2:
        score -= 1.0; improve.append("Sound more confident: avoid phrases like 'I guess' or 'not sure'.")

    score = round(max(0.0, min(10.0, score)), 1)
    verdict = "Strong answer" if score >= 7.5 else "Decent answer" if score >= 5 else "Needs work"
    return {
        "score": score, "verdict": verdict, "strengths": strengths, "improvements": improve,
        "model_answer_tip": "", "ai_generated": False,
    }


def evaluate_answer(role_id: str, role: str, question: str, answer: str, client=None, model: str = "") -> Dict[str, Any]:
    if client is not None:
        try:
            prompt = (
                f"You are a strict but fair interviewer for a {role} position.\n"
                f"Question: {question}\nCandidate answer: {answer}\n\n"
                'Return JSON: {"score": number 0-10, "verdict": "Strong answer|Decent answer|Needs work", '
                '"strengths": ["..."], "improvements": ["..."], "model_answer_tip": "2-3 sentences on what a strong answer would include"}. '
                "Judge technical correctness and structure. Be specific and concise."
            )
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": "Return only valid JSON."}, {"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            d = json.loads(resp.choices[0].message.content)
            return {
                "score": float(max(0, min(10, d.get("score", 5)))),
                "verdict": str(d.get("verdict", "Decent answer")),
                "strengths": [str(x) for x in d.get("strengths", [])][:5],
                "improvements": [str(x) for x in d.get("improvements", [])][:5],
                "model_answer_tip": str(d.get("model_answer_tip", "")),
                "ai_generated": True,
            }
        except Exception:
            pass
    return _heuristic_feedback(role_id, question, answer)
