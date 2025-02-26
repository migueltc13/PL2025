#!/usr/bin/env python3

"""
Markdown to HTML converter

Supports:
- Paragraphs
- Headers
- Numbered lists
- Unordered lists
- Images
- Links
- Italics
- Bold
- Horizontal rules
"""

import sys
import os
import re

substitutions = [
    (
        # 1. Headers
        r"^(#{1,6}) (.+)$",
        lambda m: f"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>",
        re.MULTILINE
    ),
    (
        # 2. Numbered lists
        r"((?:^\d\.\s(.+)(?:\n|$))+)",
        lambda m: (
            "<ol>\n"
            + ''.join(
                f"<li>{item.strip()}</li>\n"
                for item in re.findall(r"^\d\.\s(.+)", m.group(1), re.MULTILINE)
            )
            + "</ol>\n"
        ),
        re.MULTILINE
    ),
    (
        # 3. Unordered lists
        r"((?:^-\s(.+)(?:\n|$))+)",
        lambda m: (
            "<ul>\n"
            + ''.join(
                f"<li>{item.strip()}</li>\n"
                for item in re.findall(r"^-\s(.+)", m.group(1), re.MULTILINE)
            )
            + "</ul>\n"
        ),
        re.MULTILINE
    ),
    (
        # 4. Images
        r"\!\[(.+)\]\((.+)\)",
        lambda m: f"<img src='{m.group(2)}' alt='{m.group(1)}'>",
        0
    ),
    (
        # 5. Links
        r"\[(.+)\]\((.+)\)",
        lambda m: f"<a href='{m.group(2)}'>{m.group(1)}</a>",
        0
    ),
    (
        # 6. Horizontal rules
        r"^(?:-{3,}|_{3,}|\*{3,})$",
        lambda m: "<hr>",
        re.MULTILINE
    ),
    (
        # 7. Bolds
        r"\*\*(.+?)\*\*",
        lambda m: f"<b>{m.group(1)}</b>",
        0
    ),
    (
        # 8. Italics
        r"\*(.+?)\*",
        lambda m: f"<i>{m.group(1)}</i>",
        0
    ),
    (
        # 9. Inline code
        r"`(.+?)`",
        lambda m: f"<code>{m.group(1)}</code>",
        0
    ),
    (
        # 9. Paragraphs
        # r"((?:^(?!\s*$)(?!<\w+>)[^\n]+(?:\n[^\n]+)*)+)",
        r"((?:^(?!\s*$)(?!<\/?\w).+$\n?)+)",
        lambda m: f"<p>{m.group(1).rstrip('\n')}</p>",
        re.MULTILINE
    )
]


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input.md>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, "r", encoding="utf-8") as f:
        contents = f.read()

    # Substitute potencial html tags
    contents = re.sub(r"<", "&lt;", contents)
    contents = re.sub(r">", "&gt;", contents)

    for pattern, repl, flags in substitutions:
        contents = re.sub(pattern, repl, contents, flags=flags)

    # output file name
    if input_file.endswith(".md"):
        output_file = input_file.replace(".md", ".html")
    else:
        output_file = input_file + ".html"

    # Save to the file to the current directory
    output_file = os.path.join(os.getcwd(), os.path.basename(output_file))

    # write to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n")
        f.write(contents)
        f.write("\n</body>\n</html>\n")


if __name__ == "__main__":
    main()
