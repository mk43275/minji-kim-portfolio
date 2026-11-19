"""Builds every page of the site from the content below.

To update the site:
  1. Edit the CONTENT section in this file.
  2. Run:  python3 build.py
  3. Commit the changed .html files and push. Vercel deploys them as-is (no build step).

Sentences in descriptions are put on separate lines automatically.
"""
import html, os, re
from pathlib import Path

ROOT = Path(__file__).parent

# ============================== CONTENT ==============================

SITE = {
    "name": "Minji Kim",
    "email": "minjik416@gmail.com",
    "linkedin": "https://www.linkedin.com/in/minjikimut",
    "github": "https://github.com/mk43275",
    "cv": "/photo/Minji%20Kim%20CV.pdf",
    "photo": "/photo/Minji%20Headshot.png",
    "headline": "Scalable <em>Responsible</em> AI and Data Systems",  # HTML allowed
    "eyebrow": "AI · Governance · Data",
    "side": ["Enterprise AI Consultant at VIPC.", "Brumley Fellow at the Strauss Center.", "MS Business Analytics at UT Austin."],
    "intro": "I build AI and data systems that work for people, then figure out how to govern them.",
    "about": "I'm an Enterprise AI & Automation Consultant at VIPC, a Brumley Graduate Fellow at the Strauss Center, and an MS Business Analytics student at UT Austin McCombs.",
}

# Projects: first 3 appear on the home page.
PROJECTS = [
    {"slug": "phish-in-the-web", "title": "Phish in the Web", "year": "2024", "tags": ["Security", "ML"],
     "desc": "Explainable phishing detection for non-experts.",
     "stats": [("98%", "accuracy"), ("50 → 13", "features"), ("10K+", "URLs")],
     "problem": "Black-box blockers flag real sites, so people stop trusting the warnings.",
     "did": ["Compared 6+ models on 10K+ labeled URLs", "Cut 50 features to 13 so every flag is explainable", "Built a live URL checker and tested it with real users"],
     "why": "Fewer false alarms means people keep listening to the real ones.",
     "links": []},
    {"slug": "federated-aml", "title": "Federated AI for AML", "year": "2026", "tags": ["Governance", "Research"],
     "desc": "Governing cross-border AI that fights money laundering.",
     "stats": [("4+", "jurisdictions"), ("3", "model setups"), ("CRI", "partner")],
     "problem": "Banks can't share data across borders. Money launderers don't have that problem.",
     "did": ["Comparing AML data-sharing rules across 4+ jurisdictions", "Benchmarking local, central, and federated models", "Drafting a governance framework with the Cyber Risk Institute"],
     "why": "Federated learning keeps data local, but someone still has to be accountable.",
     "links": []},
    {"slug": "revision", "title": "ReVision", "year": "2025", "tags": ["Publication", "ML"],
     "desc": "Privacy-preserving visual instructions. Published at IJCNLP–AACL 2025.",
     "stats": [("AACL", "2025"), ("$7.5K", "research fellowship"), ("VLM", "on-device")],
     "problem": "Visual assistants usually need to see more of your life than the task requires.",
     "did": ["Co-authored a new dataset and VLM baseline", "Rewrote instructions so private details stay private", "Funded by UT's Undergraduate Research Fellowship"],
     "why": "Helpful AI shouldn't require giving up your privacy.",
     "links": [("Read on arXiv", "https://arxiv.org/abs/2502.14780")]},
    {"slug": "research-dashboard", "title": "Researcher Commercialization Dashboard", "year": "2026", "tags": ["Data", "AI"],
     "desc": "Finds Virginia researchers with startup potential.",
     "stats": [("200K+", "publications"), ("AWS", "vector search"), ("VA", "statewide")],
     "problem": "Great university research rarely reaches the investors who could fund it.",
     "did": ["Built vector search over 200K+ publications", "Ranked researchers by commercialization signals", "Shipped it on AWS for VIPC"],
     "why": "Turns academic output into leads people can act on.",
     "links": []},
    {"slug": "robo-caller", "title": "Less Annoying Robo Caller", "year": "2025", "tags": ["ML"],
     "desc": "Hears frustration in a caller's voice and words.",
     "stats": [("+30%", "vs. one mode"), ("7.4K", "audio clips"), ("Live", "prototype")],
     "problem": "Automated phone lines can't tell when a caller is about to hang up angry.",
     "did": ["Fused speech audio with transcribed text", "Trained on 7,400+ labeled clips", "Tested it on live voice input"],
     "why": "Systems that notice emotion can hand people to a human sooner.",
     "links": []},
    {"slug": "safer-pittsburgh", "title": "Safer City for Pittsburgh", "year": "2025", "tags": ["Data"],
     "desc": "Mapped property decay hotspots for the city.",
     "stats": [("100K+", "records merged"), ("4K", "properties"), ("CDO", "presented to")],
     "problem": "The city's property data had gaps too big to plan around.",
     "did": ["Merged 100K+ outside records to fill gaps", "Mapped deterioration hotspots in Power BI", "Presented fixes to the Chief Data Officer"],
     "why": "Better data points inspectors to the blocks that need them.",
     "links": []},
]
PROJECT_FILTERS = ["Governance", "Security", "ML", "Data", "Publication"]

