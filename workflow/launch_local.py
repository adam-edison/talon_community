"""Open localhost with a given port in Brave browser."""

import subprocess

from talon import Module, app

mod = Module()


@mod.action_class
class UserActions:
    def launch_local(port: int):
        """Open http://localhost:<port>/app in Brave browser."""
        url = f"http://localhost:{port}/app"
        if app.platform == "mac":
            # Brave Browser is the standard app name on macOS
            subprocess.run(
                ["open", "-a", "Brave Browser", url],
                check=False,
                timeout=5,
            )
        elif app.platform == "linux":
            subprocess.run(
                ["xdg-open", url],
                check=False,
                timeout=5,
            )
        elif app.platform == "windows":
            subprocess.run(
                ["cmd", "/c", "start", "", url],
                check=False,
                timeout=5,
            )
        else:
            # Fallback: try opening with default browser
            import webbrowser

            webbrowser.open(url)

    def open_in_brave(url: str):
        """Open <url> in Brave browser."""
        if app.platform == "mac":
            subprocess.run(
                ["open", "-a", "Brave Browser", url],
                check=False,
                timeout=5,
            )
        elif app.platform == "linux":
            subprocess.run(
                ["xdg-open", url],
                check=False,
                timeout=5,
            )
        elif app.platform == "windows":
            subprocess.run(
                ["cmd", "/c", "start", "", url],
                check=False,
                timeout=5,
            )
        else:
            import webbrowser

            webbrowser.open(url)
