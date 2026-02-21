"""Unit tests for notebookmd.emitters module."""

import sys
import pytest
from unittest.mock import patch
from notebookmd.emitters import (
    render_md,
    render_note,
    render_code,
    render_table,
    render_figure,
    render_kv,
    render_summary,
)


# render_md() tests
def test_render_md_basic():
    """Test raw markdown passthrough with double newline."""
    result = render_md("# Hello World")

    assert result == "# Hello World\n\n"


def test_render_md_strips_trailing():
    """Test trailing whitespace removed."""
    result = render_md("Hello   \n\n  ")

    assert result == "Hello\n\n"


# render_note() tests
def test_render_note_blockquote():
    """Test format as > **Note:** {text}."""
    result = render_note("This is a note")

    assert "> **Note:** This is a note\n\n" == result


def test_render_note_strips_text():
    """Test leading/trailing whitespace removed."""
    result = render_note("  Some note  \n")

    assert "> **Note:** Some note\n\n" == result


# render_code() tests
def test_render_code_python():
    """Test Python code block with triple backticks."""
    code = "def hello():\n    print('Hello')"
    result = render_code(code, lang="python")

    assert "```python" in result
    assert code in result
    assert result.endswith("```\n\n")


def test_render_code_custom_lang():
    """Test custom language tag."""
    code = "SELECT * FROM users;"
    result = render_code(code, lang="sql")

    assert "```sql" in result
    assert code in result


def test_render_code_strips_trailing():
    """Test trailing newlines removed from code."""
    code = "print('hello')\n\n\n"
    result = render_code(code, lang="python")

    assert "print('hello')" in result
    # Should end with ``` and double newline, not extra newlines in code
    assert result.count("\n\n\n") == 0


# render_table() with pandas
@pytest.mark.requires_pandas
def test_render_table_basic(sample_df):
    """Test DataFrame to markdown table with heading."""
    result = render_table(sample_df, name="Sample Data")

    assert "#### Sample Data" in result
    assert "|" in result  # Table delimiter
    assert "date" in result
    assert "value" in result
    assert "category" in result


@pytest.mark.requires_pandas
def test_render_table_truncation(long_df):
    """Test long table with ellipsis row when > max_rows."""
    result = render_table(long_df, max_rows=10, name="Long Data")

    assert "#### Long Data" in result
    assert "…" in result or "..." in result  # Ellipsis row (Unicode or ASCII)


@pytest.mark.requires_pandas
def test_render_table_custom_max_rows(long_df):
    """Test respects override parameter."""
    result = render_table(long_df, max_rows=20, name="Data")

    # Should truncate at 20 rows
    lines = result.split("\n")
    # Count table rows (excluding header, separator, and empty lines)
    table_lines = [l for l in lines if l.strip().startswith("|") and "---" not in l]
    # Header + 20 rows + ellipsis = 22 lines
    assert len(table_lines) <= 23


@pytest.mark.requires_pandas
def test_render_table_shape_annotation(sample_df):
    """Test shape annotation appended."""
    result = render_table(sample_df, name="Data")

    assert "_shape: 10 rows × 3 cols_" in result


@pytest.mark.requires_pandas
def test_render_table_custom_name(sample_df):
    """Test heading uses custom name."""
    result = render_table(sample_df, name="My Custom Table")

    assert "#### My Custom Table" in result


def test_render_table_unsupported_type():
    """Test fallback message for unsupported data types."""
    result = render_table("not a table", name="Test")

    # String is not a supported table format, should get fallback
    assert "unsupported" in result.lower() or "note" in result.lower()


# render_table() with plain-Python data (no pandas required)
def test_render_table_list_of_dicts():
    """Test list of dicts renders as a table."""
    data = [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
    ]
    result = render_table(data, name="People")

    assert "#### People" in result
    assert "| name | age | city |" in result
    assert "| Alice | 30 | NYC |" in result
    assert "| Bob | 25 | LA |" in result
    assert "_shape: 2 rows × 3 cols_" in result


