# Импорт новостей Top50

Аггрегатор новостей проекта Top50. Является утилитой в поддержку RoR приложение top52.

Основные возможности:

* Импорт новостей из [parallel.ru](http://www.parallel.ru/news)
* Хранение новостей в базе данных
* Обновление новостей по заданному таймеру

## Требования

1. Установить все необходимые пакеты (в скрипте `config/install.bash`)
2. Развернуть RoR приложение top52 и выполнить миграции
3. Заполнить пользователя и название базы (`config/database.yml`)

## Установка

```bash
$ git clone https://github.com/mozharovsky/parallels-news.git ./
$ cd parallel-news
$ ./config/install.bash
```

## Запуск

```bash
$ ./config/run.bash
```
