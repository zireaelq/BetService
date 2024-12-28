# BetService

Сервис управлением событиями и ставками на эти события.\
*тестовое задание*

## Основные функции

- **Line Provider**
  - CRUD событий с сохранением в Redis
  - Кэширование событий
  - callback при обновлении статуса события
- Bet Maker
  - Создание/просмотр ставок
  - Получение событий из line provider
  - обработка callback обновления статуса события

Все взаимодействия с внешними сервисами осуществляются в асинхронном режиме.\
Все сервисы докеризированы и управляются через docker compose.\
Все данные хранятся в Redis.\
Предусмотрено демонстрационное тестирование через Pytest.

## Основные технологии

- **Фреймворк**: FastAPI
- **Контейнеризация**: Docker, Docker Compose
- **База данных**: Redis

## Зависимости

- **[Docker](https://www.docker.com/)**
- **[Docker Compose](https://docs.docker.com/compose/)**
- **[Make](https://www.gnu.org/software/make/manual/make.html)**

## Установка и запуск

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/zireaelq/BetService.git
   cd BetService
   ```

2. **Переименуйте .example.env в .env**

3. **Запустите сервисы через Makefile и Docker:**

   ```bash
   make test
   ```

