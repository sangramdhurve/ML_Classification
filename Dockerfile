FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y gcc \
python3-pip\
&& apt-get clean

RUN mkdir /usr/src/app

ADD ./requirements.txt /usr/src/app/

RUN pip3 install -r /usr/src/app/requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app
EXPOSE 5000
ENTRYPOINT ["python","/usr/src/app/src/api.py"]