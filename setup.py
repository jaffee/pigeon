from setuptools import setup

setup(
    name='pigeon',
    version='0.1.1',
    description="",
    install_requires=[
	'Flask',
        'requests',
	],
    packages=['pigeon'],
    scripts=['runpigeon.py'],
)
