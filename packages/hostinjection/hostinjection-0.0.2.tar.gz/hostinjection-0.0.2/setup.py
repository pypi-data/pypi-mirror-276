from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = 'testy'
LONG_DESCRIPTION = 'This is a tool used for test'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hostinjection",
    version=VERSION,
    author="@jutrm",
    author_email="<jutrm@gmail.com>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'hostinjection = packages.main:main',
        ],
    },
    install_requires=['requests', 'argparse'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)