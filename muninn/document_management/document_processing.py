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

import builtins
import glob
import itertools
import os
import sys

# For document conversion
import markdown2

import nbconvert

import nbformat

from .document_indexer import *


# Use grip library to convert md files to html
def md_to_html(file_path):
    """
    Return html files from markdown.

    Currently the makrdown2 module is downgraded for the XSS
    vulnerability.

    Parameters
    ----------
    file_path: string
        path to markdown file

    Returns
    -------
    boolean
        Whether or not this completed sucessfully

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
        sys.stderr.write(str(exception))
        return False
    return False


# nbconvert to change .ipynb to html
def ipynb_to_html(file_path):
    """
    Return html using nbconvert module for .ipynb's .

    Parameters
    ----------
    file_path: string
        path to ipynb file

    Returns
    -------
    boolean
        Whether or not this completed succesfully

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
                return True
            except PermissionError as exception:
                sys.stderr.write(str(exception))
                return False
        else:
            return False
    except PermissionError as exception:
        sys.stderr.write(str(exception))
        return False


# There is probably a more perfomant way to do this
def glob_multiple_types(my_dir, *patterns):
    """Return files matching multiple patterns from a desired directory."""
    return itertools.chain.from_iterable(
        glob.iglob(my_dir+"/**/"+pattern,
                   recursive=True) for pattern in patterns)


# This will need to parameterized to for user - inputted
# file types
def get_file_names(my_dir):
    """
    Return files in the directory that match the file extension patterns.

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
    Return a dict of methods for file processing.

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
    return methods


def crawl_and_process(out_file, input_dir):
    """
    Return whoosh index from given directory.

    Crawl and process files to convert documents to html
    then rebuild the whoosh index.
    """
    # Get all the files we need to convert
    files = get_file_names(input_dir)
    # Go through each of the files and then
    # convert the md and ipynb files to html

    for my_file in files:
        # do this to bypass any reveal.js content
        # from notebook slides
        if not builtins.any(word in my_file for word in ['reveal', 'ai_py']):
            _, file_ext = os.path.splitext(my_file)
            prep_html(file_ext, my_file)

    # Regenerate the index
    gen_index(input_dir, out_file)
