"""
Per-app sound scroll speeds, read from and written to a CSV file.

Each CSV row holds an app name and its scroll speed. These helpers have no
Talon dependencies so they can be unit tested.
"""

import csv
from pathlib import Path

DEFAULT_SCROLL_SPEED = 8.0
MIN_SCROLL_SPEED = 0.5
MAX_SCROLL_SPEED = 32.0


def clamp_scroll_speed(speed: float) -> float:
    return max(MIN_SCROLL_SPEED, min(MAX_SCROLL_SPEED, speed))


def parse_scroll_speed(text: str) -> float | None:
    try:
        speed = float(text)
    except ValueError:
        return None

    return clamp_scroll_speed(speed)


def parse_scroll_speeds(rows: dict[str, str]) -> dict[str, float]:
    parsed = {app_name: parse_scroll_speed(text) for app_name, text in rows.items()}
    return {app_name: speed for app_name, speed in parsed.items() if speed is not None}


def format_scroll_speed(speed: float) -> str:
    return f"{speed:g}"


def _scroll_speed_rows(speeds: dict[str, float]) -> list[list[str]]:
    return [[app_name, format_scroll_speed(speed)] for app_name, speed in speeds.items()]


def write_scroll_speeds(
    path: Path, headers: tuple[str, str], speeds: dict[str, float]
) -> None:
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(_scroll_speed_rows(speeds))
