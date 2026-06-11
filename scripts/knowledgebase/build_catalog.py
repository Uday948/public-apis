#!/usr/bin/env python3
"""
Build a structured API knowledge base from README.md.

Parses the public-apis README into per-category Markdown files under docs/apis/
plus a master index. Re-run this whenever README.md changes:

    python3 scripts/knowledgebase/build_catalog.py

Source data per API (all that the README provides): Name, Doc Link,
Description, Auth, HTTPS, CORS. Endpoints / rate limits are not in the source,
so they are summarised at the category level and deferred to official docs.
"""
import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README = os.path.join(ROOT, "README.md")
OUTDIR = os.path.join(ROOT, "docs", "apis")

# Category -> (slug/filename, capabilities blurb, typical use cases blurb)
# Slugs intentionally use friendly aliases for the common domains
# (Machine Learning -> ai, Geocoding -> maps). Email + Phone merge into
# communication. Everything else is a slugified category name.
CATEGORIES = OrderedDict([
    ("Animals", ("animals", "Animal facts, imagery, taxonomy and pet/adoption data.", "Educational apps, pet adoption sites, fun bots, placeholder media.")),
    ("Anime", ("anime", "Anime/manga metadata, artwork, quotes and tracking.", "Anime catalog apps, recommendation engines, fan sites, Discord bots.")),
    ("Anti-Malware", ("anti-malware", "URL/file reputation, threat intelligence and malware scanning.", "Security scanners, link checkers, abuse detection, SOC tooling.")),
    ("Art & Design", ("art-design", "Museum collections, color palettes, design assets and imagery.", "Design tools, gallery apps, color generators, creative content.")),
    ("Authentication & Authorization", ("authentication", "Identity, OAuth/OIDC, magic links and access management.", "Login flows, SSO, passwordless auth, user management.")),
    ("Blockchain", ("blockchain", "On-chain data, indexing, smart-contract and wallet queries.", "Web3 dashboards, explorers, DeFi apps, analytics.")),
    ("Books", ("books", "Book metadata, full text, catalogs and reading data.", "Reading apps, citation tools, library catalogs, recommendations.")),
    ("Business", ("business", "Company data, invoicing, CRM, lead and entity lookup.", "B2B SaaS, billing systems, sales tooling, enrichment.")),
    ("Calendar", ("calendar", "Holidays, events, scheduling and date utilities.", "Scheduling apps, HR systems, reminders, localization.")),
    ("Cloud Storage & File Sharing", ("cloud-storage", "Object storage, file hosting, sync and sharing.", "Backups, file uploads, media hosting, document pipelines.")),
    ("Continuous Integration", ("continuous-integration", "Build pipelines, CI status and deployment automation.", "DevOps dashboards, build bots, release tooling.")),
    ("Cryptocurrency", ("cryptocurrency", "Crypto prices, market data, exchange and DeFi feeds.", "Trading bots, portfolio trackers, price tickers, analytics.")),
    ("Currency Exchange", ("currency-exchange", "Fiat/forex rates, historical and real-time conversion.", "Pricing, invoicing, travel apps, financial dashboards.")),
    ("Data Validation", ("data-validation", "Email/phone/address/VAT validation and verification.", "Sign-up forms, data cleaning, compliance, lead quality.")),
    ("Development", ("development", "Developer utilities: testing, hosting, code, webhooks, tooling.", "Internal tools, automation, prototyping, dev productivity.")),
    ("Dictionaries", ("dictionaries", "Definitions, synonyms, translations and word data.", "Language apps, writing aids, word games, education.")),
    ("Documents & Productivity", ("documents-productivity", "Document generation, PDF, OCR, office and productivity tooling.", "Doc automation, invoicing, e-sign, content extraction.")),
    ("Email", ("communication", "Transactional/marketing email, validation and inbox tooling.", "Notifications, newsletters, OTP delivery, contact forms.")),
    ("Entertainment", ("entertainment", "Jokes, trivia, memes and miscellaneous fun content.", "Chatbots, games, social apps, engagement features.")),
    ("Environment", ("environment", "Climate, carbon, air quality and sustainability data.", "ESG apps, dashboards, climate tooling, research.")),
    ("Events", ("events", "Event discovery, ticketing and venue data.", "Event apps, listings, local discovery, ticket integrations.")),
    ("Finance", ("finance", "Stocks, market data, banking, economics and financial statements.", "Trading apps, dashboards, fintech, research, accounting.")),
    ("Food & Drink", ("food-drink", "Recipes, nutrition, restaurants and beverage data.", "Recipe apps, meal planners, nutrition trackers, ordering.")),
    ("Games & Comics", ("games-comics", "Game stats, comics, board/video game data and APIs.", "Companion apps, leaderboards, fan tools, game bots.")),
    ("Geocoding", ("maps", "Geocoding, reverse geocoding, maps, places and routing.", "Maps, delivery, store locators, location search, navigation.")),
    ("Government", ("government", "Open government, civic, legislative and public-sector data.", "Civic tech, compliance, research, transparency apps.")),
    ("Health", ("health", "Medical, clinical, drug, nutrition and wellness data.", "Health apps, clinical tools, research, fitness.")),
    ("Jobs", ("jobs", "Job listings, recruiting and labor-market data.", "Job boards, recruiting tools, career sites, analytics.")),
    ("Machine Learning", ("ai", "AI/ML inference: NLP, vision, generative, speech and prediction.", "AI features, chatbots, content generation, automation, analysis.")),
    ("Music", ("music", "Tracks, lyrics, metadata, streaming and audio data.", "Music apps, players, discovery, lyric displays, bots.")),
    ("News", ("news", "Headlines, articles, aggregation and media feeds.", "News apps, alerts, aggregators, sentiment monitoring.")),
    ("Open Data", ("open-data", "Public datasets across many domains.", "Research, dashboards, data science, civic apps.")),
    ("Open Source Projects", ("open-source", "Data about open-source projects and ecosystems.", "Dev dashboards, dependency tools, OSS analytics.")),
    ("Patent", ("patent", "Patent search, filings and intellectual-property data.", "IP research, legal tooling, prior-art search.")),
    ("Personality", ("personality", "Quotes, advice, horoscopes and personality content.", "Engagement features, chatbots, content widgets.")),
    ("Phone", ("communication", "SMS, voice, phone validation and telephony.", "OTP/2FA, notifications, call apps, contact verification.")),
    ("Photography", ("photography", "Stock photos, image hosting, processing and search.", "Galleries, placeholder media, image pipelines, design.")),
    ("Programming", ("programming", "Coding challenges, language and programming-related data.", "Learning platforms, dev tools, practice apps.")),
    ("Science & Math", ("science-math", "Scientific, astronomical, mathematical and research data.", "Education, research, visualization, STEM apps.")),
    ("Security", ("security", "Vulnerabilities, breaches, secrets scanning and security data.", "Security tooling, monitoring, compliance, research.")),
    ("Shopping", ("shopping", "Products, pricing, e-commerce and retail data.", "Storefronts, price comparison, affiliate, inventory.")),
    ("Social", ("social", "Social platforms, profiles, posts and engagement data.", "Social apps, dashboards, marketing, community tools.")),
    ("Sports & Fitness", ("sports-fitness", "Scores, stats, fixtures and fitness/activity data.", "Sports apps, fantasy leagues, fitness trackers, betting.")),
    ("Test Data", ("test-data", "Mock/fake data and placeholder generators.", "Testing, seeding, prototyping, demos.")),
    ("Text Analysis", ("text-analysis", "NLP: sentiment, entities, language detection and parsing.", "Moderation, analytics, search, content understanding.")),
    ("Tracking", ("tracking", "Shipment, parcel and logistics tracking.", "E-commerce, logistics dashboards, delivery notifications.")),
    ("Transportation", ("transportation", "Transit, flights, traffic and mobility data.", "Travel apps, routing, fleet tools, transit displays.")),
    ("URL Shorteners", ("url-shorteners", "Short links, redirects and link analytics.", "Marketing, social sharing, click tracking.")),
    ("Vehicle", ("vehicle", "VIN, registration, EV and automotive data.", "Auto marketplaces, fleet, insurance, EV apps.")),
    ("Video", ("video", "Video metadata, streaming, hosting and processing.", "Media apps, players, discovery, transcoding pipelines.")),
    ("Weather", ("weather", "Forecasts, current conditions, severe weather and climate.", "Weather apps, dashboards, agriculture, logistics, alerts.")),
])

ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|(.*)$")


