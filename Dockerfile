FROM python:3.6

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt
RUN pip install -U /code

ENTRYPOINT ["python", "./update_ssspend_summary.py"]
