import pytest

from prepembd.lib.helper import remove_excessive_dots, strip_quote_prefixes


def test_remove_excessive_dots():
    # Example usage
    original_text = (
        "This is a test.... with more than four dots..... and here's another...."
    )
    cleaned_text = remove_excessive_dots(original_text)
    assert cleaned_text == "This is a test with more than four dots and here's another"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "This is a test.\nThis is another line.",
            "This is a test.\nThis is another line.",
        ),
        (
            "> This is a quoted line.\nThis is not quoted.",
            "This is a quoted line.\nThis is not quoted.",
        ),
        ("> Quote1.\n> Quote2.", "Quote1.\nQuote2."),
        ("", ""),
        ("Single line with > quote", "Single line with > quote"),
        (">No space after quote mark", ">No space after quote mark"),
    ],
)
def test_strip_quote_prefixes(test_input, expected):
    assert strip_quote_prefixes(test_input) == expected
