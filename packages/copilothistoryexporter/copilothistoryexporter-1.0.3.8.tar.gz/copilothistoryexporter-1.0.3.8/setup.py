import os

from setuptools import setup, find_packages


def read_file(filename):
    full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    with open(full_path, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


setup(
    name="copilothistoryexporter",
    version='1.0.3.8',
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
    ],
    entry_points='''
     [console_scripts]
     copilothistoryexporter=copilothistoryexporter.main:sys_main
     '''
)
