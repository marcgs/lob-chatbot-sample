from pathlib import Path


def chatbot_eval_root_path() -> Path:
    """Return the root path of the project."""
    return Path(__file__).parent
