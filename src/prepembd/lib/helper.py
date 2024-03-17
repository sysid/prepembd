import re


def remove_excessive_dots(text):
    pattern = r"\.{4,}"
    # Change '' to '.' if you want to replace with a single dot instead of removing
    return "\n".join(re.sub(pattern, "", text) for text in text.split("\n"))


def strip_quote_prefixes(text):
    return "\n".join(
        line[2:] if line.startswith("> ") else line for line in text.split("\n")
    )
