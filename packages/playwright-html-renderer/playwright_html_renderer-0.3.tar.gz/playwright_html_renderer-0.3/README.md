# Playwright HTML Renderer

[![PyPI](../../actions/workflows/pypi.yml/badge.svg)](../../actions/workflows/pypi.yml)

Playwright HTML Renderer is a command-line interface (CLI) tool designed to render HTML using [Playwright](https://playwright.dev/python).

## ⚙️ Installation

You can install Playwright HTML Renderer via pip:

```sh
$ pip install playwright-html-renderer
```

## ⌨️ Usage

Playwright HTML Renderer provides a simple command-line interface to render HTML content using Playwright. Here are some examples of how to use it:

- Read HTML from a file and output rendered HTML to `STDOUT`:  
  ```sh
  $ playwright-html-renderer --html examples/input.html
  ```

- Read HTML from `STDIN` and output rendered HTML to a file:  
  ```sh
  $ cat examples/input.html | playwright-html-renderer --html - -o examples/output.html
  ```

- Read HTML from a file, wait for a specific CSS selector (`#navigation`), and output to `STDOUT`:  
  ```sh
  $ playwright-html-renderer --html examples/input.html -s "#navigation"
  ```

- Read HTML from a file, wait for multiple selectors (`#navigation`, `.main`), and output to a file:  
  ```sh
  $ playwright-html-renderer --html examples/input.html -s "#navigation" ".main" -o examples/output.html
  ```

For more information, you can also use the --help option:  

```sh
$ playwright-html-renderer --help
```

## 🔨 Technology

The following technologies, tools and platforms were used during development.

- **Code**: [Python](https://python.org)
- **CI/CD**: [GitHub Actions](https://github.com/actions)

## 🐛 Found a Bug?

Thank you for your message! Please fill out a [bug report](../../issues/new?assignees=&labels=&template=bug_report.md&title=).

## License

This project is licensed under the [European Union Public License 1.2](https://choosealicense.com/licenses/eupl-1.2/).