# Writing: kind must be one of WRITING_KINDS. wip=True shows "In the works" and isn't clickable.
WRITING_KINDS = ["Published Technical Paper", "Blog", "Research/Policy Paper"]
WRITING = [
    {"title": "Predicting Weekly Walmart Sales", "kind": "Blog", "date": "", "note": "DL/ML project", "wip": True},
    {"title": "Governing Cross-Border Federated AI for Anti-Money Laundering", "kind": "Research/Policy Paper", "date": "", "note": "Brumley Fellowship", "wip": True},
    {"title": "ReVision: A Dataset and Baseline VLM for Privacy-Preserving Task-Oriented Visual Instruction Rewriting",
     "kind": "Published Technical Paper", "date": "2025", "note": "IJCNLP–AACL 2025", "url": "https://arxiv.org/abs/2502.14780"},
]

# Experience: first 4 appear on the home page.
EXPERIENCE = [
    ("2026 – now", "Enterprise AI & Automation Consultant", "Virginia Innovation Partnership Corporation (VIPC)"),
    ("2026 – now", "Graduate Brumley Fellow", "Strauss Center for International Security and Law"),
    ("2025 – 2026", "AI Systems & Transformation Fellow // Data Operations & Strategy Analyst", "VIPC"),
    ("2024 – 2025", "Data Science Researcher", "UT Austin AI/ML/NLP Labs"),
    ("2024 – 2025", "Cybersecurity Consultant", "Texas Cybersecurity Clinic"),
    ("2025", "SOC Analyst", "UT Regional Security Operations Center"),
    ("2024 – 2025", "Undergraduate Associate Researcher", "UT Austin iSchool Labs"),
    ("2023 – 2024", "Transformation Analyst", "LOE Cosmetics"),
]

EDUCATION = [
    ("May 2027", "MS Business Analytics", "UT Austin, McCombs School of Business"),
    ("Dec 2025", "BS Human-Centered Data Science", "UT Austin · Minors in Risk Management, Programming & Computation"),
]

HONORS = [
    ("2026", "AI Panelist", "American Society for Public Administration"),
    ("2025", "National Security Fellow", "Girl Security"),
    ("2025", "NobleReach AI Scholar", "NobleReach Foundation"),
    ("2025", "Cyber 9/12 Strategy Challenge Semi-Finalist", "Atlantic Council · 4th in Washington, DC and 6th in Austin"),
    ("2024", "Undergraduate Research Fellowship", "UT Austin"),
    ("2023", "University Honors", "UT Austin"),
    ("2023 – 2025", "President, Girls Who Code", "UT Austin · 200+ members"),
    ("2023 – 2025", "President, Informatics Undergraduate Student Council", "UT Austin"),
    ("2025 – now", "Member, Responsible AI Institute", "AI governance, policy, and risk"),
]

COURSES = ["Human-Centered Data Science", "Research Methods for Informatics", "Applied Machine Learning",
           "Deep Learning & Multimodal Systems", "Natural Language Processing", "User Experience Design",
           "Applied Cybersecurity Foundations", "MS Business Analytics coursework (in progress)"]
CERTS = [("Google Cybersecurity Professional Certificate", "Coursera"), ("OS Fundamentals", "Hack The Box")]

SKILLS = [
    ("Programming", "Python · SQL · R · JavaScript · HTML/CSS · Swift · Git · Linux · Docker"),
    ("Data & Cloud", "AWS · Azure · GCP · Snowflake · Spark · Airflow · Elasticsearch · Tableau · Power BI"),
    ("AI / ML", "PyTorch · TensorFlow · scikit-learn · Hugging Face · OpenAI & Anthropic APIs · Gurobi"),
    ("Governance & Security", "Role-based access · Audit logging · Data validation · NIST CSF · FATF guidance"),
]

CAFES = [
    {"name": "Instill Coffee", "loc": "Cedar Park, TX", "stars": 5, "review": "Amazing matcha lattes here and kind workers! Avo toast is great as well!", "images": ["Instill 1.jpg", "Instill 2.jpg"]},
    {"name": "CaPhe.in Coffee", "loc": "Austin, TX", "stars": 4, "review": "Great unique lattes & matchas, but it is so expensive! Worth a try though!", "images": ["Caphein 1.jpg", "Caphein 2.JPG"]},
    {"name": "Caffe Paradiso", "loc": "New York, NY", "stars": 4, "review": "Long line + expensive, but their latte on tap was SO GOOD! Worth a try!", "images": ["Caffe Paradiso.jpg"]},
    {"name": "Soricha Tea & Theater", "loc": "Annandale, VA", "stars": 5, "review": "Lovely cafe! Korean-style lattes, tea, and desserts. So yummy!", "images": ["Soricha 1.jpg", "Soricha 2.jpg", "Soricha 3.jpg"]},
]

