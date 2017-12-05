# Muninn
In Norse mythology, Huginn (from Old Norse "thought") and Muninn (Old Norse "memory" or "mind") are a pair of ravens that fly all over the world, Midgard, and bring information to the god Odin [Wikipedia](https://en.wikipedia.org/wiki/Huginn_and_Muninn)

## Index and Search Tool
These tools are made for indexing and searching directories.  Currently the code indexes '.ipynb','.Rmd','.md', and '.html' files.  A search portal is served using Dash, Dash beta datatables, and Whoosh search capabilities.

Users can select a single row from the results table to have the content rendered to the browser.

Currently the code requires Dash, [dash table experiments](https://github.com/plotly/dash-table-experiments), and Whoosh.

## Scripts 

### Index generation : convert_to_html.py
>
usage: convert_to_html.py [-h] [-d DIR]
>
Manager for reproducible research
for converting analyses to HTML and indexing>
optional arguments:

  -h, --help       show this help message and exit
  -d DIR, --d DIR  input directory to index docs

The convert_to_html script will crawl a given input directory, identify any .md/.ipynb files and convert them to html for better screen rendering.  Afterwards it generates an index in the specified output directory.

### Search portal: dash.py 
>
usage: dash.py [-h] [-d DIR]
>
POC for indexing/searching ipynb and rmd files
>
optional arguments:
  -h, --help       show this help message and exit
  -d DIR, --d DIR  input directory to index docs

This script will start the dashboard app for searching, the input directory should be the path to the index generated from the previous step.

### Example execution:
1. Install the requirements
```
pip install -r requirements.txt
```
2. Generate your document index and convert .ipynb and .md files to html for viewing:
```
<your path to python3> <your path>/convert_to_html.py \ 
-d <your dir to be crawled> \ 
-o <your path>/<your index filename> 
```
3. Host the dashboard to search the documents
```bash
<your path to python3> <your path>/dash.py \ 
-d <your path>/<your index filename> 
```

### Docker image
A dockerfile is included with the project to build an image to host the search tool:

```
docker build -t my_search_app .
docker run -v <full path to folder to index>:/my_input -p 9999:8050 my_search_app
```
