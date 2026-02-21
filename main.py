from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse

from agents.agentic_workflow import GraphBuilder
from models import UserPreferenceManager
from utils.save_document import save_document

load_dotenv()

pref_mgr = UserPreferenceManager()


# ---------------------------------------------------------------------------
# Lifespan: build the default (no-user) graph ONCE at startup.
# Per-user graphs with preference injection are built on demand.
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager — runs startup logic before yield."""
    print("Initialising default GraphBuilder and compiling ReAct graph...")
    graph_builder = GraphBuilder(model_provider="groq")
    app.state.agent = graph_builder()
    print("Graph compiled and ready.")
    yield
    print("Application shutting down.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Travel Planner",
    description="Agentic travel planning API powered by LangGraph + Groq.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class QueryRequest(BaseModel):
    question: str
    user_id: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str


class PreferenceIn(BaseModel):
    user_id: int
    key: str
    value: str


class PreferenceDeleteIn(BaseModel):
    user_id: int
    key: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/query", response_model=QueryResponse)
async def query_travel_agent(query: QueryRequest):
    """
    Accept a natural-language travel question and return a detailed travel plan.

    If `user_id` is provided, a personalised graph with the user's stored
    preferences is compiled on-the-fly.  Otherwise, the default singleton
    graph is used.
    """
    try:
        if query.user_id is not None:
            # Build a per-user graph with preference injection
            builder = GraphBuilder(model_provider="groq", user_id=query.user_id)
            react_app = builder()
        else:
            react_app = app.state.agent

        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return QueryResponse(answer=final_output)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


# ── Preferences CRUD ──────────────────────────────────────────────────────

@app.post("/preferences")
async def set_preference(pref: PreferenceIn):
    """Add or update a user preference."""
    pref_mgr.add_preference(pref.user_id, pref.key, pref.value)
    return {"status": "ok", "message": f"Preference '{pref.key}' saved."}


@app.get("/preferences/{user_id}")
async def get_preferences(user_id: int):
    """Return all preferences for a user."""
    return {"user_id": user_id, "preferences": pref_mgr.get_preferences(user_id)}


@app.delete("/preferences")
async def delete_preference(pref: PreferenceDeleteIn):
    """Delete a specific preference."""
    deleted = pref_mgr.delete_preference(pref.user_id, pref.key)
    if deleted:
        return {"status": "ok", "message": f"Preference '{pref.key}' deleted."}
    return JSONResponse(status_code=404, content={"error": "Preference not found."})


@app.post("/users")
async def create_user(name: str = "Traveller"):
    """Create a new user and return their ID."""
    user_id = pref_mgr.get_or_create_user(name)
    return {"user_id": user_id, "name": name}


@app.get("/health")
async def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok"}