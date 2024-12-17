# lecker

Lecker is a command line utility that crawls yummy web pages and converts their
content into markdown format, making it suitable for use in Large Language
Model (LLM) prompts in other CLI tools.

## Installation

```bash
poetry install && poetry shell
```

After installation, you need to run the setup command to install required dependencies:

```bash
lecker setup # This only needs to be done once
```

This will ensure Chrome/Chromium is installed and configure the web crawler properly.

## Usage

### Fetching Web Pages

Basic usage to fetch a webpage and convert it to markdown:

```bash
lecker fetch example.com
```

The URL will automatically have `https://` added if no protocol is specified.

Options:

- `-v, --verbose`: Enable verbose logging to see the crawling progress

  ```bash
  lecker fetch example.com --verbose
  ```

The markdown output is always sent to stdout, so you can pipe it to other commands:

```bash
lecker fetch example.com > output.md
```
