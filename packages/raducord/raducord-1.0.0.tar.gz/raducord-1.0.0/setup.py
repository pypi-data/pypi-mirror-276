from setuptools import setup, find_packages

VERSION = "1.0.0"

setup(
    name="raducord",
    version=VERSION,
    author="H4cK3dR4Du",
    author_email="<rostermast70@gmail.com>",
    url="https://github.com/H4cK3dR4Du/raducord",
    description="The best library for designs, with a wide variety of colors and useful utils for your tools.",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "tls_client",
        "fake_useragent",
        "windows-curses; platform_system=='Windows'",
        "pyfiglet"
    ],
    keywords=["python", "utils", "color", "colors", "tools"],
    python_requires=">=3.11.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
