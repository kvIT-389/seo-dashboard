# SEO Dashboard

## Установка

Следующие шаги установки были протестированы на ОС Ubuntu версии 22.04

### Установка компонентов

```cmd
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev libpq-dev \
  postgresql postgresql-contrib
```

### Настройка базы данных

```cmd
$ sudo -u postgres psql
```

Создание пользователя:

```cmd
postgres=# CREATE USER seo_db_user WITH PASSWORD '<db password>';
```

Настройка пользователя:

```cmd
postgres=# ALTER ROLE seo_db_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE seo_db_user SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE seo_db_user SET timezone TO 'UTC';
```

Создание базы данных и выдача прав доступа пользователю:

```cmd
postgres=# CREATE DATABASE seo_db;
postgres=# GRANT ALL PRIVILEGES ON DATABASE seo_db TO seo_db_user;
```

Выход:

```cmd
postgres=# \q
```

### Настройка сервера

Все действия выполняются в каталоге ./server

Установка виртуальной среды:

```cmd
$ python3 -m pip install virtualenv
$ python3 -m virtualenv .venv
```

Активация виртуальной среды:

```cmd
$ source .venv/bin/activate
```

Установка зависимостей:

```cmd
$ pip install -r requirements.txt
```

Создание и применение миграций:

```cmd
$ python manage.py makemigrations
$ python manage.py migrate
```

Запуск сервера:

```cmd
$ python manage.py runserver
```

### Настройка переменных среды

Для корректной работы с базой данных, а также с API Метрики и Topvisor'а, необходимо создать файл с переменными среды, содержащим пароли, токены и прочие данные.

Создание файла:

```cmd
$ python create_dotenv.py
```

Запуск данного скрипта создаст файл .env с переменными, который необходимо заполнить.

- [Получение токена Яндекс.Метрики](https://yandex.ru/dev/metrika/doc/api2/intro/authorization.html)
- [Получение API-ключа Topvisor'а](https://topvisor.com/ru/api/v2/#)

После обновления данного файла желательно перезапустить сервер.

### Настройка клиентского приложения

Все действия выполняются в каталоге ./client

Установка менеджера npm (если отсутствует):

```cmd
sudo apt-get install npm
```

Установка зависимостей:

```cmd
npm install
```

Запуск dev-сервера:

```cmd
npm run dev
```

## Использование API сервера

Адреса сервера и клиента (при запуске на локальном сервере):

- [Сервер](http://localhost:8000)
- [Клиент](http://localhost:5173)

Сервер не имеет корня страницы, так как предназначен только для получения данных от него.

### Получение данных

По адресу `/api/get/<категория данных>` можно получить загруженные в БД данные, дополнительно указав в параметрах запроса `date1` и `date2` - начало и конец периода, за который необходимо получить данные.

Категории данных:

- `new_users` - посещения и новые пользователи по датам;
- `traffic_sources` - источники траффика;
- `device_categories` - типы устройств пользователей;
- `search_engines` - поисковые системы;
- `search_phrases` - поисковые фразы (сегментация траффика);
- `goals` - статистика по выполнению настроенных целей;
- `positions` - позиции сайта;
- `tops` - процент выдачи в топ-10.

К каждому запросу можно добавлять параметры `date1` и `date2` для выбора периода, за который необходимо получить статистику.

### Загрузка данных

По адресу `/api/load/<категория данных>` можно загрузить данные в БД, которые будут автоматически загружены с соответствующего сервиса.

Категории данных:

- `visits` - загрузка всех необходимых данных из Яндекс.Метрики. Начало и окончание периода, за который необходимо выгрузить данные - `date1` и `date2` соответственно.
- `positions` - загрузка данных по позициям из Topvisor'а. Данные загружаются за период с 1-го числа предыдущего месяца и по текущую дату. Однако период можно сдвигать заменой текущей даты на какую-либо еще, передав ее в параметре `ref_date`
- `tops` - загрузка данных по выдаче в топ-10 из Topvisor'а. Работа с датами происходит аналогичным образом, как с позициями.
