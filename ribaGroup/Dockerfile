# 1. Используем базовый образ Python
FROM python:3.10-slim

# 2. Устанавливаем переменные среды для оптимизации работы
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Создаем рабочую директорию внутри контейнера
WORKDIR /ribaGroup

# 4. Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /ribaGroup/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Копируем всё содержимое проекта внутрь контейнера
COPY . /ribaGroup/

# 6. Запускаем приложение
CMD ["python", "manage.py", "runserver"]
