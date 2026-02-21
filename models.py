"""
models.py — SQLAlchemy ORM models and preference manager for long-term user memory.

Tables:
    - User:       Stores user profiles.
    - Preference:  Stores key-value preferences per user (e.g. "diet" → "vegan").
"""

import os
import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, create_engine
)
from sqlalchemy.orm import (
    declarative_base, relationship, sessionmaker, Session
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "travel_planner.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ── ORM Models ────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(120), nullable=False, default="Traveller")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    preferences = relationship(
        "Preference", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r}>"


class Preference(Base):
    __tablename__ = "preferences"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    user_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    key      = Column(String(100), nullable=False)
    value    = Column(Text, nullable=False)

    user = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<Preference {self.key!r}={self.value!r}>"


# Create tables on first import
Base.metadata.create_all(engine)


# ── Preference Manager (Single Responsibility) ───────────────────────────────

class UserPreferenceManager:
    """
    Provides CRUD operations for user preferences and formats them
    for injection into the LLM system prompt.
    """

    def __init__(self) -> None:
        self._session_factory = SessionLocal

    def _session(self) -> Session:
        return self._session_factory()

    # ── User CRUD ─────────────────────────────────────────────────────────

    def get_or_create_user(self, name: str = "Traveller") -> int:
        """Return the user's id, creating the user if not found."""
        with self._session() as session:
            user = session.query(User).filter_by(name=name).first()
            if not user:
                user = User(name=name)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user.id

    # ── Preference CRUD ───────────────────────────────────────────────────

    def add_preference(self, user_id: int, key: str, value: str) -> None:
        """Add or update a preference for a user."""
        with self._session() as session:
            existing = (
                session.query(Preference)
                .filter_by(user_id=user_id, key=key)
                .first()
            )
            if existing:
                existing.value = value
            else:
                session.add(Preference(user_id=user_id, key=key, value=value))
            session.commit()

    def get_preferences(self, user_id: int) -> list[dict]:
        """Return all preferences for a user as a list of {key, value} dicts."""
        with self._session() as session:
            prefs = (
                session.query(Preference)
                .filter_by(user_id=user_id)
                .all()
            )
            return [{"key": p.key, "value": p.value} for p in prefs]

    def delete_preference(self, user_id: int, key: str) -> bool:
        """Delete a specific preference. Returns True if deleted."""
        with self._session() as session:
            pref = (
                session.query(Preference)
                .filter_by(user_id=user_id, key=key)
                .first()
            )
            if pref:
                session.delete(pref)
                session.commit()
                return True
            return False

    # ── Prompt Injection ──────────────────────────────────────────────────

    def format_for_prompt(self, user_id: int) -> str:
        """
        Build a text block that can be appended to the system prompt.
        Returns an empty string if the user has no stored preferences.
        """
        prefs = self.get_preferences(user_id)
        if not prefs:
            return ""

        lines = ["\n\n## User Preferences (personalise the plan accordingly):"]
        for p in prefs:
            lines.append(f"- **{p['key']}**: {p['value']}")
        return "\n".join(lines)
