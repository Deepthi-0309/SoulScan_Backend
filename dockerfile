FROM public.ecr.aws/docker/library/python:3.10

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /code/


COPY ./requirements.txt /code/


RUN pip install -r requirements.txt

COPY . /code/


EXPOSE 5000

CMD ["python","main.py"]