def parse_readme():
    with open(README, encoding="utf-8") as f:
        lines = f.readlines()

    cats = OrderedDict()  # category name -> list of api dicts
    current = None
    for line in lines:
        h = re.match(r"^###\s+(.*?)\s*$", line)
        if h:
            current = h.group(1)
            cats.setdefault(current, [])
            continue
        if current is None:
            continue
        m = ROW_RE.match(line.rstrip())
        if not m:
            continue
        name, link, rest = m.group(1), m.group(2), m.group(3)
        parts = [p.strip() for p in rest.split("|")]
        # rest splits into: description, auth, https, cors, (trailing empties)
        desc = parts[0] if len(parts) > 0 else ""
        auth = parts[1] if len(parts) > 1 else ""
        https = parts[2] if len(parts) > 2 else ""
        cors = parts[3] if len(parts) > 3 else ""
        auth_clean = auth.replace("`", "").strip() or "Unknown"
        if auth_clean.lower() == "no":
            auth_clean = "None"
        cats[current].append({
            "name": name.strip(),
            "link": link.strip(),
            "desc": desc.strip(),
            "auth": auth_clean,
            "https": https.strip() or "Unknown",
            "cors": cors.strip() or "Unknown",
        })
    return cats


def slug_for(category):
    if category not in CATEGORIES:
        raise KeyError(f"Unmapped category: {category}")
    return CATEGORIES[category][0]


