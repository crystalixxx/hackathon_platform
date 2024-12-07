# Hackathon Platform

## 📄 Аннотация

Этот проект представляет собой онлайн-платформу для организации и участия в соревнованиях по программированию, 
хакатонах и кейс-чемпионатах. Проект разработан в рамках предмета Deep Python 2-го курса ПМИ ФКН ВШЭ, а также курсовой.

Онлайн-платформа для проведения соревнований по программированию, хакатонов и кейс-чемпионатов.  
Поддерживается функционал команд c возможность ее поиска для участия в мероприятиях через заполнение профиля 
(навыки, портфолио, примеры кода) и фильтрацию участников или команд; индивидуальное участие также поддерживается. 
Новые команды могут создаваться под разные мероприятия, где прикрепление к событию происходит либо индивидуально, 
либо через капитана команды.

Мероприятия включают атрибуты (название, описание, ссылки, тип, локация и т.д.) и связаны с пользователями. 
В рамках хакатонов и кейс-чемпионатов можно загружать материалы, общаться с модерацией, получать уведомления и 
дополнительные материалы от организаторов. Олимпиады предлагают аналогичную функциональность для решения задач и 
взаимодействия с организаторами, но при этом для них будет реализована тестирующая система.

Платформа будет отображать статистику каждого пользователя по занятым местам, баллам и статусу, а также иметь общий 
лидерборд и ссылки на сертификаты. Архивные мероприятия перемещаются вниз страницы. Дополнительно платформа поддерживает 
блог и новости сообщества.

Организаторы и модераторы выступают как системные пользователи с ограниченной видимостью. Поддержка специальных 
аккаунтов для HR специалистов с возможностью просмотра статистики всех мероприятий, доступу к аккаунтам и контактной 
информации участников. Дополнительные социальные функции включают ачивки за активность и призовые места, а также 
отображение аналитики по участию.

## Ожидаемый результат

Ожидаемый результат — высоконагруженное приложение с элементами социальной активности, которое поддерживает проведение 
мероприятий и командное участие прямо на платформе, с real-time уведомлениями, загрузкой решений, тестирующей системой 
для олимпиад и интеграцией дополнительного контента от организаторов.

## Актуальность решения

Существующие решения либо только информируют ([https://www.хакатоны.рус](https://www.хакатоны.рус), [https://www.хакатоны.рф](https://www.хакатоны.рф)),  
либо слишком узкие ([https://contest.yandex.ru](https://contest.yandex.ru) (олимпиады), [https://zavodit.ru](https://zavodit.ru) (хакатоны)).  

Предложенное решение будет полезно как для пользователей (1 аккаунт для участия в любых мероприятиях),  
так и для бизнеса (сотрудничество с одной платформой для проведения олимпиад, хакатонов, кейс-чемпионатов для поиска  
работников, создания MVP, получения идей).

## 👥 Команда

### 🔧 **Другов Максим**  
- Роли: Fullstack / DevOps / Data Engineer

---

### 🖥️ **Жемуков Альберт**  
- Роль: Backend

---

### 🚀 **Тимур Петров**  
- Самый крутой мужик в мире

---

### **Музаффар Садуллаев**
- Гений разработки
---

### 🦜 **Попугай**  
- Роль: Злодей-британец  
- Воплощение сарказма и циничного взгляда на разработку.

## 📂 Микросервисная структура проекта

- Сервис пользователей и команд
- Сервис мероприятий
- Сервис тестирования
- Сервис уведомлений и чатов

## Что реализовано на данный момент:

- CI/CD
- Сервис пользователей и команд (кэширование с Redis)

---

## 🛠️ Стек технологий

### Backend
- **Язык программирования**: Python
- **Основной фреймворк**: [FastAPI](https://fastapi.tiangolo.com)
- **Работа с базами данных**:
  - [SQLAlchemy](https://www.sqlalchemy.org/) для ORM.
  - [Alembic](https://alembic.sqlalchemy.org/en/latest/) для миграций.
- **Очереди и задачи**: [Celery](https://docs.celeryproject.org/en/stable/)
- **Тестирование**:
  - [pytest](https://docs.pytest.org/en/stable/) + coverage.
- **Форматирование кода**:
  - [ruff](https://github.com/charliermarsh/ruff) + [black](https://black.readthedocs.io/en/stable/).
- **Валидация данных**: [pydantic](https://pydantic-docs.helpmanual.io/) + pydantic settings.
- **Авторизация и безопасность**:
  - [pyjwt](https://pyjwt.readthedocs.io/) для JWT токенов.
  - [passlib](https://passlib.readthedocs.io/) для работы с хешированием паролей.
- **Дополнительно**:
  - Библиотеки для инфраструктуры: `pymongo`, `redis`, и др.

### Frontend
- **Язык программирования**: JavaScript.
- **Основной фреймворк**: [React](https://reactjs.org/)
- **Дополнительные библиотеки**:
  - `react-router-dom` для маршрутизации.
  - `react-hook-form` для работы с формами.

### Базы данных
- **Реляционная СУБД**: PostgreSQL
- **Ключ-значение**: Redis.
- **Документоориентированная СУБД**: MongoDB

### DevOps
- **Контейнеризация**: Docker + Docker Compose.
- **CI/CD**: GitHub Actions.

![Попугаи на хакатоне](26683997-5d17-4e5a-a651-4971ea7bccd3.webp)
---