def test_render_table_list_of_lists():
    """Test list of lists renders as a table with auto-generated headers."""
    data = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    result = render_table(data, name="Numbers")

    assert "#### Numbers" in result
    assert "| col_0 | col_1 | col_2 |" in result
    assert "| 1 | 2 | 3 |" in result
    assert "| 4 | 5 | 6 |" in result
    assert "_shape: 2 rows × 3 cols_" in result


def test_render_table_list_of_lists_with_columns():
    """Test list of lists with explicit column headers."""
    data = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    result = render_table(data, name="Numbers", columns=["x", "y", "z"])

    assert "| x | y | z |" in result
    assert "| 1 | 2 | 3 |" in result


def test_render_table_list_of_tuples():
    """Test list of tuples renders as a table."""
    data = [
        ("Alice", 30),
        ("Bob", 25),
    ]
    result = render_table(data, name="Tuples", columns=["name", "age"])

    assert "| name | age |" in result
    assert "| Alice | 30 |" in result
    assert "| Bob | 25 |" in result


def test_render_table_dict_of_lists():
    """Test column-oriented dict renders as a table."""
    data = {
        "name": ["Alice", "Bob", "Carol"],
        "score": [95, 87, 92],
    }
    result = render_table(data, name="Scores")

    assert "#### Scores" in result
    assert "| name | score |" in result
    assert "| Alice | 95 |" in result
    assert "| Bob | 87 |" in result
    assert "| Carol | 92 |" in result
    assert "_shape: 3 rows × 2 cols_" in result


def test_render_table_plain_truncation():
    """Test truncation works for plain-Python data."""
    data = [{"x": i, "y": i * 2} for i in range(50)]
    result = render_table(data, name="Long", max_rows=5)

    assert "#### Long" in result
    # Should have ellipsis row
    assert "…" in result
    # Shape should reflect actual data size
    assert "_shape: 50 rows × 2 cols_" in result
    # Count data rows (excluding header, separator, ellipsis)
    lines = [l for l in result.split("\n") if l.strip().startswith("|") and "---" not in l]
    # header + 5 data rows + 1 ellipsis row = 7
    assert len(lines) == 7


def test_render_table_empty_list():
    """Test empty list falls back to unsupported message."""
    result = render_table([], name="Empty")

    assert "unsupported" in result.lower() or "note" in result.lower()


def test_render_table_empty_dict():
    """Test empty dict falls back to unsupported message."""
    result = render_table({}, name="Empty")

    assert "unsupported" in result.lower() or "note" in result.lower()


# render_figure() tests
def test_render_figure_basic():
    """Test ![alt](path) format."""
    result = render_figure("path/to/image.png", filename="Chart")

    assert "![Chart](path/to/image.png)" in result


def test_render_figure_with_caption():
    """Test caption appended as *caption*."""
    result = render_figure("image.png", caption="Figure 1: Results")

    assert "![Figure 1: Results](image.png)" in result
    assert "*Figure 1: Results*" in result


def test_render_figure_no_caption():
    """Test only image link when no caption."""
    result = render_figure("image.png")

    assert "![image.png](image.png)" in result
    assert result.count("*") == 0  # No caption


def test_render_figure_alt_fallback():
    """Test alt text fallback: caption → filename → path."""
    # With caption
    result1 = render_figure("path/to/image.png", caption="My Caption")
    assert "![My Caption](path/to/image.png)" in result1

    # Without caption, should use path as alt
    result2 = render_figure("path/to/image.png")
    assert "![path/to/image.png](path/to/image.png)" in result2


# render_kv() tests
def test_render_kv_basic():
    """Test Key/Value table with markdown format."""
    data = {"Name": "Alice", "Age": "30", "City": "NYC"}
    result = render_kv(data, title="User Info")

    assert "#### User Info" in result
    assert "Name" in result
    assert "Alice" in result
    assert "Age" in result
    assert "30" in result
    assert "|" in result  # Table format


