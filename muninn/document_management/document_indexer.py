# title                 :document_indexer.py
# description           :POC for indexing ipynb and rmd files
# author                :Bobak (c180489)
# date                  :20170925
# version               :0.1.0
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
These functions help in the generation of whoosh indices,
iterating available files, and operating whoosh-based searches
on generated indicies

Todo:
    - Add more descriptive failure messages for index generation
"""

import builtins
import glob
import itertools
import os
import sys

import pandas

import whoosh.fields
import whoosh.index
import whoosh.qparser
import whoosh.searching


def glob_multiple_types(my_dir, *patterns):
    """Return files matching multiple patterns from a desired directory.

    Parameters
    ----------
    my_dir: string
        Path to the directory to be processed
    *patterns: list
        List of patterns to match

    Returns
    --------
    file_list: itertools.chain
        Full file paths for files that match pattern

    """
    file_list = itertools.chain.from_iterable(
        glob.iglob(my_dir+"/**/"+pattern,
                   recursive=True) for pattern in patterns)

    return file_list


def gen_index(my_dir, index_name="indexdir"):
    """
    Return the directory and index the files for ingestion and searching.

    Todo:
        * Manage json content instead of reading whole
          file

    :param dir: Directory that needs to be indexed
    :return: whoosh index
    """
    # Get paths for all the notebooks, rmd files, and
    # markdown

    all_files = [x for x in glob_multiple_types(my_dir,
                                                '*.*md',
                                                '*.md',
                                                '*.MD',
                                                '*.ipynb',
                                                '*.html',
                                                '*.HTML')]

    if all_files:
        schema = whoosh.fields.Schema(title=whoosh.fields.TEXT(stored=True),
                                      path=whoosh.fields.ID(stored=True),
                                      content=whoosh.fields.TEXT)

        # if the index path doesn't exist,
        # make itertools

        if not os.path.exists(index_name):
            os.mkdir(index_name)

        # Make the index
        whoosh_index = whoosh.index.create_in(index_name, schema)
        writer = whoosh_index.writer()

        # Iterate files then add their content to the
        # index
        for filename in all_files:
            try:
                if not builtins.any(
                        word in filename for word in ['reveal', 'ai_py']):

                    base_name = filename.split('/')[-1]
                    with open(filename, 'r', encoding='utf-8') as myfile:
                        writer.add_document(title=base_name,
                                            path=filename,
                                            content=myfile.read())

            except PermissionError as exception:
                # If there is a permission error log itertools and keep going
                sys.stderr.write(str(exception))

        writer.commit()

        return True
    # Something happened and the index wasn't generated
    return False


def do_search(search_term, index_name="indexdir"):
    """
    Return search for given term on an index in the file path.

    Parameters
    ----------
    search_term: string
        search term to find across indexed files
     index_name: whoosh index
        index name and path to search; default='indexdir'

    Returns
    -------
    my_results: pandas DataFrame
        Datframe of the results

    """
    # Maybe parameterize this
    if os.path.exists(index_name):
        whoosh_index = whoosh.index.open_dir(index_name)
        whoosh_qp = whoosh.qparser.QueryParser("content",
                                               schema=whoosh_index.schema)
        whoosh_query = whoosh_qp.parse(search_term)

        # build a quick and dirty query
        with whoosh_index.searcher() as searcher:
            results = searcher.search(whoosh_query)
            res_list = []
            # iterate through the results
            # and make a list of the dicts
            [res_list.append(dict(hitertools)) for hitertools in results]

        my_results = pandas.DataFrame(res_list)

        return my_results
    return False
