FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ribaGroup

RUN apk --update add \
    gcc libc-dev libffi-dev jpeg-dev zlib-dev libjpeg \
    && pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . ./

RUN python manage.py collectstatic --noinput

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/ribaGroup/entrypoint.sh"]
