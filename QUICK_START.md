# ⚡ Быстрый старт - AI Development Team

## 🎯 За 10 минут запустите разработку своего сервиса

### Шаг 1: Подготовка окружения (2 мин)

```bash
# 1. Клонировать/скопировать файлы
mkdir my_ai_dev_team
cd my_ai_dev_team

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# 3. Установить зависимость
pip install anthropic

# 4. Добавить API ключ (выбрать один вариант)

# Вариант A: Через .env файл
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Вариант B: Через переменную окружения
export ANTHROPIC_API_KEY="sk-ant-..."

# Вариант C: На Windows
setx ANTHROPIC_API_KEY "sk-ant-..."
```

**Где получить API ключ:**
- Перейти на https://console.anthropic.com/
- Create API Key
- Скопировать ключ

---

### Шаг 2: Написать конфиг проекта (2 мин)

Создать файл `main.py`:

```python
import asyncio
from ai_dev_team_starter import PMAgent, ProjectConfig

async def main():
    # ===== DEFINE YOUR PROJECT =====
    config = ProjectConfig(
        name="Your Service Name",
        description="What your service does",
        root_path="./output_project",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL",
            "devops": "Docker + GitHub Actions"
        },
        requirements="""
        BACKEND:
        1. User authentication (JWT)
        2. Chat API endpoints
        3. File upload support
        4. Database models
        
        FRONTEND:
        1. Login/Register pages
        2. Chat interface
        3. File upload UI
        4. Settings page
        
        DEVOPS:
        1. Docker setup
        2. CI/CD pipeline
        3. Deployment script
        4. Monitoring
        """
    )
    
    # ===== CREATE PM AGENT =====
    pm = PMAgent(config)
    
    # ===== PLAN SPRINT =====
    sprint = await pm.plan_sprint("Sprint 1: Full Stack", duration_days=7)
    
    # ===== EXECUTE SPRINT =====
    print("\n🚀 Starting development...\n")
    results = await pm.execute_sprint(sprint)
    
    # ===== GET REPORT =====
    report = pm.get_sprint_report()
    
    print("\n" + "="*60)
    print("✅ SPRINT COMPLETED!")
    print("="*60)
    print(f"Completed tasks: {report['tasks']['completed']}/{report['tasks']['total']}")
    print(f"Generated files: {report['generated_files']}")
    print(f"\n📁 Output directory: {config.root_path}")
    print("\n🚀 Next steps:")
    print(f"   cd {config.root_path}")
    print("   docker-compose up -d")
    print("   # Enjoy your new service!")

if __name__ == "__main__":
    asyncio.run(main())
```

---

### Шаг 3: Запустить разработку (1 мин)

```bash
python main.py
```

**Что происходит:**
1. ✅ PM Agent разбивает требования на задачи
2. ✅ Backend Agent генерирует API код + тесты
3. ✅ Frontend Agent генерирует React компоненты + тесты
4. ✅ DevOps Agent генерирует Docker + CI/CD + monitoring
5. ✅ Все файлы сохраняются в `./output_project`

**Время:** ~5-15 минут в зависимости от размера проекта

---

### Шаг 4: Использовать сгенерированный код (5 мин)

```bash
# Перейти в проект
cd output_project

# Запустить локально
docker-compose up -d

# Доступно на:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API docs: http://localhost:8000/docs

# Развернуть в production (когда готово)
bash scripts/deploy.sh
```

---

## 📋 Шаблоны для разных проектов

### Template 1: Simple API

```python
config = ProjectConfig(
    name="Simple API",
    description="RESTful API",
    root_path="./simple_api",
    tech_stack={
        "backend": "Python + FastAPI",
        "frontend": "None (API only)",
        "database": "PostgreSQL"
    },
    requirements="""
    1. User CRUD endpoints
    2. Authentication
    3. Database models
    4. Unit tests
    """
)
```

### Template 2: Web Application

```python
config = ProjectConfig(
    name="Web App",
    description="Full-stack web application",
    root_path="./web_app",
    tech_stack={
        "backend": "Python + FastAPI",
        "frontend": "React + TypeScript",
        "database": "PostgreSQL"
    },
    requirements="""
    1. User management
    2. Dashboard
    3. CRUD operations
    4. Responsive design
    5. Mobile support
    """
)
```

