"""Tests for notebookmd.runner module."""

import os
from io import StringIO

from notebookmd.runner import LiveWriter, RunConfig, Runner, RunResult, RunStatus

# ---------------------------------------------------------------------------
# RunResult
# ---------------------------------------------------------------------------


class TestRunResult:
    def test_success_result(self):
        r = RunResult(status=RunStatus.SUCCESS, script="test.py", duration_seconds=1.5)
        assert r.ok is True
        assert "[OK]" in r.summary()

    def test_error_result(self):
        r = RunResult(status=RunStatus.ERROR, script="test.py", error="boom")
        assert r.ok is False
        assert "[FAIL]" in r.summary()
        assert "boom" in r.summary()

    def test_interrupted_result(self):
        r = RunResult(status=RunStatus.INTERRUPTED, script="test.py")
        assert r.ok is False
        assert "[INTERRUPTED]" in r.summary()

    def test_summary_with_artifacts(self):
        r = RunResult(
            status=RunStatus.SUCCESS,
            script="test.py",
            output_path="out.md",
            artifacts=["fig1.png", "fig2.png"],
        )
        s = r.summary()
        assert "out.md" in s
        assert "2 file(s)" in s


# ---------------------------------------------------------------------------
# RunConfig
# ---------------------------------------------------------------------------


class TestRunConfig:
    def test_defaults(self):
        cfg = RunConfig()
        assert cfg.live is False
        assert cfg.output is None
        assert cfg.variables == {}
        assert cfg.no_cache is False
        assert cfg.log_level == "INFO"

    def test_custom(self):
        cfg = RunConfig(live=True, variables={"x": "1"})
        assert cfg.live is True
        assert cfg.variables == {"x": "1"}


# ---------------------------------------------------------------------------
# LiveWriter
# ---------------------------------------------------------------------------


class TestLiveWriter:
    def test_writes_to_stream(self):
        stream = StringIO()
        writer = LiveWriter(stream=stream)
        writer.on_write("# Hello\n\n")
        writer.on_write("Some text\n")
        assert stream.getvalue() == "# Hello\n\nSome text\n"

    def test_tracks_bytes(self):
        stream = StringIO()
        writer = LiveWriter(stream=stream)
        writer.on_write("hello")
        assert writer.total_bytes == 5
        assert writer.chunk_count == 1


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


class TestRunner:
    def test_execute_missing_script(self, tmp_path):
        runner = Runner(RunConfig())
        result = runner.execute(str(tmp_path / "missing.py"))
        assert result.status == RunStatus.ERROR
        assert "not found" in result.error

    def test_execute_non_py_file(self, tmp_path):
        f = tmp_path / "report.txt"
        f.write_text("hello")
        runner = Runner(RunConfig())
        result = runner.execute(str(f))
        assert result.status == RunStatus.ERROR
        assert ".txt" in result.error

    def test_execute_simple_script(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "out.md"
        script.write_text(f'from notebookmd import nb\nn = nb("{out}", title="Test")\nn.header("Hello")\nn.save()\n')
        runner = Runner(RunConfig())
        result = runner.execute(str(script))
        assert result.status == RunStatus.SUCCESS
        assert result.duration_seconds > 0
        assert out.exists()

    def test_execute_script_with_error(self, tmp_path):
        script = tmp_path / "bad.py"
        script.write_text("raise ValueError('test error')")
        runner = Runner(RunConfig())
        result = runner.execute(str(script))
        assert result.status == RunStatus.ERROR
        assert "test error" in result.error
        assert result.traceback is not None

    def test_execute_with_variables(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "out.md"
        script.write_text(
            f"import os\n"
            f'ticker = os.environ.get("NOTEBOOKMD_VAR_TICKER", "DEFAULT")\n'
            f"from notebookmd import nb\n"
            f'n = nb("{out}", title=ticker)\n'
            f"n.save()\n"
        )
        runner = Runner(RunConfig(variables={"ticker": "MSFT"}))
        result = runner.execute(str(script))
        assert result.status == RunStatus.SUCCESS
        content = out.read_text()
        assert "MSFT" in content

    def test_execute_with_live_output(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "out.md"
        script.write_text(f'from notebookmd import nb\nn = nb("{out}", title="Live")\nn.header("Section")\nn.save()\n')
        stream = StringIO()
        runner = Runner(RunConfig(live=True, stream=stream))
        result = runner.execute(str(script))
        assert result.status == RunStatus.SUCCESS
        # Live output should have received the markdown chunks
        live_output = stream.getvalue()
        assert "Live" in live_output

    def test_execute_collects_output_path(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "report.md"
        script.write_text(f'from notebookmd import nb\nn = nb("{out}", title="Test")\nn.save()\n')
        runner = Runner(RunConfig())
        result = runner.execute(str(script))
        assert result.output_path is not None
        assert "report.md" in result.output_path

    def test_execute_with_no_cache(self, tmp_path):
        script = tmp_path / "test.py"
        script.write_text("x = 1")
        runner = Runner(RunConfig(no_cache=True))
        result = runner.execute(str(script))
        assert result.status == RunStatus.SUCCESS

    def test_restores_cwd(self, tmp_path):
        script = tmp_path / "test.py"
        script.write_text("import os")
        original_cwd = os.getcwd()
        runner = Runner(RunConfig())
        runner.execute(str(script))
        assert os.getcwd() == original_cwd

    def test_restores_cwd_on_error(self, tmp_path):
        script = tmp_path / "test.py"
        script.write_text("raise RuntimeError('fail')")
        original_cwd = os.getcwd()
        runner = Runner(RunConfig())
        runner.execute(str(script))
        assert os.getcwd() == original_cwd
