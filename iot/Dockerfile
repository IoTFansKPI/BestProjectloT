# Use the official Python image as the base image
FROM python:3.9-slim
# Set the working directory inside the container
WORKDIR /app
# Copy the entire application into the container
COPY . .
RUN pip3 install poetry && poetry lock && poetry install
# Run the main.py script inside the container when it starts
CMD ["poetry", "run", "python", "/app/main.py"]