### Template 3: Full Production System

```python
config = ProjectConfig(
    name="Production Service",
    description="Enterprise-grade service",
    root_path="./enterprise_service",
    tech_stack={
        "backend": "Python + FastAPI",
        "frontend": "React + TypeScript",
        "database": "PostgreSQL",
        "devops": "Docker + Kubernetes + AWS"
    },
    requirements="""
    BACKEND:
    1. Microservices architecture
    2. Advanced auth (OAuth2, SSO)
    3. Payment processing
    4. Email notifications
    5. Analytics tracking
    6. Rate limiting & caching
    
    FRONTEND:
    1. Admin dashboard
    2. User portal
    3. Real-time notifications
    4. Advanced analytics
    5. Multi-language support
    
    DEVOPS:
    1. Auto-scaling setup
    2. Multi-environment deployment
    3. Prometheus monitoring
    4. ELK logging
    5. Disaster recovery
    """
)
```

---

## 🎯 Фреймворки/примеры

### Пример: Todo App

```python
requirements="""
BACKEND:
1. User registration/login
2. Create/Read/Update/Delete todos
3. Todo filtering and search
4. Share todos with users

FRONTEND:
1. Login page
2. Todo list page
3. Add/Edit todo forms
4. Share dialog

DEVOPS:
1. Docker setup
2. GitHub Actions CI/CD
3. Deployment script
"""
```

### Пример: E-commerce Platform

```python
requirements="""
BACKEND:
1. Product management
2. Shopping cart
3. Order processing
4. Payment integration (Stripe)
5. Email notifications
6. Admin dashboard API

FRONTEND:
1. Product listing with filters
2. Product details page
3. Shopping cart
4. Checkout flow
5. Order history
6. Admin panel

DEVOPS:
1. Scalable Docker setup
2. Database replication
3. CDN for static files
4. Monitoring & alerting
"""
```

### Пример: SaaS Application

```python
requirements="""
BACKEND:
1. Multi-tenant architecture
2. User management & roles
3. Billing & subscriptions
4. API rate limiting
5. Webhook system
6. Advanced analytics

FRONTEND:
1. Multi-workspace support
2. Settings & billing page
3. Real-time collaboration
4. Advanced UI components
5. Mobile responsive

DEVOPS:
1. Auto-scaling
2. Database failover
3. Backup strategy
4. Security monitoring
5. Performance optimization
"""
```

---

## 📊 Что будет сгенерировано

### Backend (Python + FastAPI)

```
✅ API Endpoints (~30+ строк на endpoint)
   - Full type hints
   - Input validation (Pydantic)
   - Error handling
   - Docstrings

✅ Database Models (SQLAlchemy 2.0)
   - Relationships
   - Indexes
   - Validators

✅ Services (Business Logic)
   - Clean architecture
   - Async/await
   - Error handling

✅ Tests (pytest)
   - Unit tests
   - Integration tests
   - ~80%+ coverage

✅ Migrations (Alembic)
   - Forward & downgrade
   - Data transformations
```

### Frontend (React + TypeScript)

```
✅ Components
   - Reusable & modular
   - Full TypeScript
   - TailwindCSS styled
   - Accessible (a11y)

✅ Pages
   - Responsive design
   - Mobile-first
   - Loading states
   - Error handling

✅ State Management (Zustand)
   - Type-safe
   - DevTools integration
   - Persist middleware

✅ Tests (Jest + RTL)
   - Component tests
   - Integration tests
   - User interaction tests

✅ API Client
   - Type-safe requests
   - Error handling
   - Retry logic
```

### DevOps

```
✅ Dockerfile
   - Multi-stage build
   - Security hardening
   - Optimized size

✅ docker-compose.yml
   - All services
   - Development setup
   - Health checks

✅ GitHub Actions
   - Automated testing
   - Code quality checks
   - Auto-deployment

✅ Deployment Script
   - Database migrations
   - Health verification
   - Rollback capability

✅ Monitoring
   - Prometheus metrics
   - Grafana dashboards
   - Alert rules
```

### Documentation

