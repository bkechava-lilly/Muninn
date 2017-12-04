# title                 :convert_to_html.py
# description           :Manager for reproducible research for converting
#                        analyses to HTML for indexing
# author                :Bobak (c180489)
# date                  :20171012
# version               :0.1.0
# usage                 :python convert_to_html.py
# notes                 :
# python_version        :3.5.1
# Copyright (C) 2017 Eli Lilly - Bobak Kechavarzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
"""
Manager for reproducible research
for converting analyses to HTML and indexing
"""

import sys
import argparse
import os
import builtins

# For document conversion
import document_management.document_processing
import document_management.document_indexer


# Disable for pylint string arguments
# pylint: disable=unused-argument
def parse(my_args):
    """
    Argument Parser
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-o',
                        '--o',
                        help="path and filename for index output",
                        dest="out_file",
                        type=str,
                        required=True
                       )
    parser.add_argument('-d',
                        '--d',
                        help="input directory to process",
                        dest="my_dir",
                        type=str,
                        required=True
                       )
    return parser.parse_args()


def eprint(*args, **kwargs):
    """
    Helper to print errors/exceptions to
    stderr, this is because this tool
    is currently used in a cron job
    """
    print(*args, file=sys.stderr, **kwargs)


MY_ARGS = parse(sys.argv)


def main():
    """
    Crawl and process files to convert documents to html,
    then rebuild the whoosh index
    """

    # Get all the files we need to convert
    files = document_management.document_processing.get_file_names(
        MY_ARGS.my_dir)
    # Go through each of the files and then
    # convert the md and ipynb files to html

    for my_file in files:
        # do this to bypass any reveal.js content
        # from notebook slides
        if not builtins.any(
                word in my_file for word in ['reveal', 'ai_py']):

            _, file_ext = os.path.splitext(my_file)
            document_management.document_processing.prep_html(
                file_ext, my_file)

    # Regenerate the index
    document_management.document_indexer.gen_index(MY_ARGS.my_dir,
                                                   MY_ARGS.out_file)


if __name__ == '__main__':
    main()
