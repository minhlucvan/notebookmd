"""Integration tests for asset management end-to-end."""

from pathlib import Path

import pytest

from notebookmd import Notebook


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_figure_saved_to_assets_dir(tmp_path, sample_figure):
    """Test figure saved in assets/ subdirectory."""
    N = Notebook(out_md=str(tmp_path / "report.md"))

    N.section("Chart")
    N.figure(sample_figure, "chart.png")

    N.save()

    # Verify figure in assets directory
    assets_dir = tmp_path / "assets"
    assert (assets_dir / "chart.png").exists()


@pytest.mark.integration
@pytest.mark.requires_pandas
def test_csv_saved_to_assets_dir(tmp_path, sample_df):
    """Test CSV saved in assets/ subdirectory."""
    N = Notebook(out_md=str(tmp_path / "report.md"))

    N.section("Data")
    N.export_csv(sample_df, "data.csv")

    N.save()

    # Verify CSV in assets directory
    assets_dir = tmp_path / "assets"
    assert (assets_dir / "data.csv").exists()


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_multiple_figures_tracked(tmp_path):
    """Test all figures in artifact index."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        N = Notebook(out_md=str(tmp_path / "report.md"))

        N.section("Multiple Charts")
        fig1, ax1 = plt.subplots()
        ax1.plot([1, 2, 3])
        N.figure(fig1, "chart1.png")

        fig2, ax2 = plt.subplots()
        ax2.plot([4, 5, 6])
        N.figure(fig2, "chart2.png")

        fig3, ax3 = plt.subplots()
        ax3.plot([7, 8, 9])
        N.figure(fig3, "chart3.png")

        result_path = N.save()
        content = result_path.read_text()

        assert "[chart1.png]" in content
        assert "[chart2.png]" in content
        assert "[chart3.png]" in content

    except ImportError:
        pytest.skip("matplotlib not installed")


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_relative_paths_correct(tmp_path, sample_figure):
    """Test paths relative to markdown file work in rendered output."""
    out_path = tmp_path / "reports" / "analysis.md"

    N = Notebook(out_md=str(out_path))

    N.section("Chart")
    rel_path = N.figure(sample_figure, "plot.png")

    result_path = N.save()
    content = result_path.read_text()

    # Should have relative path from markdown file to asset
    assert "assets/plot.png" in content


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_artifact_deduplication(tmp_path, sample_figure):
    """Test same artifact registered once only."""
    N = Notebook(out_md=str(tmp_path / "report.md"))

    # Register same artifact multiple times
    N._asset_mgr.register("test.png")
    N._asset_mgr.register("test.png")
    N._asset_mgr.register("test.png")

    assert len(N._asset_mgr.artifacts) == 1


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_custom_assets_directory(tmp_path, sample_figure):
    """Test custom assets_dir parameter respected."""
    custom_assets = tmp_path / "my_custom_assets"

    N = Notebook(
        out_md=str(tmp_path / "report.md"),
        assets_dir=str(custom_assets),
    )

    N.section("Chart")
    N.figure(sample_figure, "chart.png")

    N.save()

    # Verify in custom directory
    assert (custom_assets / "chart.png").exists()


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_figure_filename_collision(tmp_path):
    """Test multiple figures with same name handled correctly."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        N = Notebook(out_md=str(tmp_path / "report.md"))

        N.section("Charts")
        fig1, ax1 = plt.subplots()
        ax1.plot([1, 2, 3])
        path1 = N.figure(fig1, "chart.png")

        # Save another with same name (should overwrite or handle)
        fig2, ax2 = plt.subplots()
        ax2.plot([4, 5, 6])
        path2 = N.figure(fig2, "chart.png")

        N.save()

        # Both should complete without error
        assert Path(tmp_path / "assets" / "chart.png").exists()

    except ImportError:
        pytest.skip("matplotlib not installed")


@pytest.mark.integration
@pytest.mark.requires_matplotlib
def test_artifact_index_ordering(tmp_path, sample_figure, sample_df):
    """Test artifacts listed in registration order."""
    N = Notebook(out_md=str(tmp_path / "report.md"))

    N.section("Assets")
    N.figure(sample_figure, "first.png")
    N.export_csv(sample_df, "second.csv")

    result_path = N.save()
    content = result_path.read_text()

    # Find positions in output
    first_pos = content.find("[first.png]")
    second_pos = content.find("[second.csv]")

    # Should be in order
    assert first_pos < second_pos
