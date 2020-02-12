# -*- coding: utf-8 -*-
# title                 :dash_app.py
# description           :Dashboard for search tool
# author                :Bobak (c180489)
# date                  :20171012
# version               :0.1.0
# usage                 :python dash_app.py
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
This script is made to load an index and offer up a search interface
using Whoosh search tools and Dash components

Todo:
        - host as an argument?
"""

# Standard
import argparse
import sys
import os
import pandas

# Dash tools
import dash
import document_management.document_indexer
import dash_core_components
import dash_html_components
import dash_table_experiments


APP = dash.Dash()
# Use an open access CSS to make the page look nicer
MY_CSS_URL = "https://codepen.io/chriddyp/pen/bWLwgP.css"
APP.css.append_css({
    "external_url": MY_CSS_URL
    })


# Disable for pylint string arguments
# pylint: disable=unused-argument
def parse(my_args):
    """
    Argument parser
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d',
                        '--d',
                        help="full input path to a Whoosh document index",
                        dest="index_dir",
                        type=str,
                        required=True
                       )
    return parser.parse_args()


MY_ARGS = parse(sys.argv)


def generate_table(dataframe, max_rows=10):
    """
    Generation of HTML tables from pandas
    dataframes to go in DCC HTML
    """

    # pylint: disable=maybe-no-member
    return dash_html_components.Table(
        # Header
        [dash_html_components.Tr(
            [dash_html_components.Th(col)
             for col in dataframe.columns])] +

        # Body
        [dash_html_components.Tr([
            dash_html_components.Td(
                dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# App layout, one column, has to have this weird template
# of our table for the way Dash processes the web page
# as a document.  This is a bit of a bug in the data
# table package which should be eventually fixed.
# This is a little hack to get around it.


# pylint: disable=maybe-no-member
APP.layout = dash_html_components.Div(className='container', children=[
    dash_html_components.Header(
        dash_html_components.H1(children='Search Portal')),

    dash_html_components.Div([
        dash_core_components.Input(
            id='search_term', value='search term', type="text"),
        dash_html_components.Div(
            dash_table_experiments.DataTable(rows=[{'title': '',
                                                    'path': '',
                                                    'highlight': ''}],
                                             columns=['title',
                                                      'path',
                                                      'highlight'],
                                             row_selectable=True,
                                             sortable=True,
                                             editable=True,
                                             enable_drag_and_drop=False,
                                             id='results_table'),
            id='hidden_div'),
        dash_html_components.Div(id='my_div'),
    ])

])

# Decorator and function for updating table data
# based on search term.


@APP.callback(
    dash.dependencies.Output('results_table', 'rows'),
    [dash.dependencies.Input('search_term', 'value')])
def update_output(input_value):
    """
    Updates the table output after a query has been run
    """

    if input_value != 'search term':
        results = document_management.document_indexer.do_search(
            input_value,
            MY_ARGS.index_dir)
        rows = results.to_dict('records')
    return rows

# Decorator and function for gathering file data from
# selected row indicies to render markdown in the
# browser window


@APP.callback(
    dash.dependencies.Output('my_div', 'children'),
    [dash.dependencies.Input('results_table', 'rows'),
     dash.dependencies.Input('results_table', 'selected_row_indices')])
def render_markdown(rows, selected_row_indices):
    """
    Actually render document content in the browser, either as a div
    if the content is markdown or in an iframe if the content is
    html
    """
    table_df = pandas.DataFrame(rows)
    # Make sure the table is made by checking
    # if the indicies exist
    if selected_row_indices:
        # Only one row can be selected at time to
        # display files
        if len(selected_row_indices) > 1:
            return dash_core_components.Markdown(
                """## Only one row can be selected for output""")
        else:
            file_path = table_df.get_value(selected_row_indices[0],
                                           'path')
            _, file_extension = os.path.splitext(file_path)
            # Right now the file extensions are hard-coded
            # but I want to make this something that is configurable
            markdown = ['.Rmd', '.md', '.MD', '.RMD']
            html_files = ['.html', '.HTML']
            supported_types = markdown+html_files

            # Make sure the file exists, and it is one
            # of the supported types
            if os.path.exists(file_path):
                if file_extension in supported_types:
                    in_file = open(file_path, 'r', encoding='utf-8')
                    data = in_file.read()
                    in_file.close()

                    if file_extension in html_files:
                        # To render the html nicely I have to start up
                        # an iframe (ugh) but this gives us a really
                        # nice view of the file
                        return dash_html_components.Iframe(
                            sandbox='',
                            srcDoc=data,
                            style={
                                'height': '100vh',
                                'width': '100%'})
                    elif file_extension in markdown:
                        return dash_core_components.Markdown(data)
                return dash_core_components.Markdown(
                    """## Unsupported filetype""")


if __name__ == '__main__':
    # Startup the server
    APP.run_server(debug=True, host='0.0.0.0',port=8888)
