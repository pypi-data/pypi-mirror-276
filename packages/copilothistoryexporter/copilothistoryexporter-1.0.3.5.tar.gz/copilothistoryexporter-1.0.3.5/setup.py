import os

from setuptools import setup, find_packages

setup(
    name="copilothistoryexporter",
    version='1.0.3.5',
    url='https://github.com/enciyo/gh-copilot-history-export',
    author='Mustafa Kilic',
    author_email='enciyomk61@gmail.com',
    description='This package exports the history of GitHub Copilot chat history.',
    long_description="This package exports the history of GitHub Copilot chat history.",
    packages=find_packages(),
    package_data={'': ['*.md']},
    install_requires=[
        "requests",
        "click",
        "mitmproxy",
        "wheel",
        "setuptools",
    ],
    entry_points={
        'console_scripts': [
            'copilothistoryexporter = copilothistoryexporter.__main__:main'
        ]
    },
)
