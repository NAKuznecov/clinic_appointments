FROM python:3.9

RUN mkdir /appointments

WORKDIR /appointments

COPY . .

# Установим Poetry
RUN pip install poetry

# Настроим конфигурацию Poetry для глобальной установки зависимостей
RUN poetry config virtualenvs.create false && poetry config virtualenvs.in-project true

# Обновляем кэш PyPI
RUN poetry cache clear pypi --all

# Устанавливаем зависимости напрямую в проект
RUN poetry install --no-root

RUN poetry run alembic upgrade head

CMD ["./wait-for-it.sh", "db:5432", "poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
