import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from core.user_settings import read_csv_list
    from workflow.sound_scroll_speeds import (
        parse_scroll_speeds,
        write_scroll_speeds,
    )

    HEADERS = ("App name", "Scroll speed")

    def test_parse_scroll_speeds_reads_numbers():
        rows = {"iTerm2": "4", "Google Chrome": "16.5"}

        assert parse_scroll_speeds(rows) == {"iTerm2": 4.0, "Google Chrome": 16.5}

    def test_parse_scroll_speeds_skips_rows_without_a_number():
        rows = {"iTerm2": "fast", "Slack": "Slack", "Google Chrome": "16"}

        assert parse_scroll_speeds(rows) == {"Google Chrome": 16.0}

    def test_parse_scroll_speeds_clamps_to_allowed_range():
        rows = {"iTerm2": "0", "Google Chrome": "99"}

        assert parse_scroll_speeds(rows) == {"iTerm2": 0.5, "Google Chrome": 32.0}

    def test_write_scroll_speeds_writes_headers_and_rows(tmp_path):
        path = tmp_path / "sound_scroll_speeds.csv"

        write_scroll_speeds(path, HEADERS, {"iTerm2": 4.0, "Google Chrome": 16.5})

        assert path.read_bytes() == (
            b"App name,Scroll speed\niTerm2,4\nGoogle Chrome,16.5\n"
        )

    def test_written_scroll_speeds_load_back_unchanged(tmp_path):
        path = tmp_path / "sound_scroll_speeds.csv"
        speeds = {"iTerm2": 4.0, "Visual Studio Code, Insiders": 12.0}

        write_scroll_speeds(path, HEADERS, speeds)
        with open(path, encoding="utf-8", newline="") as file:
            rows = read_csv_list(file, HEADERS, is_spoken_form_first=True)

        assert parse_scroll_speeds(rows) == speeds
