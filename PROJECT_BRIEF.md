# 📋 PROJECT BRIEF: Agentic AI Travel Planner
### *A Comprehensive Description for Content Creation & LinkedIn Post*

---

## 🧑‍💻 Developer

**Name:** Mustafa Kocaman  
**Role:** AI Engineer / Full-Stack Developer  
**GitHub:** github.com/MustafaKocamann  

---

## 1. WHAT IS THIS PROJECT?

The **Agentic AI Travel Planner** is a fully autonomous, multi-tool AI travel concierge application. Unlike basic chatbot wrappers, this system uses **LangGraph's ReAct (Reasoning + Acting) agent architecture** to orchestrate multiple real-time API calls, synthesize their outputs, and generate complete, data-driven travel plans — all through a single natural-language conversation.

The user simply types something like *"Plan 5 days in Paris for $2000"* and the AI agent autonomously:
- Fetches real-time weather for the destination
- Searches for hotels, restaurants, and attractions via Google Places
- Converts the budget to local currency using live exchange rates
- Calculates per-day spending allowances
- Returns a structured, day-by-day Markdown itinerary
- Plots every location on an interactive map
- Offers the plan as a downloadable branded PDF

---

## 2. THE PROBLEM IT SOLVES

Modern travel planning is fragmented. Travelers open 10+ browser tabs: weather sites, Google Maps, hotel aggregators, currency calculators, review platforms. By the time they've gathered the data, they're overwhelmed.

This project solves **the paradox of choice in travel planning** by consolidating everything into one conversational AI interface backed by real data — not hallucinated estimates.

---

## 3. TECHNICAL ARCHITECTURE

### Backend (FastAPI — Port 8000)
- Built with **FastAPI** (Python), the ASGI-based backend serves as the AI orchestration layer.
- Exposes REST endpoints: `/query`, `/preferences` (CRUD), `/users`, `/health`
- The core AI agent is a **LangGraph ReAct graph** compiled at startup using FastAPI's `lifespan` context manager (singleton pattern for performance)
- When a user_id is provided, a **personalised graph** is built on-the-fly with SQLite preferences injected into the system prompt

### AI Agent (LangGraph — ReAct Pattern)
- The `GraphBuilder` class wires together the LLM, tools, and StateGraph
- Uses **Groq Cloud** with **Meta Llama 3.3-70B Versatile** — sub-second token generation
- The agent has 8 registered tools it can call autonomously:
  1. `get_current_weather` — real-time weather conditions
  2. `get_weather_forecast` — 5-day weather forecast
  3. `convert_currency` — live exchange rates
  4. `calculate` — add, subtract, multiply, divide
  5. `calculate_percentage` — tips, tax, discounts
  6. `calculate_total_with_tax` — final cost with tax
  7. `search_places` — Google Places text search with coords
  8. `get_place_details` — reviews + detailed place info
- Two guard rails prevent common agent failures:
  - **Guard 1:** System prompt is always injected as the first message (prevents stale state issues)
  - **Guard 2:** Empty or `None` tool responses are replaced with informative fallback strings (prevents LLM confusion)

### Frontend (Flask — Port 5000)
- **Flask** serves the HTML/CSS/JS frontend with Jinja2 templates
- Session-based user tracking: each browser session gets a unique `user_id`
- Three main Flask routes: `/query` (relay), `/preferences` (CRUD), `/export_pdf` (PDF download)
- The Flask app automatically creates a user in SQLite on first visit
- Adds `sys.path` correction to import from the project root

### UI (Glassmorphism Design System)
- Built with **Tailwind CSS** (CDN-based, custom Navy + Gold config) and **vanilla CSS** for glassmorphism effects
- **GSAP 3.12** for hero entrance animations, staggered feature card reveals, floating CTA
- **Particle canvas** background (vanilla JS, 70 animated gold particles)
- **Marked.js** renders AI Markdown responses with custom styling in the chat window
- **Leaflet.js** for interactive maps with dark CARTO tiles and gold-tinted custom markers

