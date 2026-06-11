# API Knowledge Base — Index

Navigation layer for the curated public API catalog. **1554 APIs across 50 category files.** Open only the category file relevant to your task to keep context small.

Source: this repository's `README.md`. Regenerate with `python3 scripts/knowledgebase/build_catalog.py`.

## Categories

| Category | APIs | Covers |
|:---------|-----:|:-------|
| [Machine Learning](ai.md) | 28 | AI/ML inference: NLP, vision, generative, speech and prediction. |
| [Animals](animals.md) | 27 | Animal facts, imagery, taxonomy and pet/adoption data. |
| [Anime](anime.md) | 19 | Anime/manga metadata, artwork, quotes and tracking. |
| [Anti-Malware](anti-malware.md) | 15 | URL/file reputation, threat intelligence and malware scanning. |
| [Art & Design](art-design.md) | 22 | Museum collections, color palettes, design assets and imagery. |
| [Authentication & Authorization](authentication.md) | 7 | Identity, OAuth/OIDC, magic links and access management. |
| [Blockchain](blockchain.md) | 13 | On-chain data, indexing, smart-contract and wallet queries. |
| [Books](books.md) | 27 | Book metadata, full text, catalogs and reading data. |
| [Business](business.md) | 25 | Company data, invoicing, CRM, lead and entity lookup. |
| [Calendar](calendar.md) | 18 | Holidays, events, scheduling and date utilities. |
| [Cloud Storage & File Sharing](cloud-storage.md) | 18 | Object storage, file hosting, sync and sharing. |
| [Email / Phone](communication.md) | 26 | Transactional/marketing email, validation and inbox tooling.; SMS, voice, phone validat... |
| [Continuous Integration](continuous-integration.md) | 6 | Build pipelines, CI status and deployment automation. |
| [Cryptocurrency](cryptocurrency.md) | 65 | Crypto prices, market data, exchange and DeFi feeds. |
| [Currency Exchange](currency-exchange.md) | 18 | Fiat/forex rates, historical and real-time conversion. |
| [Data Validation](data-validation.md) | 7 | Email/phone/address/VAT validation and verification. |
| [Development](development.md) | 132 | Developer utilities: testing, hosting, code, webhooks, tooling. |
| [Dictionaries](dictionaries.md) | 13 | Definitions, synonyms, translations and word data. |
| [Documents & Productivity](documents-productivity.md) | 34 | Document generation, PDF, OCR, office and productivity tooling. |
| [Entertainment](entertainment.md) | 16 | Jokes, trivia, memes and miscellaneous fun content. |
| [Environment](environment.md) | 18 | Climate, carbon, air quality and sustainability data. |
| [Events](events.md) | 3 | Event discovery, ticketing and venue data. |
| [Finance](finance.md) | 51 | Stocks, market data, banking, economics and financial statements. |
| [Food & Drink](food-drink.md) | 25 | Recipes, nutrition, restaurants and beverage data. |
| [Games & Comics](games-comics.md) | 97 | Game stats, comics, board/video game data and APIs. |
| [Government](government.md) | 95 | Open government, civic, legislative and public-sector data. |
| [Health](health.md) | 35 | Medical, clinical, drug, nutrition and wellness data. |
| [Jobs](jobs.md) | 20 | Job listings, recruiting and labor-market data. |
| [Geocoding](maps.md) | 92 | Geocoding, reverse geocoding, maps, places and routing. |
| [Music](music.md) | 35 | Tracks, lyrics, metadata, streaming and audio data. |
| [News](news.md) | 20 | Headlines, articles, aggregation and media feeds. |
| [Open Data](open-data.md) | 42 | Public datasets across many domains. |
| [Open Source Projects](open-source.md) | 9 | Data about open-source projects and ecosystems. |
| [Patent](patent.md) | 4 | Patent search, filings and intellectual-property data. |
| [Personality](personality.md) | 25 | Quotes, advice, horoscopes and personality content. |
| [Photography](photography.md) | 29 | Stock photos, image hosting, processing and search. |
| [Programming](programming.md) | 5 | Coding challenges, language and programming-related data. |
| [Science & Math](science-math.md) | 35 | Scientific, astronomical, mathematical and research data. |
| [Security](security.md) | 41 | Vulnerabilities, breaches, secrets scanning and security data. |
| [Shopping](shopping.md) | 15 | Products, pricing, e-commerce and retail data. |
| [Social](social.md) | 43 | Social platforms, profiles, posts and engagement data. |
| [Sports & Fitness](sports-fitness.md) | 41 | Scores, stats, fixtures and fitness/activity data. |
| [Test Data](test-data.md) | 27 | Mock/fake data and placeholder generators. |
| [Text Analysis](text-analysis.md) | 18 | NLP: sentiment, entities, language detection and parsing. |
| [Tracking](tracking.md) | 10 | Shipment, parcel and logistics tracking. |
| [Transportation](transportation.md) | 74 | Transit, flights, traffic and mobility data. |
| [URL Shorteners](url-shorteners.md) | 20 | Short links, redirects and link analytics. |
| [Vehicle](vehicle.md) | 10 | VIN, registration, EV and automotive data. |
| [Video](video.md) | 45 | Video metadata, streaming, hosting and processing. |
| [Weather](weather.md) | 34 | Forecasts, current conditions, severe weather and climate. |

## How to use

1. Find the category matching the requirement in the table above.
2. Open that single category file (e.g. `finance.md`, `ai.md`, `maps.md`).
3. Scan the API table; follow the **Docs** link for endpoints, rate limits, and auth setup.

## Auth legend

- **None** — no authentication required.
- **apiKey** — register for an API key/token.
- **OAuth** — OAuth 2.0 / OIDC flow.
- **X-Mashape-Key / User-Agent** — provider-specific header.
- **HTTPS / CORS** — `Yes`/`No`/`Unknown` support flags from the source.
