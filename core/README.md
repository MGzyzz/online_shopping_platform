# Основной сервис Online shopping platform

## Описание
Данный проект является комплексным решением для управления интернет-магазином. Он включает в себя несколько основных модулей: `accounts`, `api`, и `shop`, каждый из которых выполняет свои специализированные функции.

## Модуль `accounts`

### Функции
- Управление учетными записями пользователей.
- Регистрация и аутентификация пользователей.
- Управление профилем пользователя, включая изменение пароля и контактной информации.
---
- За регистрацию и аунтентификацию отвечают классы `LoginView, LoginPageView, RegisterView`.
- путь: `accounts/views.py`.
---
- Верификация по телефону. За верификацию отвечает класс `Sms-Verification`.
- Путь `accounts/views.py`.



### Взаимодействие
- Обрабатывает запросы от пользователей через веб-интерфейс.
- Взаимодействует с модулем `api` для обработки данных, связанных с учетными записями.

## Модуль `api`

### Функции
- Предоставляет API для взаимодействия с внешними сервисами
- Управление данными пользователя, продуктами, заказами и т.д.
- Интеграция с внешними платежными системами и сервисами доставки.

### Взаимодействие
- Обрабатывает запросы от модуля `shop` и `accounts` для предоставления необходимых данных.
- Взаимодействует с внешними API для расширения функциональности.
- Обрабатывает сохрание данных об `заказе` и создание `фискализационого чека`.
-  основной класс `CreateCheck`.
- класс `TelegramShopsViewSet` отвечает за показ данных в телеграм боте.



## Модуль `shop`

### Функции
- Управление каталогом товаров, включая добавление, редактирование и удаление товаров.
- Управление заказами, скидками и акциями.
- Отображение товаров и информации о магазине в пользовательском интерфейсе.

### Взаимодействие
- Взаимодействует с модулем `accounts` для получения информации о пользователях и их заказах.
- Использует `api` для обработки заказов, платежей и других операций.
- Папка `views` используется для отображение данных на страницах сайта.

## Второстепенные файлы приложение
- `admin.py` отвечает за показ данных в административной панели.
- `forms.py` отвечает за проверку данных во время их получение.
- `tests.py` выполнят тесты.
- `urls.py` - отвечает за установление путей для каждого класса.

## Static Файлы `JavaScripts`

### Взаимодействие
- Обрабатывает на стороне front-end запросы такие как `login`, `register`, `sms`, `payments`, `telegram_page` и т.д.


## Примечания
- Убедитесь, что у вас установлены все необходимые зависимости, указанные в файле `reqs.txt`.
- Для запуска проекта используйте `docker-compose`, конфигурации для разработки и продакшена находятся в соответствующих файлах `docker-compose`.
- Для запуска на стороне разработки используете команду `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`.
- Для запуска на стороне сервера используете команду `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`.