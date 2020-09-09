# Импорт новостей Top50

Агрегатор новостей проекта Top50. Является утилитой в поддержку RoR приложение top52 (https://github.com/artzlt/top52/).

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
$ git clone https://github.com/brcke/top52-news-fetcher.git ./
$ cd top52-news-fetcher
$ ./config/install.bash
```

Если разворачивается на чистой машине, то рекомендуется сперва убедиться, что установлен **sudo**, а далее установить **npm**. Сделать это можно, например, с помощью такой последовательности команд: 

```bash
$ curl -sL https://deb.nodesource.com/setup_9.x | bash -
$ sudo apt-get install -y nodejs
```

Инструкции по установке можно найти в следующем разделе.

## Полезные ссылки
* [Инструкция по установке npm](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions)
* [Troubleshooting](https://github.com/npm/npm/wiki/Troubleshooting)
* [Установка npm и nodejs на Debian сервере](https://www.rosehosting.com/blog/how-to-install-nodejs-bower-and-gulp-on-debian-8/)

## Запуск

```bash
$ ./config/run.bash --port <port>
```

> По умолчанию разворачивается на порту 5000.
