"""Pydantic v2 schemas for the Legal AI Assistant (RAG)."""

from datetime import date, datetime
from typing import Annotated, Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class LegalAskRequest(BaseModel):
    """Payload for submitting a legal inquiry to the Legal AI Assistant."""

    query: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)] = Field(description="The legal question or grievance description")
    jurisdiction: Optional[str] = Field(None, description="Optional jurisdiction filter (e.g., Union of India, Maharashtra, Delhi)")
    preferred_language: str = Field("en", description="Target language code: 'en' (English), 'hi' (Hindi), 'kn' (Kannada)")
    max_sources: int = Field(5, ge=1, le=10, description="Maximum number of supporting legal chunks to retrieve")
    conversation_id: Optional[str] = Field(None, description="Optional persistent conversation identifier for stateful sessions")
    case_id: Optional[str] = Field(None, description="Optional linked LegalCase UUID")
    assessment_answers: Optional[Dict[str, Any]] = Field(None, description="Answers to previously issued assessment questions")
    action_type: Optional[str] = Field(None, description="Requested interaction: 'answer' | 'submit_assessment' | 'generate_plan' | 'draft_document' | 'toggle_step' | 'legal_aid'")
    action_payload: Optional[Dict[str, Any]] = Field(None, description="Parameters associated with action_type")


class AssessmentQuestion(BaseModel):
    """Dynamic assessment question to collect missing material facts."""

    id: str = Field(..., description="Unique question identifier e.g. 'prop_dispute_type'")
    question: str = Field(..., description="Plain-language question for the citizen")
    help_text: Optional[str] = Field(None, description="Why this fact changes the legal remedy")
    type: Literal["single_choice", "multiple_choice", "yes_no", "text", "state_district", "date", "document_upload"] = Field(
        "single_choice", description="Input widget type"
    )
    options: List[str] = Field(default_factory=list, description="Preset answer choices")
    allows_custom: bool = Field(True, description="Whether user can type freeform response")
    is_skippable: bool = Field(True, description="Whether question can be skipped")
    field_key: str = Field(..., description="Case fact attribute name mapped to this question")


class ActionStep(BaseModel):
    """Structured actionable step in a citizen legal roadmap."""

    id: str = Field(..., description="Step code e.g. 'step_1_encumbrance'")
    title: str = Field(..., description="Concise action imperative")
    description: str = Field(..., description="Detailed practical instruction")
    priority: Literal["URGENT", "HIGH", "MEDIUM", "LOW"] = "MEDIUM"
    status: Literal["pending", "in_progress", "completed", "blocked", "not_applicable"] = "pending"
    dependencies: List[str] = Field(default_factory=list, description="IDs of steps that must precede this")
    required_documents: List[str] = Field(default_factory=list, description="Supporting documents to assemble")
    relevant_authority: Optional[str] = Field(None, description="Designated court, tribunal, or government office")
    deadline: Optional[str] = Field(None, description="Statutory or practical cutoff")
    supporting_citation_ids: List[str] = Field(default_factory=list)
    assistance_action: Optional[str] = Field(None, description="One-click CTA e.g. 'draft_complaint' | 'view_checklist' | 'find_advocate'")


class LegalActionPlan(BaseModel):
    """Personalized step-by-step roadmap grounded in verified law."""

    id: str = Field(..., description="Action plan identifier")
    case_summary: str = Field(..., description="Contextual summary of citizen matter")
    assessment_status: str = Field("ASSESSMENT_COMPLETED", description="Workflow state")
    legal_domain: str = Field(..., description="Primary legal domain")
    dispute_category: str = Field(..., description="Specific dispute taxonomy")
    jurisdiction: str = Field("Karnataka", description="Governing state or central jurisdiction")
    possible_remedy: str = Field(..., description="Legal or administrative remedy applicable")
    recommended_first_action: str = Field(..., description="Immediate concrete next action")
    relevant_authorities: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    steps: List[ActionStep] = Field(default_factory=list)
    verified_fees_or_costs: Optional[str] = None
    alternative_options: List[str] = Field(default_factory=list)


class CaseSummaryData(BaseModel):
    """Structured case facts snapshot."""

    dispute_category: str
    jurisdiction: Dict[str, str] = Field(default_factory=dict)
    confirmed_facts: Dict[str, Any] = Field(default_factory=dict)
    missing_facts: List[str] = Field(default_factory=list)
    assessment_status: str


