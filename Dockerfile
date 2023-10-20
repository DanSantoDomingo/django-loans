FROM python:3.11.2-buster


RUN mkdir /source
WORKDIR /source

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin

# Update `pip` and `setuptools`
RUN pip install -U pip setuptools


COPY . /source
RUN pip install poetry
# Install project dependencies with Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
