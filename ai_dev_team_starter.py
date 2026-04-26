"""
AI Development Team - Система разработчиков на основе Claude AI

Система состоит из:
- PM Agent (управление проектом)
- Backend Agent (API, БД, логика)
- Frontend Agent (UI, компоненты, state)
- DevOps Agent (Docker, CI/CD, monitoring)

Все агенты работают параллельно под координацией PM Agent
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from anthropic import Anthropic

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Task:
    """Модель задачи"""
    id: str
    title: str
    description: str
    agent: str  # backend, frontend, devops
    status: str  # pending, in_progress, review, completed
    priority: str  # low, medium, high
    estimated_hours: float
    actual_hours: float = 0.0
    subtasks: List[str] = None
    files_generated: List[str] = None
    created_at: str = None
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.subtasks is None:
            self.subtasks = []
        if self.files_generated is None:
            self.files_generated = []

@dataclass
class Sprint:
    """Модель спринта"""
    id: str
    name: str
    duration_days: int
    status: str  # planning, in_progress, review, completed
    tasks: List[Task]
    start_date: str
    end_date: Optional[str] = None
    metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {
                "completed_tasks": 0,
                "total_tasks": len(self.tasks),
                "code_lines_written": 0,
                "test_coverage": 0.0,
                "bugs_found": 0,
                "deployment_success": False
            }

@dataclass
class ProjectConfig:
    """Конфигурация проекта"""
    name: str
    description: str
    root_path: str
    tech_stack: Dict[str, str]
    requirements: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class BaseAgent:
    """Базовый класс для всех агентов"""
    
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        self.generated_files = []
        self.task_queue = []
        self.completed_tasks = []
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Выполнить задачу"""
        task.status = "in_progress"
        print(f"\n[{self.name}] 🔄 Выполняю: {task.title}")
        
        # Реальный запрос к Claude
        result = await self._process_task(task)
        
        task.status = "completed"
        task.completed_at = datetime.now().isoformat()
        self.completed_tasks.append(task)
        
        print(f"[{self.name}] ✅ Завершено: {task.title}")
        return result
    
    async def _process_task(self, task: Task) -> Dict[str, Any]:
        """Обработать задачу (переопределяется в подклассах)"""
        raise NotImplementedError
    
    async def _call_claude(self, user_message: str, context: Optional[str] = None) -> str:
        """Вызвать Claude API"""
        
        # Добавить контекст в сообщение если есть
        if context:
            user_message = f"{context}\n\n{user_message}"
        
        # Добавить в историю
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Вызвать API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        # Получить ответ
        assistant_message = response.content[0].text
        
        # Добавить в историю
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    async def save_file(self, file_path: str, content: str) -> str:
        """Сохранить файл"""
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.generated_files.append(file_path)
        return file_path
    
    def get_status(self) -> Dict[str, Any]:
        """Получить статус агента"""
        return {
            "name": self.name,
            "role": self.role,
            "completed_tasks": len(self.completed_tasks),
            "generated_files": len(self.generated_files),
            "files": self.generated_files
        }

# ============================================================================
# BACKEND AGENT
# ============================================================================