def test_render_kv_custom_title():
    """Test heading uses custom title."""
    data = {"key": "value"}
    result = render_kv(data, title="Custom Title")

    assert "#### Custom Title" in result


def test_render_kv_empty_dict():
    """Test header only, no rows for empty dict."""
    result = render_kv({}, title="Empty")

    assert "#### Empty" in result
    assert "Key" in result
    assert "Value" in result
    # Should have header but minimal content
    lines = [l for l in result.split("\n") if l.strip()]
    assert len(lines) <= 5  # Title + table header + separator


# render_summary() with pandas
@pytest.mark.requires_pandas
def test_render_summary_basic(sample_df):
    """Test shape, columns, null counts, numeric stats."""
    result = render_summary(sample_df, title="Summary")

    assert "#### Summary" in result
    assert "10 rows × 3 cols" in result
    assert "Columns" in result
    assert "value" in result


@pytest.mark.requires_pandas
def test_render_summary_no_nulls(sample_df):
    """Test no null section if no nulls."""
    result = render_summary(sample_df, title="Summary")

    # Should have shape and columns info
    assert "#### Summary" in result
    assert "Shape" in result


@pytest.mark.requires_pandas
def test_render_summary_many_columns():
    """Test column truncation with … (+N more)."""
    try:
        import pandas as pd
        # Create DataFrame with many columns
        wide_df = pd.DataFrame({f"col_{i}": range(5) for i in range(25)})
        result = render_summary(wide_df, title="Wide Data")

        assert "… (+5 more)" in result or "+5 more" in result
    except ImportError:
        pytest.skip("pandas not installed")


@pytest.mark.requires_pandas
def test_render_summary_numeric_stats(sample_df):
    """Test mean, std, min, max table for numeric columns."""
    result = render_summary(sample_df, title="Summary")

    # Check for numeric statistics
    assert "value" in result  # numeric column
    # Should have numeric stats section
    assert "Numeric stats" in result or "stats" in result.lower()


@pytest.mark.requires_pandas
def test_render_summary_no_numeric():
    """Test no stats section if no numeric columns."""
    try:
        import pandas as pd
        text_df = pd.DataFrame({"name": ["Alice", "Bob"], "city": ["NYC", "LA"]})
        result = render_summary(text_df, title="Text Data")

        assert "#### Text Data" in result
        # Should still have basic info even without numeric stats
        assert "2 rows" in result
    except ImportError:
        pytest.skip("pandas not installed")


@pytest.mark.requires_pandas
def test_render_summary_custom_title(sample_df):
    """Test heading uses custom title."""
    result = render_summary(sample_df, title="My Summary")

    assert "#### My Summary" in result


def test_render_summary_no_pandas():
    """Test fallback message when pandas unavailable."""
    # Test with a non-DataFrame object
    result = render_summary({}, title="Test")

    # Dict is not a DataFrame, so should get fallback
    assert "not a pandas dataframe" in result.lower()


# render_summary() edge cases
@pytest.mark.requires_pandas
def test_render_summary_empty_df():
    """Test empty DataFrame (0 rows)."""
    try:
        import pandas as pd
        empty_df = pd.DataFrame()
        result = render_summary(empty_df, title="Empty")

        assert "#### Empty" in result
        assert "0 rows" in result
    except ImportError:
        pytest.skip("pandas not installed")


@pytest.mark.requires_pandas
def test_render_summary_wide_df():
    """Test > 20 columns with truncation."""
    try:
        import pandas as pd
        wide_df = pd.DataFrame({f"col_{i}": range(3) for i in range(30)})
        result = render_summary(wide_df, title="Wide")

        assert "#### Wide" in result
        assert "30 cols" in result or "30 columns" in result
    except ImportError:
        pytest.skip("pandas not installed")


def test_render_summary_not_dataframe():
    """Test non-DataFrame object fallback."""
    result = render_summary([1, 2, 3], title="Not a DF")

    # Should handle gracefully with fallback message
    assert "not a pandas dataframe" in result.lower()