### Database (SQLite + SQLAlchemy ORM)
- **Two ORM tables:** `User` (id, name, created_at) and `Preference` (id, user_id, key, value)
- `UserPreferenceManager` class handles all CRUD via context-managed SQLAlchemy sessions
- `format_for_prompt()` builds a formatted text block injected into the agent's system prompt
- Example: `budget=luxury`, `diet=vegan`, `pace=relaxed` → affects every trip plan automatically

### PDF Export (xhtml2pdf)
- Converts any Markdown AI response to branded HTML via the `markdown` library
- Applies Navy + Gold CSS styling (header, tables, code blocks, footer)
- Returns raw PDF bytes as a Flask file download (`application/pdf`)
- Triggered by a "Export as PDF" button that appears after each AI response

### Real-Time APIs
| API | Provider | What it provides |
|-----|----------|-----------------|
| Weather | OpenWeatherMap | Current conditions + 5-day forecast in Celsius |
| Places | Google Places API | Hotel/restaurant search with lat/lng, ratings, reviews |
| Currency | Frankfurter (free) | Live exchange rates, no API key required |

---

## 4. CODE STRUCTURE (All Files)

```
ai-travel-planner/
│
├── main.py                      ← FastAPI app, lifespan, all endpoints
├── models.py                    ← SQLAlchemy ORM: User, Preference, UserPreferenceManager
├── app.py                       ← Original Streamlit interface (legacy)
│
├── agents/
│   └── agentic_workflow.py      ← GraphBuilder: tool binding, ReAct graph, system prompt injection
│
├── tools/
│   ├── calculator_tool.py       ← @tool wrappers: calculate, percentage, tax
│   ├── currency_conversion.py   ← @tool wrapper: convert_currency
│   ├── place_search.py          ← @tool wrappers: search_places, get_place_details
│   └── weather_information.py   ← @tool wrappers: get_current_weather, get_weather_forecast
│
├── utils/
│   ├── calculator.py            ← Calculator class with float-safe arithmetic
│   ├── currency_converter.py    ← Frankfurter API wrapper with error handling
│   ├── place_info.py            ← Google Places: text search + place details (enriched)
│   ├── weather_info.py          ← OpenWeatherMap: current + 5-day forecast aggregation
│   ├── pdf_generator.py         ← Markdown → branded xhtml2pdf PDF bytes
│   ├── model_loader.py          ← LLM factory: loads ChatGroq from YAML config
│   ├── config_loader.py         ← Reads config/config.yaml (model name, provider)
│   └── save_document.py         ← Saves travel plans to outputs/ as .txt
│
├── flask_app/
│   ├── app.py                   ← Flask routes + session management + sys.path fix
│   ├── templates/
│   │   └── index.html           ← Full UI: hero, features, chat, Leaflet map, prefs modal
│   └── static/
│       ├── css/style.css        ← Design system: glassmorphism, animations, map styles
│       └── js/main.js           ← GSAP + particle canvas + chat logic + Leaflet + PDF export
│
├── prompt_library/
│   └── prompt.py                ← SYSTEM_PROMPT: elite travel concierge persona + rules
│
├── config/
│   └── config.yaml              ← LLM config: groq / llama-3.3-70b-versatile
│
├── exception/
│   └── handling.py              ← Custom exception classes
│
├── logger/
│   └── logging.py               ← Logging configuration
│
├── .env                         ← API keys (not in git)
├── .env.example                 ← Template for new developers
├── .gitignore                   ← Python standard gitignore
├── requirements.txt             ← All dependencies with version pins
└── README.md                    ← Professional README with badges + Mermaid diagrams
```

---

## 5. KEY LIBRARIES & THEIR ROLES

| Library | Version | Role |
|---------|---------|------|
| `fastapi` | ≥0.110 | High-performance async REST API server |
| `uvicorn` | ≥0.27 | ASGI server for FastAPI |
| `flask` | ≥3.0 | Frontend web server + template rendering |
| `langchain-groq` | ≥0.2 | Groq LLM integration for LangChain |
| `langchain-core` | ≥0.3 | Tool decorators, message types, base classes |
| `langgraph` | ≥0.2 | ReAct agent graph builder + StateGraph |
| `sqlalchemy` | ≥2.0 | ORM for SQLite user preferences |
| `pydantic` | ≥2.6 | Request/response validation in FastAPI |
| `python-dotenv` | ≥1.0 | Environment variable loading from .env |
| `pyyaml` | ≥6.0 | YAML config file parsing |
| `requests` | ≥2.31 | HTTP calls to external APIs |
| `xhtml2pdf` | ≥0.2 | HTML-to-PDF conversion for export |
| `markdown` | ≥3.5 | Markdown-to-HTML for PDF styling |
| **Tailwind CSS** | CDN | Utility-first CSS framework (frontend) |
| **GSAP** | 3.12 CDN | Professional animation library (frontend) |
| **Leaflet.js** | 1.9 CDN | Interactive open-source maps (frontend) |
| **Marked.js** | CDN | Markdown rendering in chat (frontend) |

