#### Запуск и настройка

* Быстрый запуск.

    * Нужен `docker` и `docker-compose` выполняем команду `make up` (или
      `docker-compose -f docker/docker-compose.app.yaml up --pull always --force-recreate` если `make` по какой то
      причине нету в системе).
    * Переходим по [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    * Пробуем работать с API.

* Локальное развёртывание

    * Установить [Poetry](https://python-poetry.org/docs/#installation)
    * Установить зависимости `poetry install --no-root`
    * Запустить инфраструктуру (Postgres и Elastic) `make infra`
    * Мигрировать БД - `make migrate`
    * Настроить переменные окружения (описание ниже) - `cp .env.example .env` с последующем редактированием `.env`
    * Запустить приложение `make app`

#### Переменные окружения

| ENV                   | Описание                                                                         | required | default                                                    |
|-----------------------|----------------------------------------------------------------------------------|----------|------------------------------------------------------------|
| `ORGZ_DATA_BASE_DSN`  | Строка подключения в БД                                                          | +        | `postgresql+asyncpg://postgres:password@127.0.0.1:5557/db` |
| `ORGZ_API_KEY`        | Ключ для доступа к API                                                           | +        |                                                            |
| `ORGZ_DATA_BASE_ECHO` | Подробное логирование в SQLAlchemy                                               | -        | `yes`                                                      |
| `ORGZ_FORCE_RECREATE` | При каждом запуске пересоздавать Elastic Search Index и перезаливать данные в БД | -        | `no`                                                       |
| `ORGZ_USE_FAKE_DATA`  | Использовать сгенерированные данные для наполнения БД и поискового индекса       | -        | `no`                                                       |
| `ORGZ_LOG_LEVEL`      | Уровень логирования                                                              | -        | `INFO`                                                     |
| `ORGZ_ELASTIC_HOST`   | Адрес хоста с Elastic Search                                                     | -        | `http://localhost:9200`                                    |
| `ORGZ_ES_INDEX_NAME`  | Название поискового индекса                                                      | -        | `orgz-index`                                               |

#### Описание REST API

##### !!!WARNING!!!

При обращению к любому API требуется указывать заголовок `X-ORGZ-Key`.

##### Организации

* [/api/v1/organization/id/{org_id}](/api/v1/organization/id/{org_id})

  Получение информации об `Организации` по её ID.
* [/api/v1/organization/building/{building_id}](/api/v1/organization/building/{building_id})

  Список `Организаций` в `Здании` `{building_id}`.

* [/api/v1/organization/activity/{activity_id}](/api/v1/organization/activity/{activity_id})

  Список `Организаций` принадлежащих `Виду деятельности` `{activity_id}`.

  Без учёта дочерних `Видов деятельности`.
* [/api/v1/organization/geo](/api/v1/organization/geo)

  Список `Организаций`, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на
  карте.
* [/api/v1/organization/search](/api/v1/organization/search)

  Поиск `Организаций` по `Адресу Здания`, `Названию Организации`, `Названию Вида Деятельности`.
  При поиске по `Названию Вида Деятельности` учитываются все дочерние `Виды Деятельности`.
  Возможно частичное совпадение.

##### Виды Деятельности

* [/api/v1/activity/all/](/api/v1/activity/all/)

  Получения дерева всех видов деятельности.
* [/api/v1/activity/name](/api/v1/activity/name)

  Искать вид деятельности по названию. Возможно частичное совпадение.

  Ответ - древовидная структура найденного вида деятельности и его потомков.

##### Здания

* [/api/v1/building/address](/api/v1/building/address)

  Поиск `Зданий` по адресу, возможно частичное совпадение.
* [/api/v1/building/geo](/api/v1/building/geo)

  Список `Зданий`, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте.