class BackendAgent(BaseAgent):
    """Backend Developer Agent - разработка API и бизнес-логики"""
    
    SYSTEM_PROMPT = """Ты Senior Backend Developer с опытом в Python, FastAPI, PostgreSQL.

Твои обязанности:
1. Проектирование и реализация REST API endpoints
2. Создание database моделей и миграций
3. Реализация бизнес-логики и сервисов
4. Написание unit и интеграционных тестов
5. Обеспечение безопасности и производительности

При написании кода:
- Используй FastAPI с type hints
- Используй SQLAlchemy ORM
- Добавляй docstrings и комментарии
- Следуй best practices Python
- Пиши асинхронный код (async/await)
- Включай error handling

При написании тестов:
- Используй pytest
- Пиши unit и integration тесты
- Тестируй edge cases
- Целевой coverage 80%+"""
    
    def __init__(self):
        super().__init__(
            name="BackendAgent",
            role="Backend Developer",
            system_prompt=self.SYSTEM_PROMPT
        )
    
    async def _process_task(self, task: Task) -> Dict[str, Any]:
        """Обработать backend задачу"""
        
        if "API endpoint" in task.title:
            return await self.implement_endpoint(task)
        elif "database" in task.title.lower():
            return await self.implement_database_model(task)
        elif "service" in task.title.lower():
            return await self.implement_service(task)
        elif "test" in task.title.lower():
            return await self.write_tests(task)
        else:
            return await self.implement_generic(task)
    
    async def implement_endpoint(self, task: Task) -> Dict[str, Any]:
        """Реализовать API endpoint"""
        
        prompt = f"""Напиши полный FastAPI endpoint для: {task.description}

Требования:
1. Правильные HTTP методы и пути
2. Pydantic schemas для request/response
3. Input validation
4. Error handling с правильными status codes
5. Docstring
6. Type hints

Код должен быть production-ready."""
        
        code = await self._call_claude(prompt)
        
        # Сохранить код
        file_path = f"src/api/endpoints/{task.id}.py"
        await self.save_file(file_path, code)
        task.files_generated.append(file_path)
        
        return {
            "task_id": task.id,
            "type": "api_endpoint",
            "code": code,
            "file": file_path,
            "status": "completed"
        }
    
    async def implement_database_model(self, task: Task) -> Dict[str, Any]:
        """Реализовать database модель"""
        
        prompt = f"""Напиши SQLAlchemy ORM модель для: {task.description}

Требования:
1. Используй SQLAlchemy 2.0
2. Определи все поля с правильными типами
3. Добавь relationships если нужны
4. Добавь indexes для часто используемых полей
5. Добавь validators
6. Добавь __repr__ метод

Также напиши Alembic миграцию для создания таблицы."""
        
        result = await self._call_claude(prompt)
        
        # Сохранить модель
        model_file = f"src/models/{task.id}.py"
        await self.save_file(model_file, result)
        task.files_generated.append(model_file)
        
        return {
            "task_id": task.id,
            "type": "database_model",
            "code": result,
            "file": model_file,
            "status": "completed"
        }
    
    async def implement_service(self, task: Task) -> Dict[str, Any]:
        """Реализовать бизнес-логику сервис"""
        
        prompt = f"""Напиши Python сервис с бизнес-логикой для: {task.description}

Требования:
1. Clean architecture с методами для каждой операции
2. Async/await поддержка
3. Dependency injection паттерн
4. Логирование
5. Error handling
6. Type hints
7. Docstrings

Сервис должен быть переиспользуемым в endpoints."""
        
        code = await self._call_claude(prompt)
        
        # Сохранить сервис
        service_file = f"src/services/{task.id}_service.py"
        await self.save_file(service_file, code)
        task.files_generated.append(service_file)
        
        return {
            "task_id": task.id,
            "type": "service",
            "code": code,
            "file": service_file,
            "status": "completed"
        }
    
    async def write_tests(self, task: Task) -> Dict[str, Any]:
        """Написать тесты"""
        
        prompt = f"""Напиши comprehensive pytest тесты для: {task.description}

Требования:
1. Unit тесты для каждой функции
2. Integration тесты если нужны
3. Тесты для edge cases и error scenarios
4. Fixtures для setup/teardown
5. Mocks для dependencies
6. Целевой coverage 80%+

Используй pytest и pytest-asyncio."""
        
        test_code = await self._call_claude(prompt)
        
        # Сохранить тесты
        test_file = f"tests/test_{task.id}.py"
        await self.save_file(test_file, test_code)
        task.files_generated.append(test_file)
        
        return {
            "task_id": task.id,
            "type": "tests",
            "code": test_code,
            "file": test_file,
            "status": "completed"
        }
    
    async def implement_generic(self, task: Task) -> Dict[str, Any]:
        """Реализовать генерический backend компонент"""
        
        prompt = f"""Реализуй для backend: {task.title}

Описание: {task.description}

Требования:
1. Production-ready код
2. Proper error handling
3. Type hints
4. Docstrings
5. Tests если applicable"""
        
        code = await self._call_claude(prompt)
        
        file_path = f"src/utils/{task.id}.py"
        await self.save_file(file_path, code)
        task.files_generated.append(file_path)
        
        return {
            "task_id": task.id,
            "type": "generic",
            "code": code,
            "file": file_path,
            "status": "completed"
        }

