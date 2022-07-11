FROM python:3.8

RUN apt-get clean \
    && apt-get -y update

# RUN apt-get -y install \
#     nginx \
#     python3-dev \
#     build-essential

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./gunicorn.sh"]