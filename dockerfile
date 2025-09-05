FROM python:3.13-slim
COPY . /app
WORKDIR /app
RUN poetry install
RUN poetry run alembic upgrade head
EXPOSE 8000
CMD ["python", "run.py"]