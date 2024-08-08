#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    # если база еще не запущена
    echo "база еще не запущена..."

    # Проверяем доступность хоста и порта
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "DB did run."
fi
# Удаляем все старые данные
#### python manage.py flush --no-input
# Выполняем миграции
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
exec "$@"