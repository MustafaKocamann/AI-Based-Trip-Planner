import os
import datetime


def save_document(content: str, filename: str = None) -> str:
    """
    Save a travel plan document to the outputs/ directory.

    Args:
        content:  The text content to save.
        filename: Optional file name (without extension). Defaults to a
                  timestamp-based name.

    Returns:
        The absolute path of the saved file.
    """
    outputs_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs"
    )
    os.makedirs(outputs_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}"

    # Sanitize filename
    safe_filename = "".join(
        c if c.isalnum() or c in ("_", "-") else "_" for c in filename
    )
    file_path = os.path.join(outputs_dir, f"{safe_filename}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path