class DocumentDraft(BaseModel):
    """Personalized draft legal document or complaint."""

    document_type: str = Field(..., description="e.g. 'POLICE_COMPLAINT_FIR' | 'CONSUMER_COMPLAINT' | 'RTI_APPLICATION' | 'LEGAL_AID_PETITION'")
    title: str
    target_authority: str
    subject: str
    content: str
    placeholders_to_fill: List[str] = Field(default_factory=list)
    required_attachments: List[str] = Field(default_factory=list)
    filing_instructions: List[str] = Field(default_factory=list)
    is_draft: bool = True
    disclaimer: str = "DRAFT FOR REVIEW ONLY. Must be signed and verified before submission to any authority."


class LegalAidInfo(BaseModel):
    """Free Legal Aid eligibility and application routing."""

    is_eligible: bool
    eligibility_criteria: List[str]
    applicable_authority: str
    helpline: str = "15100"
    application_steps: List[str]
    statutory_basis: str = "Section 12, Legal Services Authorities Act, 1987"


class CitationItem(BaseModel):
    """Verified statutory or judicial citation grounded in official source records."""

    source_title: str = Field(..., description="Official Act title or published judgment name")
    source_type: str = Field(..., description="BARE_ACT | COURT_JUDGMENT | GAZETTE_NOTIFICATION | LEGAL_AID_SCHEME")
    act_or_judgment_identifier: Optional[str] = Field(None, description="Official Act number or citation (e.g., Act No. 26 of 1881)")
    section_or_paragraph: Optional[str] = Field(None, description="Specific statutory section or judgment paragraph")
    clause_heading: Optional[str] = Field(None, description="Official section heading or ratio headline")
    official_source_url: Optional[str] = Field(None, description="Government gazette, e-Courts, or IndiaCode URL")
    jurisdiction: Optional[str] = Field("Union of India", description="Territorial jurisdiction of the legal source")
    document_version: Optional[str] = Field("1.0", description="Version or effective date information")
    relevant_text: Optional[str] = Field(None, description="Verbatim statutory text snippet extracted from source chunk")
    content_checksum: Optional[str] = Field(None, description="SHA-256 checksum of verified source chunk")
    is_verified_in_corpus: bool = Field(True, description="Strictly verified against retrieved knowledge base records")

    model_config = ConfigDict(from_attributes=True)


class DeadlineInfo(BaseModel):
    """Statutory deadline information computed for the legal inquiry."""

    title: str = Field(..., description="Short title of the limitation deadline")
    days_remaining: Optional[int] = Field(None, description="Calculated days remaining")
    target_date: Optional[str] = Field(None, description="Calculated cutoff date formatted as DD MMM YYYY")
    statutory_basis: Optional[str] = Field(None, description="Act and section governing limitation")
    action_label: str = Field("Add to Court Deadlines", description="Action button CTA")


class LegalPoint(BaseModel):
    explanation: str
    source_checksum: str


