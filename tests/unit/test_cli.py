"""Tests for notebookmd.cli module."""

from notebookmd.cli import _build_parser, _file_hash, main


class TestParser:
    def test_no_args_returns_zero(self):
        assert main([]) == 0

    def test_version_command(self, capsys):
        result = main(["version"])
        assert result == 0
        captured = capsys.readouterr()
        assert "notebookmd" in captured.out

    def test_run_missing_script(self, tmp_path):
        result = main(["run", str(tmp_path / "missing.py")])
        assert result == 1

    def test_run_not_py_file(self, tmp_path):
        txt_file = tmp_path / "report.txt"
        txt_file.write_text("hello")
        result = main(["run", str(txt_file)])
        assert result == 1

    def test_run_invalid_var(self, tmp_path):
        script = tmp_path / "test.py"
        script.write_text("x = 1")
        result = main(["run", str(script), "--var", "no_equals_sign"])
        assert result == 1

    def test_run_simple_script(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "out.md"
        script.write_text(f'from notebookmd import nb\nn = nb("{out}", title="Test")\nn.header("Hello")\nn.save()\n')
        result = main(["run", str(script)])
        assert result == 0
        assert out.exists()

    def test_run_with_variables(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "out.md"
        script.write_text(
            f"import os\n"
            f"from notebookmd import nb\n"
            f'ticker = os.environ.get("NOTEBOOKMD_VAR_TICKER", "DEFAULT")\n'
            f'n = nb("{out}", title=ticker)\n'
            f"n.save()\n"
        )
        result = main(["run", str(script), "--var", "ticker=AAPL"])
        assert result == 0
        content = out.read_text()
        assert "AAPL" in content

    def test_run_with_live(self, tmp_path):
        script = tmp_path / "test.py"
        out = tmp_path / "out.md"
        script.write_text(
            f'from notebookmd import nb\nn = nb("{out}", title="LiveTest")\nn.header("Hello")\nn.save()\n'
        )
        result = main(["run", str(script), "--live"])
        assert result == 0

    def test_run_script_with_error(self, tmp_path):
        script = tmp_path / "bad.py"
        script.write_text("raise ValueError('boom')")
        result = main(["run", str(script)])
        assert result == 1


class TestCacheCommands:
    def test_cache_show(self, tmp_path):
        result = main(["cache", "show", "--cache-dir", str(tmp_path / "cache")])
        assert result == 0

    def test_cache_clear(self, tmp_path):
        result = main(["cache", "clear", "--cache-dir", str(tmp_path / "cache")])
        assert result == 0

    def test_cache_clear_data_only(self, tmp_path):
        result = main(["cache", "clear", "--data-only", "--cache-dir", str(tmp_path / "cache")])
        assert result == 0


class TestFileHash:
    def test_hash_consistent(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello")
        h1 = _file_hash(f)
        h2 = _file_hash(f)
        assert h1 == h2

    def test_hash_changes_on_content_change(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello")
        h1 = _file_hash(f)
        f.write_text("world")
        h2 = _file_hash(f)
        assert h1 != h2

    def test_hash_missing_file(self, tmp_path):
        h = _file_hash(tmp_path / "missing.txt")
        assert h == ""


class TestParserBuild:
    def test_parser_has_subcommands(self):
        parser = _build_parser()
        # Basic structure test
        assert parser.prog == "notebookmd"

    def test_run_subcommand_defaults(self):
        parser = _build_parser()
        args = parser.parse_args(["run", "script.py"])
        assert args.script == "script.py"
        assert args.live is False
        assert args.watch is False
        assert args.no_cache is False
        assert args.log_level == "INFO"

    def test_run_with_all_flags(self):
        parser = _build_parser()
        args = parser.parse_args(
            [
                "run",
                "script.py",
                "--live",
                "--watch",
                "--output",
                "out.md",
                "--var",
                "x=1",
                "--var",
                "y=2",
                "--cache-dir",
                "/tmp/cache",
                "--no-cache",
                "--log-level",
                "DEBUG",
            ]
        )
        assert args.live is True
        assert args.watch is True
        assert args.output == "out.md"
        assert args.var == ["x=1", "y=2"]
        assert args.cache_dir == "/tmp/cache"
        assert args.no_cache is True
        assert args.log_level == "DEBUG"
