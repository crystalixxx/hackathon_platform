# Hackathon Platform

## 📄 Аннотация

Этот проект представляет собой онлайн-платформу для организации и участия в соревнованиях по программированию, 
хакатонах и кейс-чемпионатах. Проект разработан в рамках курсовой работы 2-ого курса.

## Ожидаемый результат

Ожидаемый результат — высоконагруженная микросервисная архитектура с элементами социальной активности, которое поддерживает проведение 
мероприятий и командное / индивидуальное участие прямо на платформе, с real-time уведомлениями, загрузкой решений, тестирующей системой 
для олимпиад и интеграцией дополнительного контента от организаторов.

## 👥 Команда

### 🔧 **Другов Максим**  
- Роли: Fullstack / DevOps / Data Engineer
---

### 🖥️ **Жемуков Альберт**  
- Роль: Backend

## 📂 Микросервисы

- Микросервис пользователей и команд
- Микросервис мероприятий
- Микросервис тестирования
- Микросервис уведомлений и чатов
- Микросервис блогов и новостей

## Что реализовано на данный момент:

- RESTful API для микросервиса пользователей и команд
- Настроена базовая инфраструктура:
  - СУБД Redis и PostgreSQL
  - LoadBalancer / Proxy Traefic
- Python:
  - Имплементация паттернов UnitOfWork, Repository, Service для работы с транзакциями
  - Реализация моделей, схем, миграций PgSQL с помощью SQLAlchemy и Alembic
  - JWT аутентификация

## В работе:

- Настройка инфрастуктуры и написание RESTful API для микросервиса мероприятий
- Интеграция YDB: интеграция в инфраструктуру, настройка, написание соответствующего репозитория
- Написание Frontend'а для микросервисов мероприятий и пользователей и команд.

## Видео-отчет

---

## 🛠️ Стек технологий

### Backend
- **Язык программирования**: Python
- **Основной фреймворк**: FastAPI
- **Работа с базами данных**:
  - `SQLAlchemy + asyncpg` для ORM.
  - `Alembic` для миграций.
  - `Redis` для работы с Redis.
  - `PyMongoDB` для работы с MongoDB.
- **Очереди и задачи**: Celery + Kafka
- **Тестирование**:
  - `pytest` + `pytest_postgresql` + `coverage`.
- **Линтеры и статистический анализ кода**:
  - `ruff` + `pre-commit`
- **Валидация данных**: `pydantic` + `pydantic settings`.
- **Авторизация и безопасность**:
  - `JWT (pyjwt)` для JWT токенов.

### Frontend
- **Язык программирования**: JavaScript.
- **Основной фреймворк**: React
- **Дополнительные библиотеки**:
  - `react-router-dom` для маршрутизации.
  - `react-hook-form` для работы с формами.

### Базы данных
- **Реляционная СУБД**: PostgreSQL
- **Ключ-значение**: Redis.
- **Документоориентированная СУБД**: MongoDB

### DevOps
- **Контейнеризация**: Docker + Docker Compose.
- **CI/CD**: GitHub Actions + Kubernetes.

## Инструкция по деплою

![Попугаи на хакатоне](images/26683997-5d17-4e5a-a651-4971ea7bccd3.webp)
---
