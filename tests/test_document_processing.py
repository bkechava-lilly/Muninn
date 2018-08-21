"""
Tests for document processing functions
"""
import os
from muninn.document_management import document_processing
import pytest


# Tests for globbing files

def test_glob_md_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.md")
    fn.write('content')

    files = [x for x in document_processing.
             glob_multiple_types(str(tmpdir),
                                 '*.md')]
    assert(files[0].split('/')[-1] in ['tmpfile.md'])


def test_glob_html_types(tmpdir):
    fn = tmpdir.mkdir("sub").join("tmpfile.html")
    fn.write('content')

    files = [x for x in document_processing.
             glob_multiple_types(str(tmpdir),
                                 '*.html')]
    assert(files[0].split('/')[-1] in ['tmpfile.html'])


def test_md_to_html():
    file_path = 'tests/test_dir_w_files/test1.md'
    bad_file_path = 'tests/test_dir_w_files/test1.ipynb'
    no_file_path = ''

    res = document_processing.md_to_html(file_path)
    assert os.path.exists(file_path.replace('.md', '.html')) is True

    res = document_processing.md_to_html(bad_file_path)
    assert res is False

    res = document_processing.md_to_html(no_file_path)
    assert res is False