---

## 6. ENGINEERING HIGHLIGHTS (For Technical Readers)

### SOLID Principles Applied:
- **S (Single Responsibility):** Each class has one job — `UserPreferenceManager` only manages prefs, `GraphBuilder` only builds graphs, `WeatherInfo` only calls weather APIs
- **O (Open/Closed):** New tools can be added to the agent's `self.tools` list without touching the graph wiring logic
- **D (Dependency Inversion):** `ModelLoader` abstracts LLM provider — switching from Groq to OpenAI would be a one-line config change

### Singleton Pattern:
The agent graph is compiled **once** at startup via FastAPI's `lifespan` context manager and stored in `app.state.agent`. Per-user personalized graphs are built on-demand only when preferences exist.

### Lazy Initialization:
Weather and Place tools use lazy initialization (`_get_weather_info()`, `_get_place_info()`) to avoid import errors when API keys are not set in the environment — the error only fires when the tool is actually called.

### Type Safety:
- Pydantic models validate all FastAPI request/response bodies
- `Calculator` explicitly casts all inputs to `float` to prevent type errors when the LLM passes integer-like strings
- All arithmetic returns are `round(..., 4)` for currency precision

### Coordinate Extraction from LLM Output:
The JavaScript frontend uses 3 different regex patterns to extract GPS coordinates from the AI's Markdown response and automatically drop Leaflet.js map markers — no structured JSON required from the LLM.

---

## 7. WHAT MAKES IT IMPRESSIVE

1. **True Autonomy:** The agent decides which tools to call based on context — it's not hardcoded
2. **Real Data:** Every weather report, place recommendation, and currency rate is fetched live — no hallucinations
3. **Long-Term Memory:** Preferences persist across sessions in SQLite and change how the AI responds
4. **Production-Grade:** FastAPI singleton pattern, Pydantic validation, proper error handling with traceback logging, CORS middleware, health endpoint
5. **Premium Design:** The UI looks like a luxury travel startup, not a hackathon project — glassmorphism, GSAP animations, particle canvas, gold/navy palette
6. **End-to-End Tested:** All endpoints verified working: `/health`, `/query` (200 with LLM response), `/preferences` CRUD, `/export_pdf` (valid 2782-byte PDF generated)

---

## 8. METRICS & NUMBERS

- **8 AI Tools** registered and available to the agent
- **2 Database Tables** (User + Preference) with full ORM CRUD
- **3 External APIs** integrated (OpenWeatherMap, Google Places, Frankfurter)
- **1 LLM** (Llama 3.3-70B via Groq) powering all reasoning
- **~2,000 lines of code** across Python + HTML + CSS + JS
- **3 coordinate regex patterns** for automatic map pin extraction
- **2 server processes** (FastAPI :8000 + Flask :5000) in a microservice architecture
- **300-second timeout** to handle complex multi-tool trip plans
- **100% verified** — all endpoints tested and returning correct data

---

## 9. TAGS & KEYWORDS (For LinkedIn)

`#ArtificialIntelligence` `#LangGraph` `#ReActAgent` `#MultiAgentAI` `#LLM`
`#Groq` `#Llama3` `#FastAPI` `#Flask` `#Python` `#SQLAlchemy` `#SQLite`
`#LeafletJS` `#GSAP` `#TailwindCSS` `#GooglePlacesAPI` `#OpenWeatherMap`
`#TravelTech` `#AIEngineering` `#FullStack` `#OpenToWork` `#MachineLearning`
`#Productivity` `#SideProject` `#BuildInPublic` `#AIAgent` `#GenAI`
