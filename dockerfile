FROM python:alpine

RUN adduser --disabled-password cbrfuser

WORKDIR /home/cbrfuser

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY main.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R cbrfuser:cbrfuser ./
USER cbrfuser

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]