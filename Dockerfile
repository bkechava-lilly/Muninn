FROM python:3

RUN apt-get update

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD search/ /search/

CMD python search/convert_to_html.py -d /my_input -o /my_index && python search/dashboard.py -d /my_index
