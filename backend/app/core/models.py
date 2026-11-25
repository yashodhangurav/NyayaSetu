"""Consolidated ORM Model Registry for Alembic Discovery and Declarative Metadata."""

from app.core.database import Base
from app.modules.admin.models import AuditLog
from app.modules.advocates.models import AdvocateProfile, AdvocateVerification, AdvocateVerificationApplication
from app.modules.appointments.models import Appointment
from app.modules.auth.models import RefreshToken
from app.modules.cases.models import CaseMessage, LegalCase
from app.modules.communication.models import Conversation, Message
from app.modules.deadlines.models import Deadline
from app.modules.documents.models import Document
from app.modules.legal_knowledge.models import (
    LegalChunk,
    LegalDocumentVersion,
    LegalIngestionJob,
    LegalRelationship,
    LegalReviewItem,
    LegalSource,
    LegalSourceRegistry,
    LegalSyncJob,
)
from app.modules.reviews.models import Review
from app.modules.triage.models import ConsultationRequest
from app.modules.users.models import User, UserConsent

__all__ = [
    "Base",
    "User",
    "UserConsent",
    "RefreshToken",
    "AdvocateProfile",
    "AdvocateVerification",
    "AdvocateVerificationApplication",
    "LegalCase",
    "CaseMessage",
    "Conversation",
    "Message",
    "Review",
    "ConsultationRequest",
    "Appointment",
    "LegalSource",
    "LegalChunk",
    "LegalRelationship",
    "LegalIngestionJob",
    "LegalSourceRegistry",
    "LegalDocumentVersion",
    "LegalSyncJob",
    "LegalReviewItem",
    "Document",
    "Deadline",
    "AuditLog",
]
