import argparse
import sys

from playwright.sync_api import sync_playwright


VERSION = "0.2"


def get_raw_html_content(filepath: str) -> str:
    """Retrieve raw HTML content from a file or STDIN.

    Args:
        filepath: Path to the file containing HTML content, or '-' for STDIN.

    Returns:
        Raw HTML content as a string.
    """
    if filepath == "-":
        return sys.stdin.read()

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def get_rendered_html_content(html_content: str, selectors: list = None) -> str:
    """Render the HTML content in a headless browser and return the rendered HTML content.

    Args:
        html_content: The HTML content to render.
        selectors: Optional list of CSS selectors to wait for before rendering.

    Returns:
        Rendered HTML content as a string.
    """
    with sync_playwright() as playwright:
        with playwright.chromium.launch() as browser:
            page = browser.new_page()
            page.set_content(html_content)

            if selectors:
                for selector in selectors:
                    page.wait_for_selector(selector)

            rendered_html = page.content()
    return rendered_html


def save_rendered_html_content(html_content: str, filepath: str) -> None:
    """Save the HTML content to a file or output it to STDOUT.

    Args:
        html_content: The HTML content to save or output.
        filepath: Path to the output file, or '-' for STDOUT.
    """
    if filepath == "-":
        sys.stdout.write(html_content)
    else:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html_content)


def cli() -> None:
    """Parse command-line arguments and render the HTML content."""

    parser = argparse.ArgumentParser(
        description="Render HTML using Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  Read HTML from file and output rendered HTML to STDOUT:
    $ playwright-html-renderer --html examples/input.html

  Read HTML from STDIN and output rendered HTML to file:
    $ cat examples/input.html | playwright-html-renderer --html - -o examples/output.html

  Read HTML from file, wait for selector '#navigation', and output to STDOUT:
    $ playwright-html-renderer --html examples/input.html -s "#navigation"

  Read HTML from file, wait for multiple selectors, and output to file:
    $ playwright-html-renderer --html examples/input.html -s "#navigation" ".main" -o examples/output.html
""",
    )
    parser.add_argument(
        "--html",
        type=str,
        required=True,
        help="File containing HTML content, or '-' for STDIN",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="-", help="Output file, or '-' for STDOUT"
    )
    parser.add_argument(
        "-s",
        "--selectors",
        nargs="+",
        default=None,
        help="Optional list of CSS selectors to wait for before rendering",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {VERSION}"
    )
    args = parser.parse_args()

    html_content = get_raw_html_content(filepath=args.html)
    rendered_html_content = get_rendered_html_content(html_content, args.selectors)
    save_rendered_html_content(rendered_html_content, args.output)
