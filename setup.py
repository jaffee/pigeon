from setuptools import setup

setup(
    name='pigeon',
    version='0.2',
    description="Post gitlab commit messages to referenced JIRA issues",
    install_requires=[
        'Flask',
        'requests',
        'python-Levenshtein'
    ],
    packages=['pigeon'],
    scripts=['runpigeon.py'],
)
