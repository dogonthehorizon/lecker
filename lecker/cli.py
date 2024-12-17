import asyncio
import contextlib
import io
import shutil
import subprocess
import sys
from typing import Optional

from crawl4ai import AsyncWebCrawler
from crawl4ai.models import MarkdownGenerationResult
from rich import print
import typer

app = typer.Typer()


async def crawl_webpage(
    url: str, verbose: bool = False
) -> Optional[str | MarkdownGenerationResult]:
    """
    Crawl a webpage and convert it to markdown format.

    Args:
        url: The URL to crawl
        verbose: Whether to show crawling logs

    Returns:
        The markdown content or None if failed
    """
    if verbose:
        # Don't redirect output if verbose mode is enabled
        async with AsyncWebCrawler(
            headless=True, verbose=True, sleep_on_close=False
        ) as crawler:
            result = await crawler.arun(url=url)
            return result.markdown
    else:
        # Redirect stdout and stderr to nowhere to suppress logs
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            async with AsyncWebCrawler(
                headless=True, verbose=False, sleep_on_close=False
            ) as crawler:
                result = await crawler.arun(url=url)
                return result.markdown


@app.command()
def fetch(
    url: str,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
):
    """
    Fetch a webpage and convert it to markdown format.
    Output is always sent to stdout as markdown.
    """
    # Ensure URL has http:// or https:// prefix
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        if result := asyncio.run(crawl_webpage(url, verbose)):
            print(result)
        else:
            print("sad")
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}", file=sys.stderr)
        sys.exit(1)


@app.command()
def setup():
    """
    Run initial setup for the crawl4ai dependency.
    This is required before first use of the fetch command.
    """
    try:
        # Check if Chrome is installed
        chrome_paths = [
            "chrome",
            "google-chrome",
            "chromium",
            "chromium-browser",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS default
            "/Applications/Chromium.app/Contents/MacOS/Chromium",  # macOS Chromium
        ]
        chrome_found = any(shutil.which(path) for path in chrome_paths)

        if not chrome_found:
            print("Chrome not found. Installing Chrome via Playwright...")
            subprocess.run(
                ["playwright", "install", "chrome"],
                check=True,
                capture_output=True,
                text=True,
            )
            print("Chrome installation completed!")

        result = subprocess.run(
            ["crawl4ai-setup"], check=True, capture_output=True, text=True
        )
        print("Setup completed successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error: Setup failed!", file=sys.stderr)
        print("\nError details:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        print("\nPossible solutions:", file=sys.stderr)
        print(
            "1. Ensure crawl4ai is properly installed in your environment",
            file=sys.stderr,
        )
        print("2. Try running 'poetry install' again", file=sys.stderr)
        print(
            "3. Check if you have proper permissions to install dependencies",
            file=sys.stderr,
        )
        sys.exit(1)
    except FileNotFoundError:
        print("Error: crawl4ai-setup command not found!", file=sys.stderr)
        print("\nPossible solutions:", file=sys.stderr)
        print(
            "1. Make sure you're in the poetry environment (run 'poetry shell')",
            file=sys.stderr,
        )
        print("2. Try reinstalling dependencies with 'poetry install'", file=sys.stderr)
        sys.exit(1)


def main():
    app()


if __name__ == "__main__":
    main()
