import sys
import os
from setuptools import setup, find_packages, Command
from shockfish.__metadata__ import __version__, __author__, __author_email__, __description__, __title__

if sys.version_info < (3, 5):
    sys.exit("Python < 3.5 is not supported")


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')

setup(
    name=str.lower(__title__),
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url="https://github.com/positivetechnologies/shockfish.git/",
    license="GPL",
    keywords = "WAF Twisted",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3",
    ],
    data_files=[('/etc/shockfish', ['shockfish/shockfish.json'])],
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[
        "twisted",
        "pylibinjection"
    ],
    cmdclass={
        "clean": CleanCommand,
    }
)