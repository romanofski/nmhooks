# coding: utf-8
from setuptools import setup, find_packages
from nmhooks import __author__
from nmhooks import __author_email__
from nmhooks import __description__
from nmhooks import __name__
from nmhooks import __version__


setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=open("README.rst").read(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
    ],
    author=__author__,
    author_email=__author_email__,
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'notmuch',
    ],
    entry_points={
        'console_scripts': [
            'post-new= nmhooks.commandline:postnew',
        ]
    }
)
