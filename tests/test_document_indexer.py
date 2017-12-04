"""
Tests for document indexer functions
Todo:
    - make a function for generating and tearing down
      fake testing directories
"""

import os
import document_management.document_indexer
import pytest


# Tests for globbing files
def test_glob_ipynb_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.ipynb")
    fn.write('content')

    files = [x for x in document_management.document_indexer.
             glob_multiple_types(str(tmpdir),
                                 '*.ipynb')]
    assert(files[0].split('/')[-1] in ['tmpfile.ipynb'])


def test_glob_md_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.md")
    fn.write('content')

    files = [x for x in document_management.document_indexer.
             glob_multiple_types(str(tmpdir),
                                 '*.md')]
    assert(files[0].split('/')[-1] in ['tmpfile.md'])


def test_glob_rmd_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.rmd")
    fn.write('content')

    files = [x for x in document_management.document_indexer.
             glob_multiple_types(str(tmpdir),
                                 '*.rmd')]
    assert(files[0].split('/')[-1] in ['tmpfile.rmd'])


def test_glob_html_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.html")
    fn.write('content')

    files = [x for x in document_management.document_indexer.
             glob_multiple_types(str(tmpdir),
                                 '*.html')]
    assert(files[0].split('/')[-1] in ['tmpfile.html'])


# Test index generation
def test_gen_index():
    good_dir = document_management.document_indexer.gen_index(
        '../tests/test_dir_w_files/',
        '../tests/test_index_w_files')

    bad_dir = document_management.document_indexer.gen_index(
        'idontexist/',
        'test_index_w_nothing')

    # just see if an index is made with basic files
    # and returns true
    assert good_dir is True
    assert os.path.exists('../tests/test_index_w_files') is True

    # an index trying to be made from missing directory
    assert bad_dir is False


def test_do_search():
    index_dir = '../tests/test_index_w_files'
    bad_index_dir = '../tests/idontexist'
    res = document_management.document_indexer.do_search(
        'content',
        index_dir)
    no_res = document_management.document_indexer.do_search(
        'apples',
        index_dir)

    no_index_res = document_management.document_indexer.do_search(
        'content',
        bad_index_dir)

    # make sure the right number of results come back
    assert res.shape == (5, 3)

    # make sure function exists gracefully if there is no index
    assert no_index_res is False

    # make sure nothing breaks if there aren't any results
    assert no_res.shape == (0, 0)
