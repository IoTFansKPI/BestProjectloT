# set base image (host OS)
FROM python:latest
# set the working directory in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install poetry

WORKDIR /usr/agent
# copy the content of the local src directory to the working directory
COPY . .
ENTRYPOINT ["./entrypoint.sh"]
# command to run on container start
CMD ["poetry", "run", "python", "src/agent/main.py"]