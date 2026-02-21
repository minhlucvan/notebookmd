"""Unit tests for the notebookmd plugin system."""

import pytest
from notebookmd import Notebook, NotebookConfig
from notebookmd.plugins import (
    PluginSpec,
    clear_registry,
    get_registered_plugins,
    load_default_plugins,
    register_plugin,
    unregister_plugin,
)
from notebookmd.plugins_builtin import (
    BUILTIN_PLUGINS,
    AnalyticsPlugin,
    ChartPlugin,
    DataPlugin,
    LayoutPlugin,
    MediaPlugin,
    StatusPlugin,
    TextPlugin,
    UtilityPlugin,
)


# ── PluginSpec base class ─────────────────────────────────────────────────────


class TestPluginSpec:
    """Tests for PluginSpec base class."""

    def test_default_name_is_empty(self):
        """PluginSpec itself has no name."""
        assert PluginSpec.name == ""

    def test_get_methods_excludes_private(self):
        """Private methods (leading _) are not exposed."""

        class P(PluginSpec):
            name = "test"

            def public(self):
                pass

            def _private(self):
                pass

        p = P()
        methods = p.get_methods()
        assert "public" in methods
        assert "_private" not in methods

    def test_get_methods_excludes_base_attrs(self):
        """Base class attrs like get_methods itself are excluded."""

        class P(PluginSpec):
            name = "test"

            def custom(self):
                pass

        p = P()
        methods = p.get_methods()
        assert "custom" in methods
        assert "get_methods" not in methods

    def test_get_methods_returns_callables_only(self):
        """Non-callable attributes are excluded."""

        class P(PluginSpec):
            name = "test"
            some_data = 42

            def method(self):
                pass

        p = P()
        methods = p.get_methods()
        assert "method" in methods
        assert "some_data" not in methods


# ── Global Registry ───────────────────────────────────────────────────────────


class TestGlobalRegistry:
    """Tests for the global plugin registry."""

    def setup_method(self):
        """Save and clear registry before each test."""
        self._saved = get_registered_plugins()
        clear_registry()

    def teardown_method(self):
        """Restore registry after each test."""
        clear_registry()
        for name, cls in self._saved.items():
            register_plugin(cls)

    def test_register_plugin(self):
        """register_plugin adds to registry."""

        class P(PluginSpec):
            name = "test_reg"

        register_plugin(P)
        assert "test_reg" in get_registered_plugins()

    def test_register_non_pluginspec_raises(self):
        """Non-PluginSpec classes raise TypeError."""
        with pytest.raises(TypeError):
            register_plugin(str)  # type: ignore

    def test_register_no_name_raises(self):
        """Plugins without a name raise ValueError."""

        class P(PluginSpec):
            pass  # name defaults to ""

        with pytest.raises(ValueError):
            register_plugin(P)

    def test_unregister_plugin(self):
        """unregister_plugin removes from registry."""

        class P(PluginSpec):
            name = "to_remove"

        register_plugin(P)
        assert "to_remove" in get_registered_plugins()
        unregister_plugin("to_remove")
        assert "to_remove" not in get_registered_plugins()

    def test_unregister_nonexistent_is_noop(self):
        """Unregistering a non-existent plugin doesn't raise."""
        unregister_plugin("nonexistent")

    def test_clear_registry(self):
        """clear_registry empties the registry."""

        class P(PluginSpec):
            name = "test_clear"

        register_plugin(P)
        clear_registry()
        assert len(get_registered_plugins()) == 0

    def test_get_registered_returns_copy(self):
        """Modifying the returned dict doesn't affect the actual registry."""

        class P(PluginSpec):
            name = "test_copy"

        register_plugin(P)
        copy = get_registered_plugins()
        copy.clear()
        assert "test_copy" in get_registered_plugins()


# ── Built-in Plugins ─────────────────────────────────────────────────────────


