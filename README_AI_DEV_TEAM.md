# 🤖 AI Development Team - Система виртуальных разработчиков

Полнофункциональная система AI агентов (на основе Claude), которые работают как виртуальная команда разработчиков для создания полных сервисов.

```
┌─────────────────────────────────────────────┐
│     👨‍💼 PM Agent (Управление)             │
├─────────────────────────────────────────────┤
│  👨‍💻 Backend  │  👩‍💻 Frontend  │  🚀 DevOps  │
│  Developer    Developer      Engineer       │
└─────────────────────────────────────────────┘
         ⬇️  Каждый генерирует:
    ✅ Production-ready код
    ✅ Unit + Integration тесты
    ✅ Документацию
    ✅ Deployment конфиги
```

## 📋 Содержание

- [Что это такое](#что-это-такое)
- [Как это работает](#как-это-работает)
- [Требования](#требования)
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Примеры использования](#примеры-использования)
- [Архитектура](#архитектура)
- [API агентов](#api-агентов)

---

## 🎯 Что это такое

**AI Development Team** - это система, которая использует Claude AI для:

1. **Планирования** (PM Agent)
   - Разбивка требований на задачи
   -估计времени
   - Координация агентов

2. **Backend разработки** (Backend Developer Agent)
   - REST API endpoints
   - Database models & migrations
   - Business logic & services
   - Unit + Integration tests

3. **Frontend разработки** (Frontend Developer Agent)
   - React компоненты
   - Pages и layouts
   - State management (Zustand)
   - API интеграция
   - Component tests

4. **DevOps** (DevOps Engineer Agent)
   - Dockerfile & docker-compose
   - GitHub Actions CI/CD
   - Deployment scripts
   - Kubernetes manifests
   - Monitoring setup

5. **Вывода готового продукта**:
   - ✅ Production-ready код
   - ✅ Comprehensive тесты (80%+ coverage)
   - ✅ Complete документация
   - ✅ Deployment скрипты
   - ✅ Monitoring configuration

---

## 🔄 Как это работает

### 1. Вы предоставляете требования

```python
config = ProjectConfig(
    name="My Service",
    description="...",
    tech_stack={...},
    requirements="""
    1. User authentication
    2. Chat interface
    3. File upload
    ...
    """
)
```

### 2. PM Agent планирует спринт

```
📋 PM разбивает требования на 20+ конкретных задач
   ├─ Backend: auth API, chat endpoints, file handling
   ├─ Frontend: login page, chat UI, file upload
   └─ DevOps: Docker, CI/CD, monitoring
```

### 3. Агенты работают параллельно

```
⚙️ Параллельная разработка:
   ├─ Backend Agent → api/endpoints/*.py, models/*.py, tests/*.py
   ├─ Frontend Agent → components/*.tsx, pages/*.tsx, tests/*.test.tsx
   └─ DevOps Agent → Dockerfile, docker-compose.yml, .github/workflows/
```

### 4. Вы получаете готовый сервис

```
📁 ai_assistant/
   ├── src/              (Backend код)
   ├── tests/            (Тесты - 80%+ coverage)
   ├── frontend/         (React код)
   ├── Dockerfile        (Production-ready)
   ├── docker-compose.yml
   ├── .github/workflows/ci-cd.yml
   ├── README.md         (Полная документация)
   └── deploy.sh         (Deploy скрипт)
```

---

## 📋 Требования

- **Python 3.10+**
- **Anthropic API Key** (от Claude)
- **Git** (опционально)

---

## 🚀 Установка

### 1. Клонировать или скопировать файлы

```bash
# Создать папку проекта
mkdir ai-dev-team
cd ai-dev-team

# Скопировать файлы
cp ai_dev_team_starter.py .
cp usage_examples.py .
```

### 2. Установить зависимости

```bash
# Создать virtual environment
python -m venv venv

# Активировать
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install anthropic
```

### 3. Добавить API ключ

```bash
# Создать .env файл
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Или экспортировать как переменную окружения
export ANTHROPIC_API_KEY="sk-ant-..."
```

Получить ключ: https://console.anthropic.com/

---

## ⚡ Быстрый старт

### Минимальный пример

```python
import asyncio
from ai_dev_team_starter import PMAgent, ProjectConfig

async def main():
    # Создать конфиг проекта
    config = ProjectConfig(
        name="My Todo App",
        description="Simple Todo application",
        root_path="./my_todo_app",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL"
        },
        requirements="""
        1. User registration and login
        2. Create, read, update, delete todos
        3. Todo filtering and search
        4. Share todos with other users
        """
    )
    
    # Создать PM Agent
    pm = PMAgent(config)
    
    # Спланировать спринт
    sprint = await pm.plan_sprint("Sprint 1: MVP", duration_days=5)
    
    # Выполнить спринт
    results = await pm.execute_sprint(sprint)
    
    # Показать отчет
    report = pm.get_sprint_report()
    print(f"✅ Создано {report['generated_files']} файлов!")

if __name__ == "__main__":
    asyncio.run(main())
```

### Запустить

```bash
python main.py
```

### Результат

```
AI Development Team создаст в папке ./my_todo_app:

✅ Backend код:
   - FastAPI endpoints для CRUD операций
   - SQLAlchemy models
   - User authentication service
   - Database migrations

✅ Frontend код:
   - React компоненты
   - Todo list страница
   - Add todo форма
   - Settings страница

✅ Tests (80%+ coverage):
   - Unit tests для endpoints
   - Integration tests
   - Component tests для React

✅ DevOps:
   - Dockerfile
   - docker-compose.yml
   - GitHub Actions workflow

✅ Документация:
   - README.md с инструкциями
   - API documentation
   - Setup guide
```

---

## 💡 Примеры использования

### Пример 1: Простой API сервис

```python
await example_1_simple_api()
```

Создаст: REST API для управления TODO

### Пример 2: Полный стек (Backend + Frontend + DevOps)

```python
await example_2_full_stack()
```

Создаст: Expense Tracker приложение (B+F+D)

### Пример 3: Итеративная разработка

```python
await example_3_iterative_development()
```

Создаст: Social Network MVP в 5 спринтах

### Пример 4: Одна задача для одного агента

```python
await example_4_single_agent_task()
```

Создаст: Payment processing endpoint

### Пример 5: Полный реальный сервис

```python
await example_6_full_real_world_service()
```

Создаст: Полный AI Personal Assistant сервис

---

## 🏗️ Архитектура

### PM Agent (Project Manager)

```python
pm = PMAgent(config)

# Спланировать спринт (разбивает требования на задачи)
sprint = await pm.plan_sprint("Sprint 1", duration_days=7)

# Выполнить спринт (координирует агентов)
results = await pm.execute_sprint(sprint)

# Получить отчет
report = pm.get_sprint_report()
```

### Backend Agent

```python
backend = BackendAgent()

# Выполнить задачу API endpoint
result = await backend.execute_task(api_task)

# Результат: production-ready FastAPI код + тесты
```

**Может создавать:**
- REST API endpoints
- Database models (SQLAlchemy)
- Business logic services
- Database migrations (Alembic)
- Unit & integration tests (pytest)

### Frontend Agent

```python
frontend = FrontendAgent()

# Выполнить задачу React компонента
result = await frontend.execute_task(component_task)

# Результат: production-ready React код + тесты
```

**Может создавать:**
- React компоненты (TypeScript)
- Pages с layouts
- Zustand stores
- API service clients
- Component tests (Jest + RTL)

### DevOps Agent

```python
devops = DevOpsAgent()

# Выполнить задачу Docker
result = await devops.execute_task(docker_task)

# Результат: Dockerfile, docker-compose, CI/CD, monitoring
```

**Может создавать:**
- Dockerfile (optimized multi-stage)
- docker-compose.yml
- GitHub Actions workflows
- Deployment scripts (bash)
- Kubernetes manifests
- Monitoring configs (Prometheus/Grafana)

---

## 🔌 API агентов

### Task структура

```python
task = Task(
    id="auth_api",                    # Уникальный ID
    title="Implement Auth API",       # Название
    description="Create JWT auth...", # Описание
    agent="backend",                  # backend|frontend|devops
    priority="high",                  # high|medium|low
    estimated_hours=8.0,              # Оценка времени
    status="pending"                  # pending|in_progress|completed
)
```

### Sprint структура

```python
sprint = Sprint(
    id="sprint_1",
    name="Sprint 1: MVP",
    duration_days=7,
    status="in_progress",
    tasks=[task1, task2, ...],
    start_date="2024-01-15",
    metrics={...}
)
```

### ProjectConfig структура

```python
config = ProjectConfig(
    name="Service Name",
    description="Description",
    root_path="./service",
    tech_stack={
        "backend": "Python + FastAPI",
        "frontend": "React + TypeScript",
        "database": "PostgreSQL",
        "devops": "Docker + GitHub Actions"
    },
    requirements="Detailed requirements..."
)
```

---

## 📊 Что генерируется

### Backend файлы

```
src/
├── api/
│   └── endpoints/
│       ├── auth.py
│       ├── users.py
│       ├── chats.py
│       └── ...
├── models/
│   ├── user.py
│   ├── chat.py
│   └── ...
├── services/
│   ├── auth_service.py
│   ├── chat_service.py
│   └── ...
└── utils/
    ├── validators.py
    ├── exceptions.py
    └── ...

tests/
├── test_auth.py
├── test_chat.py
└── ...
```

### Frontend файлы

```
src/
├── pages/
│   ├── Login.tsx
│   ├── Chat.tsx
│   ├── Settings.tsx
│   └── ...
├── components/
│   ├── ChatWindow.tsx
│   ├── FileUpload.tsx
│   └── ...
├── services/
│   └── api.ts
├── stores/
│   ├── authStore.ts
│   ├── chatStore.ts
│   └── ...
└── types/
    ├── auth.ts
    ├── chat.ts
    └── ...

tests/
├── components.test.tsx
├── pages.test.tsx
└── ...
```

### DevOps файлы

```
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci-cd.yml
│       └── tests.yml
├── infra/
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ...
│   └── monitoring/
│       ├── prometheus.yml
│       ├── grafana-dashboard.json
│       └── ...
├── scripts/
│   ├── deploy.sh
│   ├── migrate.sh
│   └── ...
└── docs/
    ├── README.md
    ├── API.md
    ├── SETUP.md
    ├── DEPLOYMENT.md
    └── ARCHITECTURE.md
```

---

## 📈 Метрики спринта

После завершения спринта получите отчет:

```
{
  "sprint_id": "sprint_1",
  "sprint_name": "Sprint 1: MVP",
  "status": "completed",
  "tasks": {
    "total": 24,
    "completed": 24,
    "completion_rate": "100%"
  },
  "generated_files": 87,
  "agents": {
    "backend": {
      "name": "BackendAgent",
      "completed_tasks": 8,
      "generated_files": 35
    },
    "frontend": {
      "name": "FrontendAgent",
      "completed_tasks": 8,
      "generated_files": 28
    },
    "devops": {
      "name": "DevOpsAgent",
      "completed_tasks": 8,
      "generated_files": 24
    }
  }
}
```

---

## 🔐 Security considerations

Система генерирует код со встроенной безопасностью:

✅ **Backend:**
- Password hashing (bcrypt)
- JWT token validation
- SQL injection prevention (ORM)
- CORS configuration
- Input validation
- Rate limiting support

✅ **Frontend:**
- XSS prevention (React auto-escaping)
- CSRF tokens
- Secure token storage
- HTTPS support
- Input sanitization

✅ **DevOps:**
- Non-root users в Docker
- Secret management
- Health checks
- Monitoring & alerting
- Log aggregation

---

## 🚀 Развертывание

### Локально

```bash
cd generated_project
docker-compose up -d
# Доступно на http://localhost:3000 (frontend)
# API на http://localhost:8000 (backend)
```

### На сервер

```bash
cd generated_project
bash scripts/deploy.sh
# Или
kubectl apply -f infra/k8s/
```

---

## 📚 Документация

Каждый сгенерированный проект включает:

- **README.md** - Полное описание проекта
- **API.md** - OpenAPI/Swagger документация
- **SETUP.md** - Инструкции по локальному запуску
- **DEPLOYMENT.md** - Deployment guide
- **ARCHITECTURE.md** - Technical architecture docs

---

## 🐛 Troubleshooting

### "API key not found"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Rate limit exceeded"
Уменьшите количество параллельных спринтов или добавьте задержку.

### Долгая генерация кода
Это нормально - Claude думает перед написанием кода. Может занять 5-30 минут на спринт.

---

## 💬 Feedback & Improvements

Если вы хотите кастомизировать:

1. **System prompts** - Отредактируйте `SYSTEM_PROMPT` в каждом агенте
2. **Task templates** - Добавьте новые типы задач в методы агентов
3. **Output structure** - Измените структуру генерируемых файлов
4. **Tech stack** - Используйте другие фреймворки в requirements

---

## 📝 License

MIT License - используйте свободно!

---

## 🎯 Примеры использования в реальном мире

### Стартап разработка
```python
# Разработать MVP за 2 недели вместо 2 месяцев
sprint = await pm.plan_sprint("MVP Sprint", duration_days=14)
await pm.execute_sprint(sprint)
# Результат: полный рабочий продукт с кодом, тестами и deployment
```

### Быстрая разработка фич
```python
# Добавить фичу в существующий проект
sprint = await pm.plan_sprint("Feature: Notifications", duration_days=3)
# Получите API endpoints, UI components, tests и deployment готово
```

### Обучение & Прототипирование
```python
# Выучить новый стек или создать прототип быстро
sprint = await pm.plan_sprint("Learning Sprint", duration_days=1)
# Увидите production-ready code как ориентир
```

---

## 🌟 Что дальше

1. **Используйте generated код** как основу
2. **Кастомизируйте** под специфические требования
3. **Добавляйте бизнес-логику** которую не может сделать AI
4. **Экспортируйте в production** с уверенностью

---

**Happy Development! 🚀**
