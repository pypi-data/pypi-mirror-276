from setuptools import setup, find_packages

setup(
    name="LeetTerminal",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
        "rich",
        "webdriver-manager",
        "selenium",
        "cloudscraper",
    ],
    entry_points={
        "console_scripts": [
            "LeetTerminal=LeetTerminal:main",
        ],
    },
)
