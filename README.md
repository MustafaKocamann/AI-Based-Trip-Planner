<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=35&pause=1000&color=FFD700&center=true&vCenter=true&width=700&lines=Mustafa+AI+Travel+Concierge;Problem+Çözme+Sanatı+🎯;Agentic+AI+Travel+Planner;5-Star+Travel+Experience+✈️;Powered+by+LangGraph+%26+Groq" alt="Typing Animation" />
</p>

<p align="center">
  <img src="https://img.icons8.com/3d-fluency/94/airplane-take-off.png" width="80" alt="Logo"/>
</p>

<h1 align="center">✈️ Agentic AI Travel Planner</h1>

<p align="center">
  <strong>A Multi-Agent, Tool-Augmented AI Travel Concierge — powered by LangGraph, Groq, and Real-Time APIs.</strong>
</p>

<p align="center">
  <a href="https://github.com/MustafaKocamann/AI-Based-Trip-Planner"><img src="https://img.shields.io/github/stars/MustafaKocamann/AI-Based-Trip-Planner?style=for-the-badge&color=gold&logo=github" alt="Stars"/></a>
  <a href="https://github.com/MustafaKocamann/AI-Based-Trip-Planner"><img src="https://img.shields.io/github/forks/MustafaKocamann/AI-Based-Trip-Planner?style=for-the-badge&color=gold&logo=github" alt="Forks"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Stack-FastAPI_%7C_Flask_%7C_LangGraph-009688?style=for-the-badge" alt="Tech Stack"/></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider" width="100%"/>
</p>

---

## 📸 Visual Hook & System Architecture

<p align="center">
  <img src="https://github.com/MustafaKocamann/AI-Based-Trip-Planner/raw/main/docs/dashboard_preview.gif" alt="Main Dashboard GIF Placeholder" width="90%"/>
  <br/>
  <em>🎬 **Main Dashboard Preview:** AI-driven itinerary generation, interactive mapping, and PDF export in action.</em>
</p>

### 🏗️ Agentic Workflow (LangGraph)

```mermaid
graph TB
    subgraph "🖥️ Frontend — Flask :5000"
        A[🌐 Landing Page<br>GSAP + Tailwind + Glassmorphism] --> B[💬 Chat Interface<br>Markdown + Typing Indicator]
        B --> C[🗺️ Leaflet.js Map<br>Auto Marker Plotting]
        B --> D[📄 PDF Export<br>xhtml2pdf Branded Docs]
        A --> E[⚙️ Preferences Modal<br>SQLite Persistence]
    end

    subgraph "⚡ Backend — FastAPI :8000"
        F[🔀 API Router] --> G[🧠 LangGraph Agent<br>ReAct Loop]
        F --> H[📦 Preference CRUD<br>SQLAlchemy ORM]
        G --> I[🛠️ Tool Orchestrator]
    end

    subgraph "🛠️ Agent Tools"
        I --> J[🌤️ OpenWeatherMap<br>Current + 5-Day Forecast]
        I --> K[📍 Google Places<br>Search + Reviews + Coords]
        I --> L[💱 Frankfurter API<br>Real-Time Exchange Rates]
        I --> M[🧮 Calculator<br>Budget + Tax + Tips]
    end

    subgraph "💾 Persistence Layer"
        N[(🗄️ SQLite Database)]
        H --> N
        G -->|Inject Preferences| N
    end

    subgraph "🤖 LLM Provider"
        O[⚡ Groq Cloud<br>Llama 3.3-70B Versatile]
    end

    B -->|POST /query| F
    E -->|POST /preferences| F
    D -->|POST /export_pdf| F
    G --> O
    O --> G

    style A fill:#001F3F,stroke:#FFD700,color:#FFD700
    style B fill:#001F3F,stroke:#FFD700,color:#FFD700
    style G fill:#1a1a2e,stroke:#e94560,color:#FFD700
    style O fill:#0d0d0d,stroke:#e94560,color:#e94560
```