class TestBuiltinPlugins:
    """Tests that built-in plugins are correctly structured."""

    def test_all_builtins_have_names(self):
        """Every built-in plugin has a non-empty name."""
        for plugin_cls in BUILTIN_PLUGINS:
            assert plugin_cls.name, f"{plugin_cls.__name__} has no name"

    def test_all_builtins_have_unique_names(self):
        """No two built-in plugins share a name."""
        names = [p.name for p in BUILTIN_PLUGINS]
        assert len(names) == len(set(names))

    def test_builtin_count(self):
        """There are 8 built-in plugins."""
        assert len(BUILTIN_PLUGINS) == 8

    def test_text_plugin_methods(self):
        """TextPlugin exposes expected methods."""
        p = TextPlugin()
        methods = p.get_methods()
        for m in ["title", "header", "subheader", "caption", "md", "note", "code", "text", "latex", "divider"]:
            assert m in methods, f"TextPlugin missing {m}"

    def test_data_plugin_methods(self):
        """DataPlugin exposes expected methods."""
        p = DataPlugin()
        methods = p.get_methods()
        for m in ["table", "dataframe", "metric", "metric_row", "json", "kv", "summary"]:
            assert m in methods, f"DataPlugin missing {m}"

    def test_chart_plugin_methods(self):
        """ChartPlugin exposes expected methods."""
        p = ChartPlugin()
        methods = p.get_methods()
        for m in ["line_chart", "area_chart", "bar_chart", "figure", "plotly_chart", "altair_chart"]:
            assert m in methods, f"ChartPlugin missing {m}"

    def test_status_plugin_methods(self):
        """StatusPlugin exposes expected methods."""
        p = StatusPlugin()
        methods = p.get_methods()
        for m in ["success", "error", "warning", "info", "exception", "progress", "toast", "balloons", "snow"]:
            assert m in methods, f"StatusPlugin missing {m}"

    def test_layout_plugin_methods(self):
        """LayoutPlugin exposes expected methods."""
        p = LayoutPlugin()
        methods = p.get_methods()
        for m in ["expander", "container", "tabs", "columns"]:
            assert m in methods, f"LayoutPlugin missing {m}"

    def test_media_plugin_methods(self):
        """MediaPlugin exposes expected methods."""
        p = MediaPlugin()
        methods = p.get_methods()
        for m in ["image", "audio", "video"]:
            assert m in methods, f"MediaPlugin missing {m}"

    def test_analytics_plugin_methods(self):
        """AnalyticsPlugin exposes expected methods."""
        p = AnalyticsPlugin()
        methods = p.get_methods()
        for m in ["stat", "stats", "badge", "change", "ranking"]:
            assert m in methods, f"AnalyticsPlugin missing {m}"

    def test_utility_plugin_methods(self):
        """UtilityPlugin exposes expected methods."""
        p = UtilityPlugin()
        methods = p.get_methods()
        for m in ["write", "echo", "empty", "connection_status", "export_csv"]:
            assert m in methods, f"UtilityPlugin missing {m}"


# ── Notebook.use() ────────────────────────────────────────────────────────────


class TestNotebookUse:
    """Tests for the Notebook.use() method."""

    def test_use_adds_methods(self, tmp_path):
        """Plugin methods become available on the notebook."""

        class Greeter(PluginSpec):
            name = "greeter"

            def greet(self, msg: str) -> None:
                self._w(f"> Hello: {msg}\n\n")

        n = Notebook(out_md=str(tmp_path / "test.md"))
        n.use(Greeter)

        assert hasattr(n, "greet")
        n.greet("world")
        md = n.to_markdown()
        assert "> Hello: world" in md

    def test_use_non_plugin_raises(self, tmp_path):
        """Passing a non-PluginSpec class raises TypeError."""
        n = Notebook(out_md=str(tmp_path / "test.md"))
        with pytest.raises(TypeError):
            n.use(str)  # type: ignore

    def test_use_overwrites_existing_method(self, tmp_path):
        """Later plugins can override methods from earlier plugins."""

        class CustomHeader(PluginSpec):
            name = "custom_header"

            def header(self, text: str, anchor: str | None = None, divider: bool = False) -> None:
                self._ensure_started()
                self._w(f"## CUSTOM: {text}\n\n")

        n = Notebook(out_md=str(tmp_path / "test.md"))
        n.use(CustomHeader)

        n.header("Test")
        md = n.to_markdown()
        assert "## CUSTOM: Test" in md

    def test_use_multiple_plugins(self, tmp_path):
        """Multiple plugins can be loaded."""

        class PluginA(PluginSpec):
            name = "plugin_a"

            def method_a(self) -> None:
                self._w("A\n\n")

        class PluginB(PluginSpec):
            name = "plugin_b"

            def method_b(self) -> None:
                self._w("B\n\n")

        n = Notebook(out_md=str(tmp_path / "test.md"))
        n.use(PluginA)
        n.use(PluginB)

        n.method_a()
        n.method_b()
        md = n.to_markdown()
        assert "A" in md
        assert "B" in md

    def test_get_plugins(self, tmp_path):
        """get_plugins returns loaded plugins."""
        n = Notebook(out_md=str(tmp_path / "test.md"))
        plugins = n.get_plugins()

        # All built-in plugins should be loaded
        assert "text" in plugins
        assert "data" in plugins
        assert "charts" in plugins
        assert "status" in plugins
        assert "layout" in plugins
        assert "media" in plugins
        assert "analytics" in plugins
        assert "utility" in plugins


