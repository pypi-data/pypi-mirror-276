"""html module"""

from typing import Union
from pathlib import Path
from typing import Dict


def build_html(matches: Dict[str, Dict[str, int]], file_path: Union[str, Path]) -> None:
    """Build an HTML file with the colors.

    Builds an HTML file with the colors and their counts.

    Args:
        matches (Dict[str, Dict[str, int]]): The color counts.
        file_path (Union[str, Path]): path to css file
    """

    # Start the HTML file
    html = """<html><head><title>CSS Colors Stats</title></head><body>
    <h1>CSS Colors Stats</h1>
    <p>Counts of color occurences in CSS files.</p>
    <div class="colors" style="display:flex;flex-direction:column;">
    """

    for color_type in matches:
        html += f"<h2>{color_type}</h2>"
        # Add a div for each color
        for item in matches[color_type]:
            html += f'<div style="background-color:{item["color"]};width:100px;height:100px;">{item["color"]}:{item["count"]}</div>'  # noqa

    # End the HTML file
    html += "</div></body></html>"

    # Write the HTML file
    with open(Path(file_path.parent, file_path.stem + "_csscs.html"), "w") as file:
        file.write(html)
