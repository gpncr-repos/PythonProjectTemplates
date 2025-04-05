FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --no-cache-dir poetry==1.8.5
RUN poetry export --without-hashes --format=requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 7777

CMD ["python3", "-u", "main.py"]
