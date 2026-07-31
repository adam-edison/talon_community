import talon

if hasattr(talon, "test_mode"):
    # Only include this when we're running tests

    from workflow.task_text.mark_status import find_checkbox

    def test_dash_checkbox():
        match = find_checkbox("- [ ] buy milk")

        assert match.group(2) == " "

    def test_star_checkbox():
        match = find_checkbox("* [ ] buy milk")

        assert match.group(2) == " "

    def test_plain_checkbox():
        match = find_checkbox("[ ] buy milk")

        assert match.group(2) == " "

    def test_indented_checkbox():
        match = find_checkbox("   [ ] buy milk")

        assert match.group(2) == " "

    def test_indented_dash_checkbox():
        match = find_checkbox("    - [ ] buy milk")

        assert match.group(2) == " "

    def test_checked_checkbox():
        match = find_checkbox("- [x] buy milk")

        assert match.group(2) == "x"

    def test_no_checkbox():
        match = find_checkbox("- buy milk")

        assert match is None

    def test_checkbox_only_at_line_start():
        match = find_checkbox("buy milk [ ] today")

        assert match is None

    def test_checkbox_state_position():
        match = find_checkbox("- [ ] buy milk")

        assert match.end() - 2 == 3
