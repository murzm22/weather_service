FROM python:3.13-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install --no-cache-dir pipenv \
    && pipenv install --system --deploy --ignore-pipfile

COPY . /app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
