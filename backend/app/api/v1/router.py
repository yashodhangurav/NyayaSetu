"""Version 1 API Central Router."""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.openai_compat import router as openai_compat_router
from app.modules.admin.router import router as admin_router
from app.modules.advocates.router import router as advocates_router
from app.modules.appointments.router import router as appointments_router
from app.modules.auth.router import router as auth_router
from app.modules.cases.router import router as cases_router
from app.modules.communication.router import router as communication_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.deadlines.router import router as deadlines_router
from app.modules.documents.router import router as documents_router
from app.modules.legal_assistant.router import alias_router as legal_assistant_alias_router
from app.modules.legal_assistant.router import router as legal_assistant_router
from app.modules.legal_knowledge.router import router as legal_knowledge_router
from app.modules.matching.router import router as matching_router
from app.modules.reviews.router import router as reviews_router
from app.modules.triage.router import router as triage_router
from app.modules.users.router import router as users_router

api_v1_router = APIRouter()

# System Diagnostic Endpoint
api_v1_router.include_router(health_router)
api_v1_router.include_router(openai_compat_router)

# Domain Module Routers
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(advocates_router)
api_v1_router.include_router(cases_router)
api_v1_router.include_router(communication_router)
api_v1_router.include_router(reviews_router)
api_v1_router.include_router(triage_router)
api_v1_router.include_router(matching_router)
api_v1_router.include_router(legal_knowledge_router)
api_v1_router.include_router(legal_assistant_router)
api_v1_router.include_router(legal_assistant_alias_router)
api_v1_router.include_router(documents_router)
api_v1_router.include_router(appointments_router)
api_v1_router.include_router(deadlines_router)
api_v1_router.include_router(admin_router)
