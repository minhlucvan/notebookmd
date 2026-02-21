"""Text elements plugin: title, header, subheader, caption, md, note, code, text, latex, divider."""

from __future__ import annotations

from ._base import PluginSpec


class TextPlugin(PluginSpec):
    """Text elements: title, header, subheader, caption, md, note, code, text, latex, divider."""

    name = "text"
    version = "0.3.0"

    def title(self, text: str, anchor: str | None = None) -> None:
        """Emit a title heading (like st.title).

        Args:
            text: Title text.
            anchor: Optional HTML anchor ID.
        """
        from ..widgets import render_title

        self._ensure_started()
        self._w(render_title(text, anchor=anchor))

    def header(self, text: str, anchor: str | None = None, divider: bool = False) -> None:
        """Emit a section header (like st.header).

        Args:
            text: Header text.
            anchor: Optional HTML anchor ID.
            divider: If True, add a horizontal rule below.
        """
        from ..widgets import render_header

        self._ensure_started()
        self._w(render_header(text, anchor=anchor, divider=divider))

    def subheader(self, text: str, anchor: str | None = None, divider: bool = False) -> None:
        """Emit a subheader (like st.subheader).

        Args:
            text: Subheader text.
            anchor: Optional HTML anchor ID.
            divider: If True, add a horizontal rule below.
        """
        from ..widgets import render_subheader

        self._ensure_started()
        self._w(render_subheader(text, anchor=anchor, divider=divider))

    def caption(self, text: str) -> None:
        """Emit small caption text (like st.caption).

        Args:
            text: Caption text.
        """
        from ..widgets import render_caption

        self._w(render_caption(text))

    def md(self, text: str) -> None:
        """Emit raw markdown text."""
        from ..emitters import render_md

        self._w(render_md(text))

    def note(self, text: str) -> None:
        """Emit a callout / note blockquote."""
        from ..emitters import render_note

        self._w(render_note(text))

    def code(self, source: str, lang: str = "python") -> None:
        """Emit a fenced code block."""
        from ..emitters import render_code

        self._w(render_code(source, lang))

    def text(self, body: str) -> None:
        """Emit fixed-width preformatted text (like st.text).

        Args:
            body: Plain text to render in monospace.
        """
        from ..widgets import render_text

        self._w(render_text(body))

    def latex(self, body: str) -> None:
        """Emit a LaTeX math expression (like st.latex).

        Args:
            body: LaTeX expression string.
        """
        from ..widgets import render_latex

        self._w(render_latex(body))

    def divider(self) -> None:
        """Emit a horizontal divider (like st.divider)."""
        from ..widgets import render_divider

        self._w(render_divider())
