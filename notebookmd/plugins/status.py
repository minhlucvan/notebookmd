"""Status elements plugin: success, error, warning, info, exception, progress, toast, balloons, snow."""

from __future__ import annotations

from ._base import PluginSpec


class StatusPlugin(PluginSpec):
    """Status elements: success, error, warning, info, exception, progress, toast, balloons, snow."""

    name = "status"
    version = "0.3.0"

    def success(self, body: str, icon: str = "\u2705") -> None:
        """Emit a success message (like st.success)."""
        from ..widgets import render_success

        self._w(render_success(body, icon=icon))

    def error(self, body: str, icon: str = "\u274c") -> None:
        """Emit an error message (like st.error)."""
        from ..widgets import render_error

        self._w(render_error(body, icon=icon))

    def warning(self, body: str, icon: str = "\u26a0\ufe0f") -> None:
        """Emit a warning message (like st.warning)."""
        from ..widgets import render_warning

        self._w(render_warning(body, icon=icon))

    def info(self, body: str, icon: str = "\u2139\ufe0f") -> None:
        """Emit an info message (like st.info)."""
        from ..widgets import render_info

        self._w(render_info(body, icon=icon))

    def exception(self, exc: Exception) -> None:
        """Display an exception (like st.exception).

        Args:
            exc: The exception to display.
        """
        from ..widgets import render_exception

        self._w(render_exception(exc))

    def progress(self, value: float, text: str = "") -> None:
        """Emit a progress bar (like st.progress).

        Args:
            value: Progress from 0.0 to 1.0.
            text: Optional label text.
        """
        from ..widgets import render_progress

        self._w(render_progress(value, text=text))

    def toast(self, body: str, icon: str = "\U0001f514") -> None:
        """Emit a toast notification (like st.toast)."""
        from ..widgets import render_toast

        self._w(render_toast(body, icon=icon))

    def balloons(self) -> None:
        """Emit a balloons celebration marker (like st.balloons)."""
        from ..widgets import render_balloons

        self._w(render_balloons())

    def snow(self) -> None:
        """Emit a snow celebration marker (like st.snow)."""
        from ..widgets import render_snow

        self._w(render_snow())
