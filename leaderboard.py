"""Leaderboard persistence - top 10 scores."""

import json
import os
from settings import LEADERBOARD_FILE, LEADERBOARD_MAX, DIFF_NAMES


def load_leaderboard():
    """Load leaderboard from file. Returns list of {name, score, difficulty}."""
    if not os.path.exists(LEADERBOARD_FILE):
        return _default_leaderboard()
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
        if not data:
            return _default_leaderboard()
        return data[:LEADERBOARD_MAX]
    except (json.JSONDecodeError, IOError):
        return _default_leaderboard()


def _default_leaderboard():
    """Generate default top 10 with random 3-char names, scores 1000-10000."""
    import random as _r
    _r.seed(42)  # deterministic defaults
    names = []
    for _ in range(LEADERBOARD_MAX):
        name = "".join(_r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(3))
        names.append(name)
    entries = []
    for i in range(LEADERBOARD_MAX):
        entries.append({
            "name": names[i],
            "score": (LEADERBOARD_MAX - i) * 1000,
            "difficulty": "EASY"
        })
    save_leaderboard(entries)
    return entries


def save_leaderboard(entries):
    """Save leaderboard to file."""
    entries = sorted(entries, key=lambda e: e["score"], reverse=True)[:LEADERBOARD_MAX]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def is_high_score(score):
    """Check if score qualifies for leaderboard."""
    entries = load_leaderboard()
    if len(entries) < LEADERBOARD_MAX:
        return True
    return score > entries[-1]["score"]


def add_score(name, score, difficulty):
    """Add a new score entry."""
    entries = load_leaderboard()
    entries.append({"name": name, "score": score, "difficulty": DIFF_NAMES[difficulty]})
    save_leaderboard(entries)
