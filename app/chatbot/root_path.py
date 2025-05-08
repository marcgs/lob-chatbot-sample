from pathlib import Path


def root_path() -> Path:
    """Return the root path of the project."""
    return Path(__file__).parent.parent


def chatbot_root_path() -> Path:
    """Return the root path of the chatbot app."""
    return Path(__file__).parent