# ============================== TEMPLATES ==============================

e = lambda s: html.escape(s, quote=True)
def br(s):  # escape, then one sentence per line
    return re.sub(r"([.!?]) (?=[A-Z])", r"\1<br>", e(s))
img = lambda name: "/photo/cafes/" + name.replace(" ", "%20")

def page(title, active, body, desc=None):
    on = ' class="on"'
    nav = "".join(f'<a href="{href}"{on if key == active else ""}>{label}</a>'
                  for key, href, label in [("home", "/", "Home"), ("projects", "/projects/", "Projects"),
                                           ("writing", "/writing/", "Writing"), ("about", "/about/", "About"),
                                           ("cafes", "/cafes/", "Cafés")])
    full = SITE["name"] if title is None else f"{title} · {SITE['name']}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(full)}</title>
<meta name="description" content="{e(desc or SITE['intro'])}">
<link rel="icon" type="image/png" href="/photo/teaicon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap">
<nav class="top">
  <a class="me" href="/"><img src="{SITE['photo']}" alt="">{SITE['name']}</a>
  <div class="links">{nav}</div>
</nav>
<main>
{body}
</main>
<footer>
  <span>© 2026 {SITE['name']}</span>
  <span><a href="mailto:{SITE['email']}">{SITE['email']}</a> · <a href="{SITE['linkedin']}">LinkedIn</a> · <a href="{SITE['github']}">GitHub</a> · <a href="{SITE['cv']}">CV</a></span>
</footer>
</div>
</body>
</html>
"""

def project_rows(ps):
    return '<div class="rows">' + "".join(
        f'<a class="row" href="/projects/{p["slug"]}/" data-tags="{e(" ".join(p["tags"]))}"><span class="n">{i+1:02d}</span>'
        f'<div><div class="t">{e(p["title"])}</div><div class="d">{br(p["desc"])}</div></div></a>'
        for i, p in enumerate(ps)) + "</div>"

def item_list(rows):
    return '<div class="list">' + "".join(
        f'<div class="item"><span class="dt">{e(d)}</span><span><span class="it">{e(t)}</span><br><span class="sub">{e(s)}</span></span><span></span></div>'
        for d, t, s in rows) + "</div>"

def writing_list(ws):
    out = []
    for w in ws:
        date = '<span class="wip">In the works</span>' if w.get("wip") else e(w["date"])
        arrow = " ↗" if w.get("url") else ""
        inner = (f'<span class="dt">{date}</span><span><span class="it">{e(w["title"])}{arrow}</span><br>'
                 f'<span class="tag">{e(w["kind"])}</span></span><span class="rt">{e(w["note"])}</span>')
        if w.get("url"):
            out.append(f'<a class="item" href="{w["url"]}" data-kind="{e(w["kind"])}">{inner}</a>')
        else:
            out.append(f'<div class="item" data-kind="{e(w["kind"])}">{inner}</div>')
    return '<div class="list">' + "".join(out) + "</div>"

def filter_script(attr):
    return f"""<script>
document.querySelectorAll('.filters').forEach(f => f.addEventListener('click', ev => {{
  const b = ev.target.closest('button'); if (!b) return;
  f.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b));
  const k = b.dataset.f;
  document.querySelectorAll('[data-{attr}]').forEach(el => {{
    el.style.display = (k === 'All' || el.dataset.{attr}.split('|').includes(k) || el.dataset.{attr}.split(' ').includes(k)) ? '' : 'none';
  }});
}}));
</script>"""

def filters(opts):
    return '<div class="filters">' + "".join(
        f'<button class="{"on" if i == 0 else ""}" data-f="{e(o)}">{e(o)}</button>' for i, o in enumerate(["All"] + opts)) + "</div>"

def build():
    pages = {}
    side = "<br>".join(e(s) for s in SITE["side"])
    pages["index.html"] = page(None, "home", f"""
<div class="hero"><div><p class="eyebrow">{e(SITE['eyebrow'])}</p><h1>{SITE['headline']}</h1></div><p class="side">{side}</p></div>
<div class="sec"><h2>Selected projects</h2><a href="/projects/">See all →</a></div>
{project_rows(PROJECTS[:3])}
<div class="sec"><h2>Experience</h2><a href="/about/">Full experience &amp; education →</a></div>
{item_list(EXPERIENCE[:4])}
<div class="sec"><h2>Writing</h2><a href="/writing/">See all →</a></div>
{writing_list(WRITING[:3])}""")

    pages["projects/index.html"] = page("Projects", "projects", f"""
