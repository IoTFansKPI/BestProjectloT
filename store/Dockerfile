FROM python:3.13-slim

EXPOSE $PORT

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install poetry


WORKDIR /usr/store
# copy the content of the local src directory to the working directory
COPY . .

ENV PYTHONPATH=/usr/store/src/store/

# Creates a non-root user with an explicit UID and adds permission to access the /usr/store/src/ folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/store
USER appuser
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE $PORT

CMD poetry run uvicorn src.store.main:app --host 0.0.0.0 --port $PORT