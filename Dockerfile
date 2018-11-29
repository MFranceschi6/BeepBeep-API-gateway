FROM python:3.6.7-jessie
MAINTAINER "Butter Group"
EXPOSE 5000
ADD requirements.txt ./app/
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app
RUN python setup.py develop
CMD ["beepbeep-apigateway"]