from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="copilothistoryexporter",
    version='1.0.2.3',
    url='https://github.com/enciyo/gh-copilot-history-export',
    author='Mustafa Kılıç',
    author_email='enciyomk61@gmail.com',
    description='This package exports the history of GitHub Copilot chat history.',
    long_description="This package exports the history of GitHub Copilot chat history.",
    package_dir={'': 'src'},
    packages=find_packages('src', include=["*"]),
    package_data={'': ['*.md']},
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'copilothistoryexporter=copilothistoryexporter.main:sys_main',
        ],
    },
)
