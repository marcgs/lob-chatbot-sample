from pathlib import Path


def chatbot_root_path() -> Path:
    """Return the root path of the chatbot app."""
    return Path(__file__).parent
