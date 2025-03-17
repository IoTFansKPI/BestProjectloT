FROM python:3.13-slim

EXPOSE $PORT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install poetry


WORKDIR /usr/store
# copy the content of the local src directory to the working directory
COPY . .

ENV PYTHONPATH=/usr/store/src/store/

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE $PORT

CMD poetry run uvicorn src.store.main:app --host 0.0.0.0 --port $PORT