```
✅ README.md
   - Project overview
   - Installation
   - Quick start

✅ API.md
   - All endpoints
   - Request/response examples
   - Error codes

✅ SETUP.md
   - Local development
   - Database setup
   - Common issues

✅ ARCHITECTURE.md
   - System design
   - Component relationships
   - Technology choices
```

---

## 🔄 Workflow для разных сценариев

### Сценарий 1: Создать новый проект с нуля (1-2 недели → 1-2 дня)

```python
# 1. Определить требования
# 2. Создать ProjectConfig
# 3. Запустить main.py
# 4. Получить готовый код за 1-2 часа
# 5. Кастомизировать под свои нужды
# 6. Deploy в production
```

### Сценарий 2: Добавить функцию в существующий проект (1-3 дня → 1-2 часа)

```python
# Вместо того чтобы вручную писать:
# - API endpoint
# - DB model
# - Tests
# - Frontend component
# - Documentation

# Просто запустите агент для новой фичи!
```

### Сценарий 3: Обучение и прототипирование

```python
# Увидеть production-ready code для:
# - Нового фреймворка
# - Нового паттерна
# - Новой архитектуры

# Как шаблон и ориентир
```

---

## ⚙️ Настройка параметров

### Изменить tech stack

```python
tech_stack={
    "backend": "Node.js + NestJS",      # Вместо FastAPI
    "frontend": "Vue.js + Vite",        # Вместо React
    "database": "MongoDB",              # Вместо PostgreSQL
    "devops": "Docker + GitLab CI"      # Вместо GitHub Actions
}
```

### Изменить длительность спринта

```python
sprint = await pm.plan_sprint("Sprint", duration_days=14)  # 2 недели
sprint = await pm.plan_sprint("Sprint", duration_days=3)   # 3 дня
```

### Запустить несколько спринтов

```python
sprint1 = await pm.plan_sprint("Sprint 1: Backend", duration_days=5)
await pm.execute_sprint(sprint1)

sprint2 = await pm.plan_sprint("Sprint 2: Frontend", duration_days=5)
await pm.execute_sprint(sprint2)

sprint3 = await pm.plan_sprint("Sprint 3: DevOps", duration_days=3)
await pm.execute_sprint(sprint3)
```

---

## 📞 Помощь & Troubleshooting

### Error: "API key not found"

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py
```

### Error: "Rate limit exceeded"

Уменьшите размер проекта или добавьте:

```python
import time
# Добавить задержку между спринтами
await pm.execute_sprint(sprint1)
time.sleep(60)  # 1 минута задержки
await pm.execute_sprint(sprint2)
```

### Код генерируется очень медленно

Это нормально! Claude думает перед написанием. Может занять:
- Простой API: 5-10 минут
- Полный стек: 15-30 минут
- Enterprise система: 30+ минут

Используйте это время для:
- ☕ Кофе
- 📖 Чтения документации
- 📝 Написания бизнес-логики которую AI не может сделать

---

## 🎓 Примеры из боевого использования

### Реальный пример: Создание Todo App

```python
# Время которое обычно берет:
# - Backend разработка: 2-3 дня
# - Frontend разработка: 2-3 дня
# - Testing: 1 день
# - DevOps: 1 день
# ИТОГО: 6-8 дней работы разработчика

# С AI Development Team:
# - Вся разработка: 30-60 минут
# - Ревью и кастомизация: 1-2 часа
# ИТОГО: 2-3 часа с AI помощью
```

---

## 🚀 Следующие шаги

1. **Использовать сгенерированный код** как основу
2. **Кастомизировать** специфичную бизнес-логику
3. **Добавить интеграции** (payment, email, SMS и т.д.)
4. **Развернуть в production** с уверенностью
5. **Поддерживать и развивать** используя generated structure

---

## 💡 Pro Tips

✅ **Будьте специфичны в requirements** - чем детальнее, тем лучше код

✅ **Запустите несколько спринтов** - фаза 1 backend → фаза 2 frontend → фаза 3 devops

✅ **Используйте для learning** - отличный способ выучить новый стек

✅ **Customize после генерации** - AI создает базу, вы добавляете бизнес-логику

✅ **Сохраняйте .env файлы** - не коммитьте в git!

---

**Готовы создать свой первый сервис? Let's go! 🚀**

```bash
python main.py
# Релаксируйте пока AI разработчики работают 😎
```