# ============================================================================
# FRONTEND AGENT
# ============================================================================

class FrontendAgent(BaseAgent):
    """Frontend Developer Agent - разработка UI и компонентов"""
    
    SYSTEM_PROMPT = """Ты Senior Frontend Developer с опытом в React, TypeScript, TailwindCSS.

Твои обязанности:
1. Создание React компонентов на TypeScript
2. Разработка страниц с responsive design
3. State management с Zustand
4. API интеграция
5. UI/UX реализация

При написании кода:
- Используй TypeScript с full type hints
- Используй React Hooks (useState, useEffect, useContext и т.д.)
- Используй TailwindCSS для стилей
- Пиши reusable компоненты
- Добавляй JSDoc комментарии
- Делай accessibility (a11y)

При написании тестов:
- Используй Jest + React Testing Library
- Тестируй rendering, interactions, state changes
- Mock API calls"""
    
    def __init__(self):
        super().__init__(
            name="FrontendAgent",
            role="Frontend Developer",
            system_prompt=self.SYSTEM_PROMPT
        )
    
    async def _process_task(self, task: Task) -> Dict[str, Any]:
        """Обработать frontend задачу"""
        
        if "component" in task.title.lower():
            return await self.create_component(task)
        elif "page" in task.title.lower():
            return await self.create_page(task)
        elif "service" in task.title.lower():
            return await self.create_api_service(task)
        elif "store" in task.title.lower() or "state" in task.title.lower():
            return await self.create_store(task)
        elif "test" in task.title.lower():
            return await self.write_tests(task)
        else:
            return await self.create_generic(task)
    
    async def create_component(self, task: Task) -> Dict[str, Any]:
        """Создать React компонент"""
        
        prompt = f"""Создай React компонент на TypeScript: {task.title}

Описание: {task.description}

Требования:
1. Functional component с Hooks
2. Full TypeScript types для props
3. TailwindCSS для стилей
4. JSDoc комментарии
5. Reusable и модульный
6. Accessible (ARIA labels)
7. Props для кастомизации

Компонент должен быть production-ready."""
        
        code = await self._call_claude(prompt)
        
        # Сохранить компонент
        component_file = f"src/components/{task.id}.tsx"
        await self.save_file(component_file, code)
        task.files_generated.append(component_file)
        
        return {
            "task_id": task.id,
            "type": "react_component",
            "code": code,
            "file": component_file,
            "status": "completed"
        }
    
    async def create_page(self, task: Task) -> Dict[str, Any]:
        """Создать страницу"""
        
        prompt = f"""Создай React страницу на TypeScript: {task.title}

Маршрут: {task.description}

Требования:
1. Полная page layout
2. Responsive design для mobile/tablet/desktop
3. Использование компонентов
4. Loading и error states
5. Data fetching если нужно
6. State management
7. Proper TypeScript types

Страница должна быть готова к production."""
        
        code = await self._call_claude(prompt)
        
        # Сохранить страницу
        page_file = f"src/pages/{task.id}.tsx"
        await self.save_file(page_file, code)
        task.files_generated.append(page_file)
        
        return {
            "task_id": task.id,
            "type": "page",
            "code": code,
            "file": page_file,
            "status": "completed"
        }
    
    async def create_api_service(self, task: Task) -> Dict[str, Any]:
        """Создать API service для backend интеграции"""
        
        prompt = f"""Создай TypeScript API service: {task.title}

Описание: {task.description}

Требования:
1. Используй axios или fetch
2. Полные TypeScript types для requests/responses
3. Error handling
4. Retry logic
5. Timeout handling
6. Request/response interceptors
7. Type-safe методы

Service должен быть легко переиспользуемым."""
        
        code = await self._call_claude(prompt)
        
        # Сохранить сервис
        service_file = f"src/services/{task.id}.ts"
        await self.save_file(service_file, code)
        task.files_generated.append(service_file)
        
        return {
            "task_id": task.id,
            "type": "api_service",
            "code": code,
            "file": service_file,
            "status": "completed"
        }
    
    async def create_store(self, task: Task) -> Dict[str, Any]:
        """Создать Zustand store для state management"""
        
        prompt = f"""Создай Zustand store: {task.title}

Описание: {task.description}

Требования:
1. Используй Zustand
2. Full TypeScript types
3. State definition
4. Actions (setters)
5. Selectors для оптимизации
6. DevTools integration
7. Persist middleware если нужна

Store должен быть type-safe и performant."""
        
        code = await self._call_claude(prompt)
        
        # Сохранить store
        store_file = f"src/stores/{task.id}.ts"
        await self.save_file(store_file, code)
        task.files_generated.append(store_file)
        
        return {
            "task_id": task.id,
            "type": "store",
            "code": code,
            "file": store_file,
            "status": "completed"
        }
    
    async def write_tests(self, task: Task) -> Dict[str, Any]:
        """Написать тесты для React компонентов"""
        
        prompt = f"""Напиши Jest + React Testing Library тесты для: {task.title}

Требования:
1. Тесты для rendering
2. Тесты для user interactions
3. Тесты для state changes
4. Mock API calls
5. Tests для props
6. Edge cases

Используй best practices для React testing."""
        
        test_code = await self._call_claude(prompt)
        
        # Сохранить тесты
        test_file = f"tests/{task.id}.test.tsx"
        await self.save_file(test_file, test_code)
        task.files_generated.append(test_file)
        
        return {
            "task_id": task.id,
            "type": "tests",
            "code": test_code,
            "file": test_file,
            "status": "completed"
        }
    
    async def create_generic(self, task: Task) -> Dict[str, Any]:
        """Создать генерический frontend компонент"""
        
        prompt = f"""Реализуй для frontend: {task.title}

Описание: {task.description}

Требования:
1. TypeScript с полными types
2. React best practices
3. TailwindCSS стили
4. Reusable компоненты
5. Proper структура"""
        
        code = await self._call_claude(prompt)
        
        file_path = f"src/utils/{task.id}.ts"
        await self.save_file(file_path, code)
        task.files_generated.append(file_path)
        
        return {
            "task_id": task.id,
            "type": "generic",
            "code": code,
            "file": file_path,
            "status": "completed"
        }

