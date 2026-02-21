import os
import sys
import requests

# Ensure project root is importable (Flask runs from flask_app/ sub-dir)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from flask import (
    Flask, render_template, request, jsonify, session, send_file
)
from dotenv import load_dotenv
import io

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "mustafa-concierge-dev-key")

# FastAPI backend URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")


# ── Helpers ────────────────────────────────────────────────────────────────

def _ensure_user() -> int:
    """Return the session user_id, creating a new user on first visit."""
    if "user_id" not in session:
        try:
            resp = requests.post(f"{FASTAPI_URL}/users", params={"name": "Traveller"}, timeout=10)
            resp.raise_for_status()
            session["user_id"] = resp.json()["user_id"]
        except Exception:
            session["user_id"] = 1  # fallback
    return session["user_id"]


# ── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page."""
    _ensure_user()
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    """Relay the travel query to the FastAPI backend with the session user_id."""
    data = request.get_json(force=True)
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    user_id = _ensure_user()

    try:
        response = requests.post(
            f"{FASTAPI_URL}/query",
            json={"question": question, "user_id": user_id},
            timeout=300,  # complex trips can take 2-3 minutes
        )

        # Forward FastAPI response (both success and error)
        try:
            body = response.json()
        except ValueError:
            body = {"error": response.text}

        if response.ok:
            return jsonify(body)
        else:
            # Return the real error message from FastAPI
            err_msg = body.get("error", f"Backend returned {response.status_code}")
            return jsonify({"error": err_msg}), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Could not connect to the AI backend. "
                     "Please ensure the FastAPI server is running on port 8000."
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "The AI agent took too long to respond. Please try again."
        }), 504
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ── Preferences ────────────────────────────────────────────────────────────

@app.route("/preferences", methods=["GET"])
def get_preferences():
    """Return the current user's preferences."""
    user_id = _ensure_user()
    try:
        resp = requests.get(f"{FASTAPI_URL}/preferences/{user_id}", timeout=10)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/preferences", methods=["POST"])
def set_preference():
    """Save a user preference."""
    data = request.get_json(force=True)
    user_id = _ensure_user()
    try:
        resp = requests.post(
            f"{FASTAPI_URL}/preferences",
            json={"user_id": user_id, "key": data["key"], "value": data["value"]},
            timeout=10,
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ── PDF Export ─────────────────────────────────────────────────────────────

@app.route("/export_pdf", methods=["POST"])
def export_pdf():
    """Convert markdown content to a branded PDF and send as download."""
    data = request.get_json(force=True)
    content = (data or {}).get("content", "").strip()

    if not content:
        return jsonify({"error": "No content provided."}), 400

    try:
        from utils.pdf_generator import generate_pdf
        pdf_bytes = generate_pdf(content)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="travel_plan.pdf",
        )
    except ImportError as ie:
        return jsonify({"error": str(ie)}), 500
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
