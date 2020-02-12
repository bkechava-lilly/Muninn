#!/lrlhps/users/c180489/py3/bin/python
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
    - Validate the directory structure for analysis projects
    - Add more descriptive failure messages for index generation
"""

import itertools
import glob
import sys
import os
import builtins
import pandas
import whoosh.index
import whoosh.fields
import whoosh.searching
import whoosh.qparser


def eprint(*args, **kwargs):
    """
    Helper to print errors/exceptions to
    stderr, this is because this tool
    is currently used in a cron job
    """

    print(*args, file=sys.stderr, **kwargs)


def glob_multiple_types(my_dir, *patterns):
    """
    Gathers files matching multiple
    patterns from a desired directory
    """

    return itertools.chain.from_iterable(
        glob.iglob(my_dir+"/**/"+pattern,
                   recursive=True) for pattern in patterns)


def gen_index(my_dir, index_name="indexdir"):

    """
    Function that takes a directory and indexes the ipynb,
    rmd, and md files for ingestion and searching.

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
                eprint(str(exception))

        writer.commit()

        return True
    # Something happened and the index wasn't generated
    return False


def do_search(search_term, index_name="indexdir"):
    """
    Performs search for given term on an index in the file path

    :param search_term: search term to find across indexed files
    :param index_name:  index name and path to search; default='indexdir'
    :return: whoosh index
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
            # iterate through the results, find if the file
            # still exists (sometimes it gets deleted),
            # then read the contents
            for hitertools in results:
                hitertools_dict = dict(hitertools)
                if os.path.isfile(hitertools['path']):
                    with open(hitertools['path'], encoding='utf-8') as fileobj:
                        file_contents = fileobj.read()
                        hitertools_dict['highlight'] = hitertools.highlights(
                            "content", text=file_contents)
                else:
                    # If the file is missing report that in
                    # the highlights column
                    hitertools_dict['highlight'] = '**MISSING FILE**'
                res_list.append(hitertools_dict)
        return pandas.DataFrame(res_list)

    return False
