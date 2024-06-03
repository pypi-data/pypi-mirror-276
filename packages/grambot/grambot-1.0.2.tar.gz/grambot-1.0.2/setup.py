import re

from setuptools import find_packages, setup


requirements = [
    "asyncio",
    "requests"
]

with open("grambot/__init__.py", "rt", encoding="utf8") as x:
    version = re.search(r'__version__ = "(.*?)"', x.read()).group(1)

with open("grambot/__init__.py", "rt", encoding="utf8") as x:
    license = re.search(r'__license__ = "(.*?)"', x.read()).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


name = "grambot"
author = "AyiinXd"
author_email = "ayingaming98@gmail.com"
description = "Grambot Based Library For Your Telegram Bot."
url = "https://github.com/AyiinXd/grambot"
project_urls = {
    "Bug Tracker": "https://github.com/AyiinXd/grambot/issues",
    "Source Code": "https://github.com/AyiinXd/grambot",
}
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    project_urls=project_urls,
    license=license,
    packages=find_packages(exclude=["test*"]),
    install_requires=requirements,
    classifiers=classifiers,
    python_requires="~=3.7",
    package_data={
        "grambot": ["py.typed"],
    },
    zip_safe=False,
)