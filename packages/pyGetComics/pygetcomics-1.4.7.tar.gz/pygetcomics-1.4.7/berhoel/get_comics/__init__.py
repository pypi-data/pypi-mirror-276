#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Download various daily comics.
"""

# Standard library imports.
import argparse

# Local library imports.
from . import peanuts, garfield

__date__ = "2024/06/02 01:52:32 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2017, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"
__version__ = __import__("importlib.metadata", fromlist=["version"]).version(
    "pyGetComics"
)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="get_comics", description="Download various periodic comics."
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    return parser


def main(args=None):
    """Get all supported comics."""
    args = get_parser().parse_args()

    print("Get Peanuts.")
    peanuts.main(args)
    print("Get Garfield.")
    garfield.main(args)


if __name__ == "__main__":
    main()

# Local Variables:
# mode: python
# compile-command: "cd ../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
