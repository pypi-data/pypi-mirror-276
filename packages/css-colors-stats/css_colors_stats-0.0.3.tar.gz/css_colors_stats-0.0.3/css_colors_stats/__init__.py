"""css-colors-stats

Quickly extract and count colors from CSS files.


Example:
    Parse a CSS file for colors and save the color counts to a json file.

        $ css-colors-stats test.css

    Parse a CSS file and save HTML file.

        $ css-colors-stats test.css --html

    Get help.

        $ css-colors-stats --help
"""

from .core import main

__all__ = ["main"]
