# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl libpq-dev python3-dev gcc postgresql postgresql-contrib

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy only the dependencies file to optimize rebuilding the Docker image
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the Flask port
EXPOSE 5000

CMD ["sh", "-c", "while ! pg_isready -q -h $DB_HOST -p $DB_PORT; do sleep 1; done; poetry run python create_table.py && poetry run python app.py"]
