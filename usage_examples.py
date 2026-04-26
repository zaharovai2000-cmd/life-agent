"""
Примеры использования системы AI разработчиков

Демонстрирует как использовать PM Agent с Backend, Frontend и DevOps агентами
для разработки полного сервиса с кодом, тестами и deployment конфигами.
"""

import asyncio
from ai_dev_team_starter import (
    PMAgent, ProjectConfig, Task, Sprint
)

# ============================================================================
# ПРИМЕР 1: Создание простого API сервиса
# ============================================================================

async def example_1_simple_api():
    """Создать простой API сервис с authentication"""
    
    print("\n" + "="*60)
    print("ПРИМЕР 1: Создание простого API сервиса")
    print("="*60)
    
    config = ProjectConfig(
        name="Todo API",
        description="Простое REST API для управления TODO списками",
        root_path="./todo_api",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL"
        },
        requirements="""
        Создать TODO API сервис с:
        1. Endpoints для создания, обновления, удаления TODO
        2. User authentication (JWT)
        3. Sharing TODO between users
        4. Categories/Tags для TODO
        5. API documentation (Swagger)
        """
    )
    
    pm = PMAgent(config)
    
    # Спланировать спринт
    sprint = await pm.plan_sprint("Sprint 1: MVP", duration_days=3)
    
    # Выполнить спринт
    results = await pm.execute_sprint(sprint)
    
    # Показать отчет
    report = pm.get_sprint_report()
    print("\n✅ Спринт завершен!")
    print(f"   Завершено задач: {report['tasks']['completed']}/{report['tasks']['total']}")
    print(f"   Сгенерировано файлов: {report['generated_files']}")
    
    return results


# ============================================================================
# ПРИМЕР 2: Создание полного стека (Backend + Frontend + DevOps)
# ============================================================================

async def example_2_full_stack():
    """Создать полный стек приложения"""
    
    print("\n" + "="*60)
    print("ПРИМЕР 2: Полный стек приложения")
    print("="*60)
    
    config = ProjectConfig(
        name="Expense Tracker",
        description="Приложение для отслеживания расходов с аналитикой",
        root_path="./expense_tracker",
        tech_stack={
            "backend": "Python + FastAPI + PostgreSQL",
            "frontend": "React + TypeScript + TailwindCSS",
            "devops": "Docker + GitHub Actions + AWS"
        },
        requirements="""
        Создать Expense Tracker приложение:
        
        BACKEND:
        1. User authentication (JWT)
        2. API для добавления расходов
        3. Categories management
        4. Expense filtering и search
        5. Monthly reports API
        6. Budget tracking
        
        FRONTEND:
        1. Login/Register страницы
        2. Dashboard с статистикой
        3. Add expense форма
        4. Expense список с фильтрацией
        5. Reports page с графиками
        6. Settings страница
        
        DEVOPS:
        1. Dockerfile для backend и frontend
        2. docker-compose для development
        3. GitHub Actions CI/CD pipeline
        4. Deployment скрипт в AWS
        5. Monitoring setup
        """
    )
    
    pm = PMAgent(config)
    
    # Спринт 1: Backend
    print("\n📋 Спринт 1: Backend разработка")
    sprint1 = await pm.plan_sprint("Sprint 1: Backend API", duration_days=5)
    results1 = await pm.execute_sprint(sprint1)
    
    # Спринт 2: Frontend
    print("\n📋 Спринт 2: Frontend разработка")
    sprint2 = await pm.plan_sprint("Sprint 2: Frontend UI", duration_days=5)
    results2 = await pm.execute_sprint(sprint2)
    
    # Спринт 3: DevOps
    print("\n📋 Спринт 3: DevOps и deployment")
    sprint3 = await pm.plan_sprint("Sprint 3: DevOps & Deployment", duration_days=3)
    results3 = await pm.execute_sprint(sprint3)
    
    # Финальный отчет
    final_report = pm.get_sprint_report()
    print("\n" + "="*60)
    print("✅ ВСЕ СПРИНТЫ ЗАВЕРШЕНЫ")
    print("="*60)
    print(f"Всего файлов создано: {final_report['generated_files']}")


# ============================================================================
# ПРИМЕР 3: Разработка с итеративными спринтами
# ============================================================================