<p class="eyebrow">Projects</p><h1>Things I've built</h1>
{filters(PROJECT_FILTERS)}
{project_rows(PROJECTS)}
{filter_script("tags")}""", "Projects by Minji Kim in AI governance, security, machine learning, and data.")

    for p in PROJECTS:
        stats = "".join(f'<div class="stat"><b>{e(b)}</b><span>{e(l)}</span></div>' for b, l in p["stats"])
        did = "".join(f"<li>{e(x)}</li>" for x in p["did"])
        links = "".join(f'<a class="btn{" p" if i == 0 else ""}" href="{u}">{e(l)} ↗</a>' for i, (l, u) in enumerate(p["links"]))
        pages[f"projects/{p['slug']}/index.html"] = page(p["title"], "projects", f"""
<a class="back" href="/projects/">← All projects</a>
<p class="eyebrow">{e(" · ".join(p["tags"]))} · {e(p["year"])}</p><h1>{e(p["title"])}</h1><p class="lede">{br(p["desc"])}</p>
<div class="stats">{stats}</div>
<div class="three">
  <div><h3>Problem</h3><p>{br(p["problem"])}</p></div>
  <div><h3>What I did</h3><ul>{did}</ul></div>
  <div><h3>Why it matters</h3><p>{br(p["why"])}</p></div>
</div>
{f'<div class="btns">{links}</div>' if links else ''}""", p["desc"])

    pages["writing/index.html"] = page("Writing", "writing", f"""
<p class="eyebrow">Writing</p><h1>Papers &amp; posts</h1><p class="lede">Published research, policy work, and project write-ups.</p>
{filters(WRITING_KINDS)}
{writing_list(WRITING)}
{filter_script("kind")}""", "Papers and posts by Minji Kim.")

    courses = "".join(f'<div class="box"><div class="v">{e(c)}</div></div>' for c in COURSES)
    certs = "".join(f'<div class="box"><div class="k">Certification</div><div class="v">{e(n)}</div><div class="s">{e(i)}</div></div>' for n, i in CERTS)
    skills = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in SKILLS)
    pages["about/index.html"] = page("About", "about", f"""
<p class="eyebrow">About</p><h1>Hi, I'm Minji.</h1>
<p class="lede">{e(SITE['intro'])}<br>{e(SITE['about'])}</p>
<div class="btns"><a class="btn p" href="{SITE['cv']}">Download CV (PDF)</a><a class="btn" href="mailto:{SITE['email']}">Email me</a></div>
<div class="sec"><h2>Experience</h2></div>
{item_list(EXPERIENCE)}
<div class="sec"><h2>Education</h2></div>
{item_list(EDUCATION)}
<div class="sec"><h2>Honors &amp; involvement</h2></div>
{item_list(HONORS)}
<div class="sec"><h2>Courses &amp; certifications</h2></div>
<div class="grid2">{certs}{courses}</div>
<div class="sec"><h2>Skills</h2></div>
<dl class="skills">{skills}</dl>""", "Minji Kim's experience, education, honors, and skills.")

    cards = []
    for c in CAFES:
        stars = "★" * c["stars"] + f'<span class="off">{"★" * (5 - c["stars"])}</span>'
        imgs = "".join(f'<img src="{img(i)}" alt="{e(c["name"])}" loading="lazy">' for i in c["images"])
        count = f'<div class="count">{len(c["images"])} photos · swipe →</div>' if len(c["images"]) > 1 else ""
        cards.append(f'<div class="cafe"><div class="img">{imgs}</div><div class="body"><div class="name">{e(c["name"])}</div>'
                     f'<div class="loc">📍 {e(c["loc"])}</div><div class="stars">{stars}</div><div class="rev">"{e(c["review"])}"</div>{count}</div></div>')
    pages["cafes/index.html"] = page("Cafés", "cafes", f"""
<p class="eyebrow">Off the clock</p><h1>Café guide</h1>
<p class="lede">Where I study, work, and drink too much matcha.<br>Know a spot I should try? <a href="mailto:{SITE['email']}?subject=Caf%C3%A9%20suggestion" style="color:var(--accent)">Email me</a>.</p>
<div class="cafes" style="margin-top:2.5rem">{''.join(cards)}</div>""", "Minji's café guide.")

    pages["404.html"] = page("Not found", None, '<p class="eyebrow">404</p><h1>Page not found</h1><p class="lede"><a href="/" style="color:var(--accent)">Back home →</a></p>')

    for path, content in pages.items():
        f = ROOT / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
    print(f"Built {len(pages)} pages.")

if __name__ == "__main__":
    build()