# ============================================================================
# DEVOPS AGENT
# ============================================================================

class DevOpsAgent(BaseAgent):
    """DevOps Engineer Agent - инфраструктура и deployment"""
    
    SYSTEM_PROMPT = """Ты опытный DevOps Engineer с знаниями Docker, Kubernetes, CI/CD, AWS.

Твои обязанности:
1. Создание Dockerfile и docker-compose конфигов
2. GitHub Actions CI/CD pipelines
3. Kubernetes manifests
4. Deployment scripts
5. Monitoring и logging setup
6. Infrastructure as Code

При написании конфигов:
- Следуй best practices безопасности
- Оптимизируй размеры образов
- Используй multi-stage builds
- Правильный error handling
- Health checks
- Логирование

При создании CI/CD:
- Автоматическое тестирование
- Code quality checks
- Build и push образов
- Deploy в разные окружения
- Rollback capability"""
    
    def __init__(self):
        super().__init__(
            name="DevOpsAgent",
            role="DevOps Engineer",
            system_prompt=self.SYSTEM_PROMPT
        )
    
    async def _process_task(self, task: Task) -> Dict[str, Any]:
        """Обработать devops задачу"""
        
        if "dockerfile" in task.title.lower():
            return await self.create_dockerfile(task)
        elif "docker-compose" in task.title.lower():
            return await self.create_docker_compose(task)
        elif "github actions" in task.title.lower() or "ci/cd" in task.title.lower():
            return await self.create_github_actions(task)
        elif "deployment" in task.title.lower() or "deploy" in task.title.lower():
            return await self.create_deployment_script(task)
        elif "monitoring" in task.title.lower():
            return await self.setup_monitoring(task)
        elif "kubernetes" in task.title.lower() or "k8s" in task.title.lower():
            return await self.create_kubernetes_manifests(task)
        else:
            return await self.create_generic_infra(task)
    
    async def create_dockerfile(self, task: Task) -> Dict[str, Any]:
        """Создать оптимизированный Dockerfile"""
        
        prompt = f"""Напиши оптимизированный Dockerfile: {task.title}

Описание: {task.description}

Требования:
1. Multi-stage build для оптимизации размера
2. Правильный порядок слоев (кэширование)
3. Non-root user для безопасности
4. Health check
5. Правильные права на файлы
6. Минимум layers
7. Комментарии

Dockerfile должен быть production-ready."""
        
        dockerfile = await self._call_claude(prompt)
        
        # Сохранить Dockerfile
        dockerfile_path = "Dockerfile"
        await self.save_file(dockerfile_path, dockerfile)
        task.files_generated.append(dockerfile_path)
        
        return {
            "task_id": task.id,
            "type": "dockerfile",
            "code": dockerfile,
            "file": dockerfile_path,
            "status": "completed"
        }
    
    async def create_docker_compose(self, task: Task) -> Dict[str, Any]:
        """Создать docker-compose.yml для development"""
        
        prompt = f"""Напиши docker-compose.yml: {task.title}

Описание: {task.description}

Требования:
1. Все необходимые сервисы
2. Volume mounts для development
3. Network configuration
4. Environment variables
5. Health checks
6. Proper dependencies
7. Port mappings
8. Комментарии

Файл должен быть готов к использованию."""
        
        compose = await self._call_claude(prompt)
        
        # Сохранить docker-compose
        compose_path = "docker-compose.yml"
        await self.save_file(compose_path, compose)
        task.files_generated.append(compose_path)
        
        return {
            "task_id": task.id,
            "type": "docker_compose",
            "code": compose,
            "file": compose_path,
            "status": "completed"
        }
    
    async def create_github_actions(self, task: Task) -> Dict[str, Any]:
        """Создать GitHub Actions CI/CD workflow"""
        
        prompt = f"""Напиши GitHub Actions workflow (YAML): {task.title}

Описание: {task.description}

Требования:
1. Trigger на push/PR
2. Lint проверки (flake8, eslint)
3. Run tests
4. Code coverage reports
5. Build Docker image
6. Push в registry (if deployment)
7. Deploy (if needed)
8. Notifications на ошибки

Workflow должен быть robust и maintainable."""
        
        workflow = await self._call_claude(prompt)
        
        # Сохранить workflow
        os.makedirs(".github/workflows", exist_ok=True)
        workflow_path = f".github/workflows/{task.id}.yml"
        await self.save_file(workflow_path, workflow)
        task.files_generated.append(workflow_path)
        
        return {
            "task_id": task.id,
            "type": "github_actions",
            "code": workflow,
            "file": workflow_path,
            "status": "completed"
        }
    
    async def create_deployment_script(self, task: Task) -> Dict[str, Any]:
        """Создать deployment скрипт"""
        
        prompt = f"""Напиши Bash deployment скрипт: {task.title}

Описание: {task.description}

Требования:
1. Build Docker images
2. Run migrations если нужны
3. Deploy containers
4. Health checks
5. Verify deployment success
6. Rollback на ошибку
7. Logging
8. Error handling

Скрипт должен быть безопасным и надежным."""
        
        script = await self._call_claude(prompt)
        
        # Сохранить скрипт
        script_path = f"scripts/{task.id}.sh"
        await self.save_file(script_path, script)
        
        # Сделать executable
        os.chmod(script_path, 0o755)
        task.files_generated.append(script_path)
        
        return {
            "task_id": task.id,
            "type": "deployment_script",
            "code": script,
            "file": script_path,
            "status": "completed"
        }
    
    async def setup_monitoring(self, task: Task) -> Dict[str, Any]:
        """Настроить monitoring и logging"""
        
        prompt = f"""Создай конфиги для monitoring: {task.title}

Описание: {task.description}

Требования:
1. Prometheus конфиг для metrics
2. Grafana dashboard (JSON)
3. AlertManager правила
4. ELK stack конфигурация (если нужна)
5. Log aggregation setup
6. Useful metrics для tracking

Конфиги должны быть production-ready."""
        
        monitoring_config = await self._call_claude(prompt)
        
        # Сохранить конфиги
        os.makedirs("infra/monitoring", exist_ok=True)
        config_path = f"infra/monitoring/{task.id}.yaml"
        await self.save_file(config_path, monitoring_config)
        task.files_generated.append(config_path)
        
        return {
            "task_id": task.id,
            "type": "monitoring",
            "code": monitoring_config,
            "file": config_path,
            "status": "completed"
        }
    
    async def create_kubernetes_manifests(self, task: Task) -> Dict[str, Any]:
        """Создать Kubernetes manifests"""
        
        prompt = f"""Напиши Kubernetes manifests: {task.title}

Описание: {task.description}

Требования:
1. Deployment manifests
2. Service definitions
3. Ingress configuration
4. ConfigMaps и Secrets
5. Health probes
6. Resource limits
7. RBAC если нужны
8. Proper labels и annotations

Manifests должны быть в best practices."""
        
        manifests = await self._call_claude(prompt)
        
        # Сохранить manifests
        os.makedirs("infra/k8s", exist_ok=True)
        manifest_path = f"infra/k8s/{task.id}.yaml"
        await self.save_file(manifest_path, manifests)
        task.files_generated.append(manifest_path)
        
        return {
            "task_id": task.id,
            "type": "k8s_manifests",
            "code": manifests,
            "file": manifest_path,
            "status": "completed"
        }
    
    async def create_generic_infra(self, task: Task) -> Dict[str, Any]:
        """Создать генерическую infra конфигурацию"""
        
        prompt = f"""Создай инфраструктурную конфигурацию: {task.title}

Описание: {task.description}

Требования:
1. Production-ready
2. Security best practices
3. High availability considerations
4. Logging и monitoring
5. Proper documentation"""
        
        config = await self._call_claude(prompt)
        
        file_path = f"infra/{task.id}.yaml"
        await self.save_file(file_path, config)
        task.files_generated.append(file_path)
        
        return {
            "task_id": task.id,
            "type": "infra_config",
            "code": config,
            "file": file_path,
            "status": "completed"
        }

