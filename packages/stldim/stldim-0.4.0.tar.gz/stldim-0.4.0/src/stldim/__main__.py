#!/usr/bin/env python3
"""
    stldim - Get dimensions of an STL file
    Usage:
        stldim.py [options] <stlfile>

    Options:
        -h --help       Show this screen.
        --version       Show version.
        --name=<name>   Name of the object [defaults to the filename with non alpha-numeric\
characters replaced with underscores].
"""

import os
import sys

from docopt import docopt

from stldim import MeshWithBounds, version

def main():
    """
    Main function
    """
    args = docopt(__doc__, version=version.__str__)

    if not os.path.exists(args['<stlfile>']):
        sys.exit(f"ERROR: file {args['<stlfile>']} was not found!")

    stl_dimensions = MeshWithBounds.from_file(args['<stlfile>'])

    print(stl_dimensions.render('openscad_lib'))


if __name__ == '__main__':
    main()
