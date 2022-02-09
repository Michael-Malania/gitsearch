FROM python:3.9

WORKDIR /

ADD . /

RUN pip install --editable .

ENTRYPOINT ["gitsearch"] 