class LegalAskResponse(BaseModel):
    """Structured response from the Legal AI Assistant."""

    query: str
    kind: Literal["answer", "greeting"] = "answer"
    detected_language: str = Field(..., description="Identified question language (en, hi, kn)")
    answer: str = Field(..., description="Factual, grounded legal explanation derived strictly from retrieved sources")
    decision_badge: str = Field("Self-help first", description="'Self-help first' | 'Advocate advised' | 'Time-sensitive' | 'Urgent'")
    sources_found: bool = Field(..., description="Whether supporting statutory provisions were located in the curated corpus")
    citations: List[CitationItem] = Field(default_factory=list, description="Verified citations corresponding to the answer")
    unverified_citations_detected: List[str] = Field(default_factory=list, description="Citations pruned due to lack of corpus backing")
    legal_points: List[LegalPoint] = Field(default_factory=list)
    documents_to_gather: List[str] = Field(default_factory=list)
    facts_to_confirm: List[str] = Field(default_factory=list)
    suggested_next_steps: List[str] = Field(default_factory=list, description="Actionable statutory next steps (e.g., notice, advocate consultation)")
    deadline: Optional[DeadlineInfo] = Field(None, description="Computed statutory deadline if applicable")
    confidence_level: str = Field("HIGH", description="Confidence tier: HIGH | MEDIUM | LOW")
    confidence_note: Optional[str] = Field(None, description="Note displayed when confidence is not HIGH")
    follow_up_suggestions: List[str] = Field(default_factory=list, description="Up to 3 recommended follow-up questions")
    disclaimer: str = Field(
        default=(
            "NyayaSetu AI Legal Assistant provides informational guidance derived strictly from official Indian Bare Acts "
            "and published judicial precedents. This information does not constitute formal legal advice or create an "
            "advocate-client relationship. Litigants should consult an empanelled, verified advocate for matter-specific representation."
        ),
        description="Statutory non-advice disclaimer",
    )
    retrieved_chunks_count: int
    claim_support: Optional[Dict[str, Any]] = Field(
        default=None, description="Lexical claim-support diagnostics for generated prose"
    )
    evidence_sufficient: bool = Field(True, description="Whether retrieval met configured evidence thresholds")
    retrieval_source: str = Field("NONE", description="Verified database or immutable bundled corpus")
    # Additive generation diagnostics. Existing clients can ignore these fields.
    generation_status: str = Field(
        "ok",
        description=(
            "Generation outcome: ok, rate_limited, timeout, provider_unavailable, "
            "insufficient_evidence, or generation_error"
        ),
    )
    generation_error: Optional[str] = Field(None, description="Safe user-facing generation error, when applicable")
    retry_after_seconds: Optional[float] = Field(None, description="Provider-indicated retry delay in seconds")
    is_retryable: bool = Field(False, description="Whether repeating the same question is likely to succeed")
    provider_name: Optional[str] = Field(None, description="Configured generation provider used for this response")
    assessed_at: datetime
    # --- Interactive Problem-Solving Agent Extensions ---
    response_type: Literal[
        "DIRECT_ANSWER",
        "CASE_ASSESSMENT",
        "CLARIFICATION",
        "LEGAL_ACTION_PLAN",
        "CASE_FOLLOW_UP",
        "DOCUMENT_GENERATION",
        "DOCUMENT_ANALYSIS",
        "LEGAL_AID",
        "URGENT_ASSISTANCE",
        "OUT_OF_SCOPE",
    ] = "DIRECT_ANSWER"
    workflow_state: str = Field("ASSESSMENT_COMPLETED", description="Current state machine stage")
    conversation_id: Optional[str] = Field(None, description="Persistent conversation session ID")
    case_id: Optional[str] = Field(None, description="Linked LegalCase reference ID")
    assessment_questions: List[AssessmentQuestion] = Field(default_factory=list, description="Questions required for assessment")
    case_summary: Optional[CaseSummaryData] = Field(None, description="Current confirmed case facts and jurisdiction")
    action_plan: Optional[LegalActionPlan] = Field(None, description="Step-by-step action plan")
    document_draft: Optional[DocumentDraft] = Field(None, description="Personalized draft legal document or petition")
    legal_aid_info: Optional[LegalAidInfo] = Field(None, description="Legal aid eligibility and helpline guidance")
    urgent_assistance: Optional[Dict[str, Any]] = Field(None, description="Urgent emergency instructions & helplines")
    available_actions: List[str] = Field(default_factory=list, description="CTAs e.g. ['generate_action_plan', 'draft_complaint', 'save_case']")


class LegalSearchRequest(BaseModel):
    """Search request payload for Phase 1 RAG retrieval."""

    query: str = Field(..., min_length=2, max_length=2000)
    top_k: int = Field(5, ge=1, le=20)
    jurisdiction: Optional[str] = None
    filter_in_force_only: bool = True


class LegalSearchResponse(BaseModel):
    """Response payload for Phase 1 RAG retrieval."""

    query: str
    rewritten_query: str
    detected_language: str
    legacy_concordance_detected: Optional[str] = None
    total_results: int
    confidence_score: float
    confidence_level: str
    results: List[Dict[str, Any]]
    message: Optional[str] = None


class LegalSourceCreate(BaseModel):
    """Admin payload to register a curated legal source."""

    source_type: str = Field(..., description="BARE_ACT | COURT_JUDGMENT | GAZETTE_NOTIFICATION | LEGAL_AID_SCHEME")
    title: str = Field(..., min_length=3, max_length=255)
    short_code: Optional[str] = Field(None, max_length=64)
    citation: Optional[str] = Field(None, max_length=255)
    jurisdiction: str = Field("Union of India", max_length=128)
    court: Optional[str] = Field(None, max_length=128)
    act_or_judgment_identifier: Optional[str] = Field(None, max_length=128)
    publication_date: Optional[date] = None
    last_verified_date: Optional[date] = None
    document_version: str = Field("1.0", max_length=32)
    official_source_url: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class LegalChunkCreate(BaseModel):
    """Admin payload to ingest a statutory section or paragraph chunk."""

    section_number: Optional[str] = Field(None, max_length=64)
    clause_heading: Optional[str] = Field(None, max_length=255)
    chunk_text: str = Field(..., min_length=10)
    metadata_json: Optional[Dict[str, Any]] = None


class LegalSourceResponse(BaseModel):
    """Public representation of a verified LegalSource."""

    id: UUID
    source_type: str
    title: str
    short_code: Optional[str] = None
    citation: Optional[str] = None
    jurisdiction: str
    court: Optional[str] = None
    act_or_judgment_identifier: Optional[str] = None
    publication_date: Optional[date] = None
    last_verified_date: Optional[date] = None
    document_version: str
    content_checksum: Optional[str] = None
    official_source_url: Optional[str] = None
    total_chunks: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