# ============================================================================
# PROJECT MANAGER AGENT
# ============================================================================

class PMAgent:
    """Project Manager Agent - управляет разработкой проекта"""
    
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.sprints: List[Sprint] = []
        self.current_sprint: Optional[Sprint] = None
        self.task_queue: List[Task] = []
        
        # Инициализировать команду агентов
        self.backend_agent = BackendAgent()
        self.frontend_agent = FrontendAgent()
        self.devops_agent = DevOpsAgent()
        
        self.team = {
            "backend": self.backend_agent,
            "frontend": self.frontend_agent,
            "devops": self.devops_agent
        }
        
        print(f"\n✅ Проект создан: {config.name}")
        print(f"   📍 Путь: {config.root_path}")
        print(f"   🛠️  Tech Stack: {config.tech_stack}")
    
    async def plan_sprint(
        self,
        sprint_name: str,
        duration_days: int = 14
    ) -> Sprint:
        """Спланировать спринт на основе требований проекта"""
        
        print(f"\n📋 Планирование спринта: {sprint_name}")
        
        # Разбить требования на tasks
        prompt = f"""Разбей эти требования на конкретные задачи для разработки сервиса:

Название: {self.config.name}
Описание: {self.config.description}

Требования:
{self.config.requirements}

Tech Stack:
- Backend: {self.config.tech_stack.get('backend')}
- Frontend: {self.config.tech_stack.get('frontend')}
- DevOps: {self.config.tech_stack.get('devops')}

Разбей на задачи в JSON формате:
[
  {{
    "id": "task_1",
    "title": "название задачи",
    "description": "описание",
    "agent": "backend|frontend|devops",
    "priority": "high|medium|low",
    "estimated_hours": число
  }}
]

Верни ТОЛЬКО JSON массив, без markdown кода блока."""
        
        client = Anthropic()
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        tasks_text = response.content[0].text
        
        # Очистить markdown если есть
        tasks_text = tasks_text.strip()
        if tasks_text.startswith("```"):
            tasks_text = tasks_text.split("```")[1]
            if tasks_text.startswith("json"):
                tasks_text = tasks_text[4:]
        if tasks_text.endswith("```"):
            tasks_text = tasks_text[:-3]
        
        tasks_data = json.loads(tasks_text)
        
        # Создать Task объекты
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                agent=task_data["agent"],
                priority=task_data["priority"],
                estimated_hours=task_data.get("estimated_hours", 8.0)
            )
            tasks.append(task)
        
        # Создать спринт
        sprint = Sprint(
            id=f"sprint_{len(self.sprints) + 1}",
            name=sprint_name,
            duration_days=duration_days,
            status="in_progress",
            tasks=tasks,
            start_date=datetime.now().isoformat()
        )
        
        self.sprints.append(sprint)
        self.current_sprint = sprint
        
        print(f"✅ Спринт создан: {len(tasks)} задач")
        for task in tasks:
            print(f"   - [{task.agent}] {task.title} ({task.estimated_hours}h)")
        
        return sprint
    
    async def execute_sprint(self, sprint: Sprint) -> Dict[str, Any]:
        """Выполнить все задачи в спринте"""
        
        print(f"\n🚀 Выполнение спринта: {sprint.name}")
        print(f"📊 Всего задач: {len(sprint.tasks)}")
        
        results = {
            "sprint_id": sprint.id,
            "sprint_name": sprint.name,
            "tasks": [],
            "agents_output": {},
            "generated_files": {}
        }
        
        # Создать папку проекта
        os.makedirs(self.config.root_path, exist_ok=True)
        os.chdir(self.config.root_path)
        
        # Создать базовую структуру
        await self._create_project_structure()
        
        # Выполнить задачи параллельно по агентам
        # Группировать задачи по агентам
        tasks_by_agent = {}
        for task in sprint.tasks:
            if task.agent not in tasks_by_agent:
                tasks_by_agent[task.agent] = []
            tasks_by_agent[task.agent].append(task)
        
        # Выполнить для каждого агента
        for agent_name, agent_tasks in tasks_by_agent.items():
            print(f"\n👨‍💻 Передаю задачи агенту: {agent_name}")
            
            agent = self.team.get(agent_name)
            if not agent:
                print(f"   ⚠️  Агент {agent_name} не найден")
                continue
            
            agent_results = []
            for task in agent_tasks:
                try:
                    result = await agent.execute_task(task)
                    agent_results.append(result)
                    results["tasks"].append({
                        "task_id": task.id,
                        "title": task.title,
                        "agent": agent_name,
                        "status": "completed",
                        "files": task.files_generated
                    })
                except Exception as e:
                    print(f"   ❌ Ошибка в задаче {task.id}: {str(e)}")
                    results["tasks"].append({
                        "task_id": task.id,
                        "title": task.title,
                        "agent": agent_name,
                        "status": "failed",
                        "error": str(e)
                    })
            
            results["agents_output"][agent_name] = {
                "status": agent.get_status(),
                "tasks_completed": len(agent_results)
            }
            results["generated_files"][agent_name] = agent.generated_files
        
        # Завершить спринт
        sprint.status = "completed"
        sprint.end_date = datetime.now().isoformat()
        sprint.metrics["completed_tasks"] = len([t for t in sprint.tasks if t.status == "completed"])
        
        # Создать финальные файлы (docs, deployment scripts)
        await self._create_final_artifacts()
        
        print(f"\n✅ Спринт завершен!")
        print(f"   📊 Завершено задач: {sprint.metrics['completed_tasks']}/{sprint.metrics['total_tasks']}")
        print(f"   📁 Всего файлов: {len(self._get_all_generated_files())}")
        
        return results
    
    async def _create_project_structure(self):
        """Создать базовую структуру папок проекта"""
        
        structure = {
            "src": {
                "api": {"endpoints": {}},
                "models": {},
                "services": {},
                "utils": {}
            },
            "tests": {},
            "docs": {},
            "infra": {
                "k8s": {},
                "monitoring": {}
            },
            "scripts": {}
        }
        
        def create_dirs(base_path, structure_dict):
            for key, value in structure_dict.items():
                dir_path = os.path.join(base_path, key)
                os.makedirs(dir_path, exist_ok=True)
                
                if isinstance(value, dict):
                    create_dirs(dir_path, value)
                
                # Создать __init__.py для Python папок
                if key in ["src", "models", "services", "utils", "tests"]:
                    init_file = os.path.join(dir_path, "__init__.py")
                    if not os.path.exists(init_file):
                        open(init_file, "w").close()
        
        create_dirs(".", structure)
        print("   ✅ Структура проекта создана")
    
    async def _create_final_artifacts(self):
        """Создать финальные артефакты (README, requirements, т.д.)"""
        
        client = Anthropic()
        
        # Создать README
        readme_prompt = f"""Напиши профессиональный README.md для:

Название: {self.config.name}
Описание: {self.config.description}

Tech Stack:
- Backend: {self.config.tech_stack.get('backend')}
- Frontend: {self.config.tech_stack.get('frontend')}
- Database: {self.config.tech_stack.get('database')}

README должен включать:
1. Project overview
2. Features
3. Tech stack description
4. Installation instructions
5. Quick start guide
6. Project structure
7. Contributing guidelines
8. License"""
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": readme_prompt}]
        )
        
        readme = response.content[0].text
        
        with open("README.md", "w") as f:
            f.write(readme)
        
        # Создать requirements.txt
        requirements = """# Backend Dependencies
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.4.2
pydantic-settings==2.0.3
python-jose==3.3.0
passlib==1.7.4
python-dotenv==1.0.0
httpx==0.25.1
pytest==7.4.3
pytest-asyncio==0.21.1

# Development
flake8==6.1.0
black==23.11.0
isort==5.12.0"""
        
        with open("requirements.txt", "w") as f:
            f.write(requirements)
        
        # Создать .gitignore
        gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Frontend
