FROM python:3.8.7

# set work directory
WORKDIR /code

ENV FLASK_APP=ocdskingfisherprocess.web.app
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
