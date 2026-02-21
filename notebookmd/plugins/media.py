"""Media elements plugin: image, audio, video."""

from __future__ import annotations

from typing import Any

from ._base import PluginSpec


class MediaPlugin(PluginSpec):
    """Media elements: image, audio, video."""

    name = "media"
    version = "0.3.0"

    def image(
        self,
        source: Any,
        caption: str = "",
        width: int | None = None,
        filename: str | None = None,
    ) -> str:
        """Display an image (like st.image).

        Supports file paths, URLs, or raw image data (PIL/numpy).

        Returns:
            Path or URL to the image.
        """
        from ..widgets import render_image

        if isinstance(source, str):
            self._w(render_image(source, caption=caption, width=width))
            return source

        fname = filename or f"image_{self._next_id()}.png"
        rel = self._asset_mgr.save_image(source, fname)
        self._w(render_image(rel, caption=caption, width=width))
        return rel

    def audio(self, source: str, caption: str = "") -> None:
        """Display an audio player link (like st.audio)."""
        from ..widgets import render_audio

        self._w(render_audio(source, caption=caption))

    def video(self, source: str, caption: str = "") -> None:
        """Display a video link (like st.video)."""
        from ..widgets import render_video

        self._w(render_video(source, caption=caption))