---

## 🎯 The 'Why' - Solving the Paradox of Choice

Travel planning is broken. Travelers today navigate a "choice paradox," bouncing between 10+ tabs: hotel aggregators, weather sites, currency converters, Map tools, and review platforms. By the time they have gathered enough data, decision fatigue sets in.

**Agentic AI Travel Planner** solves this by providing a single conversional interface where **Multi-Agent AI** does the heavy lifting. It doesn't just "chat"—it researches, calculates, validates, and plan. It's not a hallucination engine; it's an execution engine.

---

## ✨ Key Features

<p align="center">
  <img src="https://img.shields.io/badge/🧠_Memory-SQLite_Persistence-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/🗺️_Mapping-Real--Time_Leaflet.js-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/⚡_Inference-Groq_Llama--3.3-red?style=for-the-badge"/>
</p>

### 🧠 Long-Term Memory
Persistent user profiling powered by **SQLite + SQLAlchemy**. Your historical preferences (dietary, pace, budget) are stored and dynamically injected into the AI's system prompt for a truly personalized experience.

### 🗺️ Interactive Mapping
Seamless **Leaflet.js** integration. The AI doesn't just suggest places; it drops gold-themed markers on a dark-themed interactive map in real-time.

### ⚡ Lightning Fast Inference
Leveraging **Groq Cloud** with **Meta’s Llama-3.3-70B**. Sub-second token generation provides a near-instant "Senior AI" consultation feel.

### 📊 Financial Dashboard
Precise budgeting with **real-time exchange rates** (Frankfurter API) and a precision calculator. No more manual math on currency spreads.

---

## 🔧 Tech Stack

| Category | tools |
| :--- | :--- |
| **🤖 LLM** | Groq (Llama 3.3-70B), LangChain |
| **🧩 Framework** | FastAPI, Flask, LangGraph |
| **🔍 Search** | Tavily, Google Places API |
| **🌐 API** | OpenWeatherMap, Frankfurter |
| **🎨 Frontend** | Tailwind CSS, GSAP, Leaflet.js |

---

## ⚙️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/MustafaKocamann/AI-Based-Trip-Planner.git
cd AI-Based-Trip-Planner
```

### Step 2: Environment Configuration
```bash
cp .env.example .env
# Fill in your GROQ_API_KEY and OPENWEATHERMAP_API_KEY
```

### Step 3: Deployment
```bash
pip install -r requirements.txt

# Terminal 1: Launch Backend
uvicorn main:app --reload --port 8000

# Terminal 2: Launch Frontend
python flask_app/app.py
```

### Step 4: Launch
```
🌐 Visit http://localhost:5000
```

---

## 🧬 Engineering Highlight: The Agentic Workflow

This project utilizes a **ReAct (Reasoning + Acting)** pattern implemented via **LangGraph**. Unlike standard linear LLM chains, our agent:

1.  **Observes** the user request and user preferences from SQLite.
2.  **Reasons** about which tool is required (e.g., "I need weather data before I suggest outdoor activities").
3.  **Acts** by triggering the ToolNode to call external APIs.
4.  **Refines** the plan based on tool results, repeating the loop until a multi-day itinerary is fully validated.

---

## 🗺️ Future Roadmap (Growth Hacker's Vision)

- [ ] **Mobile App Integration:** Swift/Kotlin wrappers for planning on-the-go.
- [ ] **Voice AI Assistant:** Whisper + Piper integration for hands-free concierge service.
- [ ] **Global Scaling:** Multi-language support and direct booking integration (Amadeus/Skyscanner).

---

## 📄 License & Credits

Lead Developer: **Mustafa Kocaman**  
License: **MIT**

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider" width="100%"/>
</p>

<h3 align="center">💛 Built for the Future of AI Travel</h3>

<p align="center">
  <a href="https://github.com/MustafaKocamann">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://linkedin.com/in/mustafakocaman">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn"/>
  </a>
</p>