# ── Plugin methods work correctly via Notebook ────────────────────────────────


class TestPluginMethodsViaNotebook:
    """Test that plugin-provided methods work correctly when called on Notebook."""

    def test_text_methods(self, tmp_path):
        """Text plugin methods render correctly."""
        n = Notebook(out_md=str(tmp_path / "test.md"))

        n.title("My Title")
        n.header("My Header")
        n.subheader("My Subheader")
        n.caption("My Caption")
        n.md("**Bold text**")
        n.note("A note")
        n.code("x = 1", lang="python")
        n.text("plain text")
        n.latex("E = mc^2")
        n.divider()

        md = n.to_markdown()
        assert "# My Title" in md
        assert "## My Header" in md
        assert "### My Subheader" in md
        assert "_My Caption_" in md
        assert "**Bold text**" in md
        assert "> **Note:** A note" in md
        assert "```python" in md
        assert "```text" in md
        assert "$$" in md
        assert "---" in md

    def test_data_methods(self, tmp_path):
        """Data plugin methods render correctly."""
        n = Notebook(out_md=str(tmp_path / "test.md"))

        n.metric("Revenue", "$1.2M", delta="+12%")
        n.metric_row([{"label": "A", "value": "1"}, {"label": "B", "value": "2"}])
        n.json({"key": "value"})
        n.kv({"Name": "Alice"}, title="Info")

        md = n.to_markdown()
        assert "Revenue" in md
        assert "$1.2M" in md
        assert '"key"' in md
        assert "#### Info" in md

    def test_status_methods(self, tmp_path):
        """Status plugin methods render correctly."""
        n = Notebook(out_md=str(tmp_path / "test.md"))

        n.success("Done!")
        n.error("Failed!")
        n.warning("Watch out!")
        n.info("FYI")
        n.progress(0.5, text="Loading")
        n.toast("Notification")

        md = n.to_markdown()
        assert "Done!" in md
        assert "Failed!" in md
        assert "Watch out!" in md
        assert "FYI" in md
        assert "50%" in md
        assert "Notification" in md

    def test_layout_methods(self, tmp_path):
        """Layout plugin methods render correctly."""
        n = Notebook(out_md=str(tmp_path / "test.md"))

        with n.expander("Details"):
            n.md("Hidden content")

        md = n.to_markdown()
        assert "<details>" in md
        assert "Details" in md
        assert "Hidden content" in md
        assert "</details>" in md

    def test_analytics_methods(self, tmp_path):
        """Analytics plugin methods render correctly."""
        n = Notebook(out_md=str(tmp_path / "test.md"))

        n.stat("P/E", 15.2, fmt=".1f")
        n.badge("BULLISH", style="success")
        n.change("Revenue", 120, 100, fmt=".0f")
        n.ranking("Score", 95, rank=1, total=100)

        md = n.to_markdown()
        assert "P/E" in md
        assert "15.2" in md
        assert "BULLISH" in md
        assert "Revenue" in md
        assert "Score" in md
        assert "#1 of 100" in md

    def test_utility_methods(self, tmp_path):
        """Utility plugin methods render correctly."""
        n = Notebook(out_md=str(tmp_path / "test.md"))

        n.write("Some text", 42, {"a": 1})
        n.echo("print(1)", output="1")
        n.connection_status("DB", status="connected")

        md = n.to_markdown()
        assert "Some text" in md
        assert "**42**" in md
        assert "print(1)" in md
        assert "DB" in md
        assert "connected" in md


