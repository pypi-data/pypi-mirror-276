import os

from setuptools import setup, find_packages



setup(
    name="gh-copilot-history",
    version='0.1.0',
    url='https://github.com/enciyo/gh-copilot-history-export',
    author='Mustafa Kılıç',
    author_email='enciyomk61@gmail.com',
    description='This package exports the history of GitHub Copilot chat history.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "mitmproxy"
    ],
)
