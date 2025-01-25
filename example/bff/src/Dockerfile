FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --no-cache-dir poetry
RUN poetry export --without-hashes --format=requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
