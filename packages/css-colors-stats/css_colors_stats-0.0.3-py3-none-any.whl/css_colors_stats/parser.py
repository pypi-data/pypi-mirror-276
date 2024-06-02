"""parser module"""

import re
from typing import Union
from collections import Counter
from typing import Dict, List, Literal

SEARCH_PATTERNS = {
    "hex": r"#(?:[0-9a-fA-F]{3}){1,2}\b",
    "rgb": r"rgb\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)",
    "rgba": r"rgba\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d*\.?\d+)\s*\)",
    "hsl": r"hsl\(\s*(\d+),\s*(\d+)%,\s*(\d+)%\s*\)",
    "hsla": r"hsla\(\s*(\d+),\s*(\d+)%,\s*(\d+)%\s*,\s*(\d*\.?\d+)\s*\)",
}


def parse_css_for_colors(
    css_content: str,
    color_format: Union[None, str, List[str]] = None,
) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    """Parse a CSS file for colors.

    Parses a CSS file for colors and returns the counts of each color.

    Available color formats:
    - hex
    - rgb
    - rgba
    - hsl
    - hsla

    Args:
        css_content (str): The content of the CSS file.
        color_format (Union[None, str, List[str]], optional): The color format
            to search for. Defaults to None.

    Returns:
        Dict[str, List[Dict[str, Union[str, int]]]]: Dictionary with
            the color counts for each color format.

    Raises:
        ValueError: If the color format is invalid.

    Example:
        Parse a CSS file for hex colors

            >>> css_content = 'body { background-color: #fff; color: #000; }'
            >>> parse_css_for_colors(css_content)
            {'hex': {'#fff': 1, '#000': 1}, 'rgb': {}, 'rgba': {}, 'hsl': {}, 'hsla': {}} # noqa
    """

    if color_format is None:
        color_format = ["hex", "rgb", "rgba", "hsl", "hsla"]
    elif isinstance(color_format, str) and color_format in SEARCH_PATTERNS:
        color_format = [color_format.lower()]
    elif isinstance(color_format, list):
        if any(
            [color for color in color_format if color.lower() not in SEARCH_PATTERNS]
        ):
            raise ValueError("Invalid color format in the list.")
        else:
            pass
    else:
        raise ValueError("Invalid color format.")

    # Find all color occurrences in the CSS content
    matches = {}
    for color_type in color_format:
        found = re.findall(SEARCH_PATTERNS[color_type], css_content)
        if len(found) > 0:
            matches[color_type] = []
            [
                matches[color_type].append({"color": color, "count": count, "id": i})
                for i, (color, count) in enumerate(Counter(found).items())
            ]

    # Sort each dictionary by decreasing values
    matches = sort_colors(matches)
    return matches


def sort_colors(matches: Dict, order: Literal["asc", "desc"] = "desc") -> Dict:
    """sort list of matches by count

    Args:
        matches (Dict): dictionary with color matches
        order (Literal["asc","desc"]): order of sorting. Defaults to "desc".

    Returns:
        Dict: sorted dictionary of matches
    """
    for color_type in matches:
        matches[color_type] = sorted(
            matches[color_type], key=lambda x: x["count"], reverse=order == "desc"
        )
    return matches