async def example_3_iterative_development():
    """Итеративная разработка с несколькими спринтами"""
    
    print("\n" + "="*60)
    print("ПРИМЕР 3: Итеративная разработка (Agile)")
    print("="*60)
    
    config = ProjectConfig(
        name="Social Network MVP",
        description="MVP социальной сети с постами и комментариями",
        root_path="./social_network",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL"
        },
        requirements="""
        Sprint 1: User Management
        - User registration и authentication
        - Profile creation
        - User search
        
        Sprint 2: Posts
        - Create/Read/Update/Delete posts
        - Post listing with pagination
        - Like posts
        
        Sprint 3: Comments & Interactions
        - Comments on posts
        - Reply to comments
        - Notifications
        
        Sprint 4: Frontend
        - Home feed
        - Post creation page
        - User profiles
        - Search page
        
        Sprint 5: DevOps
        - Docker setup
        - CI/CD pipeline
        - Monitoring
        """
    )
    
    pm = PMAgent(config)
    
    sprints_config = [
        ("Sprint 1: User Management", 4),
        ("Sprint 2: Posts", 4),
        ("Sprint 3: Comments", 3),
        ("Sprint 4: Frontend", 5),
        ("Sprint 5: DevOps", 3)
    ]
    
    all_results = []
    
    for sprint_name, duration in sprints_config:
        print(f"\n🚀 Выполнение: {sprint_name}")
        
        sprint = await pm.plan_sprint(sprint_name, duration_days=duration)
        results = await pm.execute_sprint(sprint)
        
        all_results.append(results)
        
        # Показать промежуточный отчет
        report = pm.get_sprint_report()
        print(f"   ✅ {report['tasks']['completed']} задач завершено")
    
    print("\n" + "="*60)
    print("✅ ИТЕРАТИВНАЯ РАЗРАБОТКА ЗАВЕРШЕНА")
    print("="*60)
    print(f"Всего спринтов: {len(all_results)}")
    print(f"Всего задач: {sum(r.get('tasks', {}).get('total', 0) for r in all_results)}")


# ============================================================================
# ПРИМЕР 4: Специфичная задача для одного агента
# ============================================================================

async def example_4_single_agent_task():
    """Выполнить специфичную задачу для одного агента"""
    
    print("\n" + "="*60)
    print("ПРИМЕР 4: Задача для отдельного агента")
    print("="*60)
    
    config = ProjectConfig(
        name="Feature Development",
        description="Разработка конкретной функции",
        root_path="./feature_dev",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL"
        },
        requirements="Нужно развить конкретную фичу в существующем проекте"
    )
    
    pm = PMAgent(config)
    
    # Создать одну специфичную задачу
    task = Task(
        id="feature_payment_integration",
        title="API Endpoint: Payment Processing",
        description="""
        Создать endpoint для обработки платежей через Stripe:
        - POST /api/v1/payments/process
        - Поддержка разных методов оплаты
        - Webhook для подтверждения платежа
        - Error handling и retry logic
        - Логирование транзакций
        """,
        agent="backend",
        priority="high",
        estimated_hours=8.0
    )
    
    # Выполнить задачу
    result = await pm.backend_agent.execute_task(task)
    
    print("\n✅ Задача завершена!")
    print(f"   Файлы: {task.files_generated}")
    print(f"   Тип: {result.get('type')}")


# ============================================================================
# ПРИМЕР 5: Обновление существующего проекта
# ============================================================================

async def example_5_existing_project_update():
    """Обновление существующего проекта"""
    
    print("\n" + "="*60)
    print("ПРИМЕР 5: Обновление существующего проекта")
    print("="*60)
    
    config = ProjectConfig(
        name="Existing Project Update",
        description="Добавление новых фич в существующий проект",
        root_path="./existing_project",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL"
        },
        requirements="""
        Добавить в существующий проект:
        1. Email notifications feature
        2. Two-factor authentication
        3. Advanced search with filters
        4. Performance optimizations
        5. Mobile-responsive improvements
        """
    )
    
    pm = PMAgent(config)
    
    # Спланировать update sprint
    sprint = await pm.plan_sprint("Sprint: New Features", duration_days=7)
    results = await pm.execute_sprint(sprint)
    
    print("\n✅ Обновление завершено!")


# ============================================================================
# ПРИМЕР 6: Чистая разработка сервиса с нуля (Full Real World)
# ============================================================================

