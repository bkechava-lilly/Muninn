#!/lrlhps/users/c180489/py3/bin/python
# title                 :document_processing.py
# description           :helper code for document processing/conversion
# author                :Bobak (c180489)
# date                  :20170925
# version               :0.01
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
Helper functions for document processing and conversion
"""

import sys
import itertools
import glob
import os

# For document conversion
import markdown2
import nbconvert
import nbformat


def eprint(*args, **kwargs):
    """
    Helper to print errors/exceptions to
    stderr, this is because this tool
    is currently used in a cron job
    """
    print(*args, file=sys.stderr, **kwargs)


# Use grip library to convert md files to html
def md_to_html(file_path):
    """
    Use the markdown2 library to convert MD files
    to html

    :param file_path: path to markdown file
    """
    try:
        if os.path.exists(file_path) and '.md' in file_path:
            markdowner = markdown2.Markdown()
            md_file = open(file_path, 'r', errors='ignore').read()
            out_text = markdowner.convert(md_file)
            out_file = open(file_path.replace('.md',
                                              '.html'), 'w')
            out_file.write(out_text)
            out_file.close()

            return True
        return False
    except PermissionError as exception:
        eprint(str(exception))
        return False
    return False


# nbconvert to change .ipynb to html
def ipynb_to_html(file_path):
    """
    Use the nbconvert python library to manage the
    .ipynb conversion

    :param file_path: path to ipynb file
    """
    try:
        if os.path.exists(file_path) and '.ipynb' in file_path:
            my_nb_content = nbformat.reads(open(file_path,
                                                'r',
                                                errors='ignore').read(),
                                           as_version=4)
            html_exporter = nbconvert.HTMLExporter()
            html_exporter.template_file = 'basic'
            (body, _) = html_exporter.from_notebook_node(my_nb_content)

            out_file_name = file_path.replace('.ipynb', '.html')
            # Extra level of catching just in case we can read
            # in a dir but not write -- itertools happened
            try:
                out_file = open(out_file_name, 'w')
                out_file.write(body)
                out_file.close()
            except PermissionError as exception:
                eprint(str(exception))
        else:
            return False
    except PermissionError as exception:
        eprint(str(exception))


# There is probably a more perfomant way to do this
def glob_multiple_types(my_dir, *patterns):

    """
    Gathers files matching multiple patterns
    from a desired directory
    """

    return itertools.chain.from_iterable(
        glob.iglob(my_dir+"/**/"+pattern,
                   recursive=True) for pattern in patterns)


# This will need to parameterized to for user - inputted
# file types
def get_file_names(my_dir):
    """
    Get all the files in the supplied directory that
    match the file extension patterns

    Todo:
        - parameterize the file extensions

    """
    all_files = [x for x in glob_multiple_types(my_dir,
                                                '*.*md',
                                                '*.md',
                                                '*.MD',
                                                '*.ipynb')]
    return all_files


def prep_html(file_type, file_path):
    """
    Get a mapping of file types observed
    and what method needs to be used to convert
    them

    :param file_type: file extension/type
    :param file_path: path to the file
    """

    # Method mapping
    methods = {'.md': md_to_html,
               '.ipynb': ipynb_to_html}
    # The actual execution that occurs
    if file_type in methods and os.path.exists(file_path):
        methods[file_type](file_path)
        return True
