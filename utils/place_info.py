import os
import requests
from dotenv import load_dotenv

load_dotenv()


class PlaceInfo:
    """
    Searches for places using the Google Places API and enriches results
    with ratings, review counts, coordinates, and top reviews.
    """

    TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    def __init__(self) -> None:
        self.api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.api_key:
            raise EnvironmentError(
                "GOOGLE_PLACES_API_KEY is not set in environment variables."
            )

    # ── Text Search (enriched) ────────────────────────────────────────────

    def search(self, query: str, location: str = "") -> list[dict]:
        """
        Search for places and return enriched structured JSON.

        Returns list of dicts with keys:
            name, address, rating, user_ratings_total,
            latitude, longitude, types, place_id
        """
        full_query = f"{query} in {location}".strip(" in") if location else query

        params = {
            "query": full_query,
            "key": self.api_key,
        }
        response = requests.get(self.TEXT_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        for place in data.get("results", [])[:10]:
            geo = place.get("geometry", {}).get("location", {})
            results.append(
                {
                    "name": place.get("name", ""),
                    "address": place.get("formatted_address", ""),
                    "rating": place.get("rating", None),
                    "user_ratings_total": place.get("user_ratings_total", 0),
                    "latitude": geo.get("lat", None),
                    "longitude": geo.get("lng", None),
                    "types": place.get("types", []),
                    "place_id": place.get("place_id", ""),
                }
            )
        return results

    # ── Place Details (top review) ────────────────────────────────────────

    def get_place_details(self, place_id: str) -> dict:
        """
        Fetch details for a single place including the top review.

        Returns dict with: name, rating, user_ratings_total,
                           latitude, longitude, top_review.
        """
        params = {
            "place_id": place_id,
            "fields": "name,rating,user_ratings_total,geometry,reviews",
            "key": self.api_key,
        }

        try:
            response = requests.get(self.DETAILS_URL, params=params, timeout=10)
            response.raise_for_status()
            result = response.json().get("result", {})
        except Exception:
            return {}

        geo = result.get("geometry", {}).get("location", {})
        reviews = result.get("reviews", [])
        top_review = reviews[0].get("text", "") if reviews else ""

        return {
            "name": result.get("name", ""),
            "rating": result.get("rating", None),
            "user_ratings_total": result.get("user_ratings_total", 0),
            "latitude": geo.get("lat", None),
            "longitude": geo.get("lng", None),
            "top_review": top_review,
        }