node_modules/
.next/
out/
dist/
build/

# Database
*.db
*.sqlite
"""
        
        with open(".gitignore", "w") as f:
            f.write(gitignore)
        
        print("   ✅ README и конфигурационные файлы созданы")
    
    def _get_all_generated_files(self) -> List[str]:
        """Получить все сгенерированные файлы"""
        
        all_files = []
        for agent in self.team.values():
            all_files.extend(agent.generated_files)
        return all_files
    
    def get_sprint_report(self) -> Dict[str, Any]:
        """Получить отчет по спринту"""
        
        if not self.current_sprint:
            return {"error": "No active sprint"}
        
        sprint = self.current_sprint
        
        return {
            "sprint_id": sprint.id,
            "sprint_name": sprint.name,
            "status": sprint.status,
            "duration_days": sprint.duration_days,
            "tasks": {
                "total": sprint.metrics["total_tasks"],
                "completed": sprint.metrics["completed_tasks"],
                "completion_rate": f"{sprint.metrics['completed_tasks'] / sprint.metrics['total_tasks'] * 100:.1f}%"
            },
            "generated_files": len(self._get_all_generated_files()),
            "agents": {
                agent_name: agent.get_status()
                for agent_name, agent in self.team.items()
            },
            "start_date": sprint.start_date,
            "end_date": sprint.end_date
        }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Основная функция для демонстрации системы"""
    
    # Конфигурация проекта
    config = ProjectConfig(
        name="AI Personal Assistant",
        description="Сервис личного AI ассистента с поддержкой Telegram, Web и Mobile",
        root_path="./ai_assistant_project",
        tech_stack={
            "backend": "Python + FastAPI",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL",
            "devops": "Docker + GitHub Actions"
        },
        requirements="""
        1. User Authentication System
           - Registration и Login
           - JWT tokens
           - Profile management
        
        2. Chat Interface
           - Real-time messaging
           - Message history
           - File upload support
        
        3. AI Agents Integration
           - Claude API integration
           - Agent routing
           - Response streaming
        
        4. Backend API
           - RESTful endpoints
           - Database models
           - Business logic
        
        5. Frontend UI
           - Chat interface
           - Agent selector
           - File management
        
        6. DevOps Setup
           - Docker containers
           - CI/CD pipeline
           - Monitoring
        """
    )
    
    # Создать PM Agent
    pm = PMAgent(config)
    
    # Спланировать спринт
    sprint = await pm.plan_sprint("Sprint 1: Core Setup", duration_days=7)
    
    # Выполнить спринт
    results = await pm.execute_sprint(sprint)
    
    # Показать отчет
    report = pm.get_sprint_report()
    
    print("\n" + "="*60)
    print("📊 ОТЧЕТ ПО СПРИНТУ")
    print("="*60)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
