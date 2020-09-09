# Импорт новостей Top50

Агрегатор новостей проекта Top50. Является утилитой в поддержку RoR приложение top52 (https://github.com/artzlt/top52/).

Основные возможности:

* Импорт новостей из [parallel.ru](https://www.parallel.ru/news)
* Хранение новостей в базе данных
* Обновление новостей по заданному таймеру

## Требования

1. Установить все необходимые пакеты (в скрипте `install.sh`)
2. Развернуть RoR приложение top52 и выполнить миграции
3. Заполнить пользователя и название базы (`config/database.yml`)

## Установка

```bash
$ git clone https://github.com/artzlt/top52-news-fetcher.git ./
$ cd top52-news-fetcher
$ ./install.sh  # устанавливаем pip и необходимые python-пакеты
```

## Запуск

```bash
$ ./fetcher.py
```

