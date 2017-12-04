"""
Tests for document processing functions
"""
import os
import document_management.document_processing
import pytest


# Tests for globbing files
def test_glob_ipynb_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.ipynb")
    fn.write('content')

    files = [x for x in document_management.document_processing.
             glob_multiple_types(str(tmpdir),
                                 '*.ipynb')]
    assert(files[0].split('/')[-1] in ['tmpfile.ipynb'])


def test_glob_md_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.md")
    fn.write('content')

    files = [x for x in document_management.document_processing.
             glob_multiple_types(str(tmpdir),
                                 '*.md')]
    assert(files[0].split('/')[-1] in ['tmpfile.md'])


def test_glob_rmd_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.rmd")
    fn.write('content')

    files = [x for x in document_management.document_processing.
             glob_multiple_types(str(tmpdir),
                                 '*.rmd')]
    assert(files[0].split('/')[-1] in ['tmpfile.rmd'])


def test_glob_html_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.html")
    fn.write('content')

    files = [x for x in document_management.document_processing.
             glob_multiple_types(str(tmpdir),
                                 '*.html')]
    assert(files[0].split('/')[-1] in ['tmpfile.html'])


def test_md_to_html():
    file_path = '../tests/test_dir_w_files/test1.md'
    bad_file_path = '../tests/test_dir_w_files/test1.ipynb'
    no_file_path = ''

    res = document_management.document_processing.md_to_html(file_path)
    assert os.path.exists(file_path.replace('.md', '.html')) is True

    res = document_management.document_processing.md_to_html(bad_file_path)
    assert res is False

    res = document_management.document_processing.md_to_html(no_file_path)
    assert res is False


def test_ipynb_to_html():
    file_path = '../tests/test_dir_w_files/test1.ipynb'
    bad_file_path = '../tests/test_dir_w_files/test1.md'
    no_file_path = ''

    res = document_management.document_processing.ipynb_to_html(file_path)
    assert os.path.exists(file_path.replace('.ipynb', '.html')) is True

    res = document_management.document_processing.ipynb_to_html(bad_file_path)
    assert res is False

    res = document_management.document_processing.ipynb_to_html(no_file_path)
    assert res is False


def test_prep_html():
    file_path = '../tests/test_dir_w_files/test1.md'
    no_path = '../tests/test_dir_w_files/foo.txt'
    res = document_management.document_processing.prep_html('.ipynb',
                                                            file_path)

    assert res is True

    # Test if file doesn't exist
    res = document_management.document_processing.prep_html('.ipynb',
                                                            no_path)
    assert res is None

    # Test if extension doesn't exist
    res = document_management.document_processing.prep_html('.foo',
                                                            file_path)
