from __future__ import annotations

from langchain_core.tools import tool

from utils.place_info import PlaceInfo


def _get_place_info() -> PlaceInfo:
    """Lazily create the PlaceInfo singleton."""
    return PlaceInfo()


@tool
def search_places(query: str, location: str = "") -> list:
    """
    Search for places, attractions, hotels, or restaurants relevant to a trip.

    Args:
        query:    What to search for (e.g. 'top restaurants', 'museums').
        location: City or region to narrow the search (e.g. 'Rome, Italy').

    Returns:
        List of up to 10 places as structured JSON. Each entry contains:
        name, address, rating, user_ratings_total, latitude, longitude,
        types, and place_id. Use latitude/longitude for mapping.
    """
    return _get_place_info().search(query, location)


@tool
def get_place_details(place_id: str) -> dict:
    """
    Get detailed information about a specific place including its top review.

    Args:
        place_id: The Google Places place_id returned by search_places.

    Returns:
        Dict with name, rating, user_ratings_total, latitude, longitude,
        and top_review text.
    """
    return _get_place_info().get_place_details(place_id)