async def example_6_full_real_world_service():
    """Разработка реального сервиса с нуля"""
    
    print("\n" + "="*60)
    print("ПРИМЕР 6: ПОЛНАЯ РАЗРАБОТКА РЕАЛЬНОГО СЕРВИСА")
    print("="*60)
    
    config = ProjectConfig(
        name="AI Personal Assistant Service",
        description="Полнофункциональный сервис личного AI ассистента",
        root_path="./ai_assistant",
        tech_stack={
            "backend": "Python + FastAPI + PostgreSQL",
            "frontend": "React + TypeScript + TailwindCSS",
            "devops": "Docker + GitHub Actions + Kubernetes"
        },
        requirements="""
        ПОЛНАЯ РАЗРАБОТКА СЕРВИСА:
        
        === BACKEND ===
        1. User Management
           - Registration, Login, Profile
           - JWT authentication
           - Password reset
        
        2. Chat API
           - Message endpoints
           - Conversation management
           - File upload support
        
        3. AI Integration
           - Claude API integration
           - Agent routing
           - Streaming responses
        
        4. Database
           - User models
           - Chat history
           - File storage
        
        5. Security
           - Rate limiting
           - CORS
           - Input validation
           - SQL injection prevention
        
        6. Tests
           - Unit tests for all endpoints
           - Integration tests
           - 80%+ coverage
        
        === FRONTEND ===
        1. Authentication Pages
           - Login page
           - Registration page
           - Password reset page
        
        2. Main App
           - Chat interface
           - Message history
           - File upload
           - Agent selector
           - Settings page
        
        3. Responsive Design
           - Mobile support
           - Tablet support
           - Desktop optimized
        
        4. State Management
           - Auth store
           - Chat store
           - User store
        
        5. API Integration
           - API service client
           - Error handling
           - Loading states
        
        6. Tests
           - Component tests
           - Integration tests
           - E2E tests
        
        === DEVOPS ===
        1. Containerization
           - Dockerfile для backend
           - Dockerfile для frontend
           - docker-compose для dev
        
        2. CI/CD
           - GitHub Actions workflow
           - Automated tests
           - Build & push images
        
        3. Deployment
           - AWS/DigitalOcean setup
           - Database migrations
           - Health checks
        
        4. Monitoring
           - Prometheus metrics
           - Grafana dashboards
           - Alert rules
           - Log aggregation
        
        5. Documentation
           - API docs (Swagger)
           - Setup guide
           - Architecture docs
           - Deployment guide
        """
    )
    
    pm = PMAgent(config)
    
    # ===== ФАЗА 1: SETUP И АРХИТЕКТУРА =====
    print("\n🎯 ФАЗА 1: SETUP И АРХИТЕКТУРА (1-2 дня)")
    
    sprint1_tasks = [
        Task(
            id="setup_project",
            title="Project Setup & Structure",
            description="Создать структуру проекта, конфиги, dependencies",
            agent="devops",
            priority="high",
            estimated_hours=4.0
        ),
        Task(
            id="db_schema",
            title="Database Schema Design",
            description="Спроектировать и создать БД схему для всех сущностей",
            agent="backend",
            priority="high",
            estimated_hours=6.0
        )
    ]
    
    for task in sprint1_tasks:
        result = await pm.backend_agent.execute_task(task) if task.agent == "backend" else await pm.devops_agent.execute_task(task)
        print(f"✅ {task.title}")
    
    # ===== ФАЗА 2: BACKEND РАЗРАБОТКА =====
    print("\n🎯 ФАЗА 2: BACKEND РАЗРАБОТКА (3-4 дня)")
    
    sprint2 = await pm.plan_sprint("Sprint: Backend Core", duration_days=4)
    results2 = await pm.execute_sprint(sprint2)
    
    # ===== ФАЗА 3: FRONTEND РАЗРАБОТКА =====
    print("\n🎯 ФАЗА 3: FRONTEND РАЗРАБОТКА (3-4 дня)")
    
    sprint3 = await pm.plan_sprint("Sprint: Frontend UI", duration_days=4)
    results3 = await pm.execute_sprint(sprint3)
    
    # ===== ФАЗА 4: DEVOPS И DEPLOYMENT =====
    print("\n🎯 ФАЗА 4: DEVOPS И DEPLOYMENT (2-3 дня)")
    
    sprint4 = await pm.plan_sprint("Sprint: DevOps & Deployment", duration_days=3)
    results4 = await pm.execute_sprint(sprint4)
    
    # ===== ФИНАЛЬНЫЙ ОТЧЕТ =====
    final_report = pm.get_sprint_report()
    
    print("\n" + "="*60)
    print("✅ 🚀 СЕРВИС ПОЛНОСТЬЮ РАЗРАБОТАН И ГОТОВ К DEPLOYMENT")
    print("="*60)
    print(f"""
    📊 СТАТИСТИКА:
    - Всего спринтов: 4
    - Всего задач завершено: {final_report['tasks']['completed']}
    - Всего файлов создано: {final_report['generated_files']}
    
    📁 АРТЕФАКТЫ:
    - Backend код с API endpoints, моделями, сервисами
    - Backend тесты (unit + integration)
    - Frontend компоненты, страницы, stores
    - Frontend тесты (component + integration)
    - Docker конфигурация
    - GitHub Actions CI/CD pipeline
    - Deployment скрипты
    - Kubernetes manifests
    - Monitoring конфигурация
    - Полная документация (README, API Docs, Architecture)
    
    🚀 СЛЕДУЮЩИЕ ШАГИ:
    1. cd ai_assistant
    2. docker-compose up -d
    3. Перейти на http://localhost:3000
    4. Использовать API на http://localhost:8000/docs
    """)


# ============================================================================
# MAIN - RUN EXAMPLES
# ============================================================================

async def main():
    """Запустить примеры"""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║         ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ AI DEVELOPMENT TEAM                  ║
    ║                                                                    ║
    ║  Система использует Claude AI для разработки полного сервиса      ║
    ║  с Backend, Frontend и DevOps агентами, работающими параллельно   ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Раскомментируйте пример который хотите запустить
    
    # await example_1_simple_api()
    # await example_2_full_stack()
    # await example_3_iterative_development()
    # await example_4_single_agent_task()
    # await example_5_existing_project_update()
    
    # ПОЛНАЯ РАЗРАБОТКА РЕАЛЬНОГО СЕРВИСА
    await example_6_full_real_world_service()


if __name__ == "__main__":
    asyncio.run(main())