# ── Custom community-style plugin ────────────────────────────────────────────


class TestCustomPlugin:
    """Test creating and using a custom plugin like a community plugin would."""

    def test_custom_analysis_plugin(self, tmp_path):
        """A custom analysis plugin can add domain-specific methods."""

        class FinancePlugin(PluginSpec):
            name = "finance"

            def pe_ratio(self, price: float, earnings: float) -> None:
                ratio = price / earnings if earnings else float("inf")
                self._w(f"**P/E Ratio:** {ratio:.1f}x\n\n")

            def market_cap(self, price: float, shares: int) -> None:
                cap = price * shares
                self._w(f"**Market Cap:** ${cap:,.0f}\n\n")

        n = Notebook(out_md=str(tmp_path / "test.md"))
        n.use(FinancePlugin)

        n.section("Valuation")
        n.pe_ratio(150.0, 10.0)
        n.market_cap(150.0, 1_000_000)

        md = n.to_markdown()
        assert "**P/E Ratio:** 15.0x" in md
        assert "**Market Cap:** $150,000,000" in md

    def test_plugin_can_access_notebook_internals(self, tmp_path):
        """Plugins can access _asset_mgr, cfg, etc."""

        class ConfigAwarePlugin(PluginSpec):
            name = "config_aware"

            def show_config(self) -> None:
                self._w(f"Max rows: {self.cfg.max_table_rows}\n\n")

        n = Notebook(out_md=str(tmp_path / "test.md"), cfg=NotebookConfig(max_table_rows=50))
        n.use(ConfigAwarePlugin)
        n.show_config()

        md = n.to_markdown()
        assert "Max rows: 50" in md

    def test_plugin_can_use_ensure_started(self, tmp_path):
        """Plugins can call _ensure_started to trigger lazy init."""

        class EagerPlugin(PluginSpec):
            name = "eager"

            def eager_write(self, text: str) -> None:
                self._ensure_started()
                self._w(f"{text}\n\n")

        n = Notebook(out_md=str(tmp_path / "test.md"), title="Eager Test")
        n.use(EagerPlugin)
        n.eager_write("Hello")

        md = n.to_markdown()
        assert "# Eager Test" in md
        assert "Hello" in md


# ── Global registration affects new notebooks ────────────────────────────────


class TestGlobalRegistrationEffectsOnNotebook:
    """Test that globally registered plugins auto-load into new Notebooks."""

    def setup_method(self):
        self._saved = get_registered_plugins()

    def teardown_method(self):
        clear_registry()
        for name, cls in self._saved.items():
            register_plugin(cls)

    def test_globally_registered_plugin_available(self, tmp_path):
        """Plugins registered globally are available on new notebooks."""

        class GlobalPlugin(PluginSpec):
            name = "global_test"

            def global_method(self) -> None:
                self._w("GLOBAL\n\n")

        register_plugin(GlobalPlugin)

        n = Notebook(out_md=str(tmp_path / "test.md"))
        assert hasattr(n, "global_method")
        n.global_method()
        md = n.to_markdown()
        assert "GLOBAL" in md


# ── load_default_plugins ──────────────────────────────────────────────────────


class TestLoadDefaultPlugins:
    """Tests for the load_default_plugins function."""

    def test_load_default_plugins_registers_builtins(self):
        """After load_default_plugins, all builtins are registered."""
        # load_default_plugins is already called by __init__.py
        registry = get_registered_plugins()
        for plugin_cls in BUILTIN_PLUGINS:
            assert plugin_cls.name in registry

    def test_load_default_plugins_idempotent(self):
        """Calling load_default_plugins multiple times is safe."""
        load_default_plugins()
        load_default_plugins()
        registry = get_registered_plugins()
        # Still exactly the expected plugins
        for plugin_cls in BUILTIN_PLUGINS:
            assert plugin_cls.name in registry