def write_category_files(cats):
    # Group categories by output slug (Email + Phone -> communication)
    by_slug = OrderedDict()
    for cat, apis in cats.items():
        slug, caps, uses = CATEGORIES[cat]
        by_slug.setdefault(slug, {"sources": [], "apis": []})
        by_slug[slug]["sources"].append((cat, caps, uses))
        by_slug[slug]["apis"].extend(apis)

    file_meta = OrderedDict()  # slug -> (title, count, sources)
    for slug, data in by_slug.items():
        sources = data["sources"]
        apis = sorted(data["apis"], key=lambda a: a["name"].lower())
        title = " / ".join(c for c, _, _ in sources)
        file_meta[slug] = {"title": title, "count": len(apis), "sources": sources}

        lines = []
        lines.append(f"# {title} APIs")
        lines.append("")
        lines.append(f"> Category file in the [API Knowledge Base](index.md). "
                     f"**{len(apis)} APIs.** Auto-generated from `README.md` by "
                     f"`scripts/knowledgebase/build_catalog.py` — do not edit by hand.")
        lines.append("")
        lines.append("## Capabilities & typical use cases")
        lines.append("")
        for cat, caps, uses in sources:
            lines.append(f"- **{cat} — capabilities:** {caps}")
            lines.append(f"  - **Use cases:** {uses}")
        lines.append("")
        lines.append("**Endpoints & rate limits:** not enumerated in the source catalog. "
                     "Each API's high-level endpoints and rate limits are documented on its "
                     "official site — open the **Docs** link before integrating.")
        lines.append("")
        lines.append("## APIs")
        lines.append("")
        lines.append("| API | Description | Auth | HTTPS | CORS | Docs |")
        lines.append("|:----|:------------|:-----|:------|:-----|:-----|")
        for a in apis:
            desc = a["desc"].replace("|", "\\|")
            auth = a["auth"] if a["auth"] != "None" else "None"
            lines.append(
                f"| {a['name']} | {desc} | {auth} | {a['https']} | {a['cors']} | "
                f"[link]({a['link']}) |"
            )
        lines.append("")
        lines.append(f"[⬆ Back to index](index.md)")
        lines.append("")
        with open(os.path.join(OUTDIR, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    return file_meta


def write_index(file_meta, total):
    lines = []
    lines.append("# API Knowledge Base — Index")
    lines.append("")
    lines.append(f"Navigation layer for the curated public API catalog. "
                 f"**{total} APIs across {len(file_meta)} category files.** "
                 f"Open only the category file relevant to your task to keep context small.")
    lines.append("")
    lines.append("Source: this repository's `README.md`. Regenerate with "
                 "`python3 scripts/knowledgebase/build_catalog.py`.")
    lines.append("")
    lines.append("## Categories")
    lines.append("")
    lines.append("| Category | APIs | Covers |")
    lines.append("|:---------|-----:|:-------|")
    for slug, meta in sorted(file_meta.items()):
        covers = "; ".join(caps for _, caps, _ in meta["sources"])
        covers = covers.replace("|", "\\|")
        # keep the "covers" cell short
        if len(covers) > 90:
            covers = covers[:87] + "..."
        lines.append(f"| [{meta['title']}]({slug}.md) | {meta['count']} | {covers} |")
    lines.append("")
    lines.append("## How to use")
    lines.append("")
    lines.append("1. Find the category matching the requirement in the table above.")
    lines.append("2. Open that single category file (e.g. `finance.md`, `ai.md`, `maps.md`).")
    lines.append("3. Scan the API table; follow the **Docs** link for endpoints, "
                 "rate limits, and auth setup.")
    lines.append("")
    lines.append("## Auth legend")
    lines.append("")
    lines.append("- **None** — no authentication required.")
    lines.append("- **apiKey** — register for an API key/token.")
    lines.append("- **OAuth** — OAuth 2.0 / OIDC flow.")
    lines.append("- **X-Mashape-Key / User-Agent** — provider-specific header.")
    lines.append("- **HTTPS / CORS** — `Yes`/`No`/`Unknown` support flags from the source.")
    lines.append("")
    with open(os.path.join(OUTDIR, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    cats = parse_readme()
    # Validate every parsed category is mapped
    unmapped = [c for c in cats if c not in CATEGORIES]
    if unmapped:
        print("ERROR: unmapped categories:", unmapped, file=sys.stderr)
        sys.exit(1)
    file_meta = write_category_files(cats)
    total = sum(len(v) for v in cats.values())
    write_index(file_meta, total)

    # Summary report
    print(f"Total APIs: {total}")
    print(f"Source categories: {len(cats)}")
    print(f"Category files: {len(file_meta)}")
    print("\nAPIs per source category:")
    for cat, apis in cats.items():
        print(f"  {cat:32s} {len(apis):4d} -> {slug_for(cat)}.md")
    # Auth distribution
    from collections import Counter
    auth_counts = Counter(a["auth"] for apis in cats.values() for a in apis)
    print("\nAuth distribution:")
    for auth, n in auth_counts.most_common():
        print(f"  {auth:20s} {n:4d}")
    no_https = [a["name"] for apis in cats.values() for a in apis if a["https"] == "No"]
    print(f"\nAPIs without HTTPS: {len(no_https)}")


if __name__ == "__main__":
    main()
