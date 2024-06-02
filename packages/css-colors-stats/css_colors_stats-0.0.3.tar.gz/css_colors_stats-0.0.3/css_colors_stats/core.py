"""Core module for the css_colors_stats package.
"""

from pathlib import Path
import argparse
import json

from css_colors_stats.html import build_html
from css_colors_stats.parser import parse_css_for_colors


def main() -> None:
    """Main function for the CLI.

    Parses a CSS file for colors and saves the color counts to a json file.
    """
    parser = argparse.ArgumentParser(
        description="Quickly extract and count colors from CSS files."
    )
    # Add the arguments
    parser.add_argument(
        "FilePath", metavar="filepath", type=str, help="the path to the CSS file"
    )
    parser.add_argument(
        "--html",
        action="store_true",  # if present true else false
        help="generate an HTML file with the color counts",
    )
    # Parse the arguments
    args = parser.parse_args()
    file_path = Path(args.FilePath)  # FilePath

    # Read CSS file
    with open(file_path, "r", encoding="utf-8") as file:
        css_content = file.read()

    # Parse CSS content for colors
    color_counts = parse_css_for_colors(css_content)

    # Save colors to HTML file
    if args.html:
        build_html(color_counts, file_path)

    # Save color counts to a json file
    with open(Path(file_path.parent, file_path.stem + "_csscs.json"), "w") as file:
        json.dump(color_counts, file, indent=4)
