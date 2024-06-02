import io
import os

from setuptools import setup, find_packages

VERSION = "0.3"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="playwright-html-renderer",
    description="CLI tool to render HTML using Playwright",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Stefan Kühnel",
    version=VERSION,
    readme="README.md",
    license="European Union Public License 1.2",
    url="https://github.com/custom-packages/playwright-html-renderer",
    project_urls={
        "Documentation": "https://github.com/custom-packages/playwright-html-renderer",
        "Source code": "https://github.com/custom-packages/playwright-html-renderer",
        "Issues": "https://github.com/custom-packages/playwright-html-renderer/issues",
        "CI": "https://github.com/custom-packages/playwright-html-renderer/actions",
    },
    python_requires=">=3.8",
    install_requires=["playwright==1.44.0"],
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        playwright-html-renderer=playwright_html_renderer.cli:cli
    """,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
    ],
)
