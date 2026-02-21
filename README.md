<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=30&pause=1000&color=FFD700&center=true&vCenter=true&width=600&lines=Mustafa+AI+Travel+Concierge;Problem+Çözme+Sanatı+🎯;Agentic+AI+Travel+Planner;5-Star+Travel+Experience+✈️" alt="Typing Animation" />
</p>

<p align="center">
  <img src="https://img.icons8.com/3d-fluency/94/airplane-take-off.png" width="80" alt="Logo"/>
</p>

<h1 align="center">✈️ Agentic AI Travel Planner</h1>

<p align="center">
  <strong>A multi-agent, tool-augmented AI travel concierge powered by LangGraph, Groq, and real-time APIs.</strong>
</p>

<p align="center">
  <a href="https://github.com/MustafaKocamann/AI-Based-Trip-Planner"><img src="https://img.shields.io/github/stars/MustafaKocamann/AI-Based-Trip-Planner?style=for-the-badge&color=gold" alt="Stars"/></a>
  <a href="https://github.com/MustafaKocamann/AI-Based-Trip-Planner"><img src="https://img.shields.io/github/forks/MustafaKocamann/AI-Based-Trip-Planner?style=for-the-badge&color=gold" alt="Forks"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Star--Worthy-FF6F00?style=for-the-badge" alt="Status"/></a>
</p>

<p align="center">
  <em>"Veriden Değere, Algoritmadan Anlama"</em>
</p>

---

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider" width="100%"/>
</p>

## 🚀 Program Özellikleri

<table align="center">
  <tr>
    <td align="center"><b>14 Hafta</b><br/>Kapsamlı Müfredat</td>
    <td align="center"><b>50+ Kavram</b><br/>Derinlemesine İçerik</td>
    <td align="center"><b>2 Proje Sunumu</b><br/>Ara & Final Projeleri</td>
    <td align="center"><b>∞ Potansiyel</b><br/>Sınırsız Öğrenme</td>
  </tr>
</table>

---

## 🏗️ System Architecture

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

## 🎯 The Core Philosophy: "Problem Çözme Sanatı"

Travel planning is a complex optimization problem. Our agent doesn't just "talk"; it **analyzes** and **executes**.

1.  **Reasoning:** The agent breaks down your request into logical sub-tasks.
2.  **Action:** It triggers real-time data fetching (Weather, Places, Currency).
3.  **Synthesis:** It compiles a data-driven, personalized itinerary.

---

## ✨ Key Technical Pillars

<p align="center">
  <img src="https://img.shields.io/badge/🧠_Memory-SQLite_SQLAlchemy-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/🗺️_Interactive-Leaflet.js-green?style=flat-square"/>
  <img src="https://img.shields.io/badge/⚡_Performance-Groq_Llama_3.3-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/📊_Budget-Frankfurter_API-yellow?style=flat-square"/>
</p>

### 🧠 Long-Term Memory
Persistent user profiling powered by **SQLite**. Your preferences (budget, dietary, pace) are dynamically injected into every plan.

### 🗺️ Interactive Mapping
**Leaflet.js** integration with gold-themed markers. Pins are automatically dropped on the map as the agent plans your route.

### 📄 PDF Engine
Branded, print-ready PDF exports using `xhtml2pdf`. One-click professional travel docs.

---

## 🔧 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

---

## 🛠️ Installation & Setup

1.  **Clone:** `git clone https://github.com/MustafaKocamann/AI-Based-Trip-Planner.git`
2.  **Env:** `cp .env.example .env` (Add your Groq & OpenWeather keys)
3.  **Setup:** `pip install -r requirements.txt`
4.  **Backend:** `uvicorn main:app --port 8000`
5.  **Frontend:** `python flask_app/app.py`
6.  **Explore:** `http://localhost:5000`

---

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="divider" width="100%"/>
</p>

<h3 align="center">💛 Lead Developer: <a href="https://github.com/MustafaKocamann">Mustafa Kocaman</a></h3>

<p align="center">
  <a href="https://github.com/MustafaKocamann">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://linkedin.com/in/mustafakocaman">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn"/>
  </a>
</p>
