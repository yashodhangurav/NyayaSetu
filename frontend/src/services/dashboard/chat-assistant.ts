import { api } from "@/lib/api-client";
import {
  AssistantServiceError,
  getAssistantFailureFromResponse,
} from "@/services/dashboard/chat-error-handling";

export type DecisionBadgeType =
  | "Self-help first"
  | "Advocate advised"
  | "Time-sensitive"
  | "Urgent";

export interface CitationItem {
  id: string;
  act: string;
  section: string;
  title: string;
  snippet: string;
  url: string;
}

export interface AssessmentQuestionItem {
  id: string;
  question: string;
  help_text?: string;
  type: "single_choice" | "multiple_choice" | "yes_no" | "text" | "state_district" | "date" | "document_upload";
  options: string[];
  allows_custom: boolean;
  is_skippable: boolean;
  field_key: string;
}

export interface ActionStepItem {
  id: string;
  title: string;
  description: string;
  priority: "URGENT" | "HIGH" | "MEDIUM" | "LOW";
  status: "pending" | "in_progress" | "completed" | "blocked" | "not_applicable";
  dependencies: string[];
  required_documents: string[];
  relevant_authority?: string;
  deadline?: string;
  assistance_action?: string;
}

export interface LegalActionPlanItem {
  id: string;
  case_summary: string;
  assessment_status: string;
  legal_domain: string;
  dispute_category: string;
  jurisdiction: string;
  possible_remedy: string;
  recommended_first_action: string;
  relevant_authorities: string[];
  required_documents: string[];
  steps: ActionStepItem[];
  verified_fees_or_costs?: string;
  alternative_options: string[];
}

export interface DocumentDraftItem {
  document_type: string;
  title: string;
  target_authority: string;
  subject: string;
  content: string;
  placeholders_to_fill: string[];
  required_attachments: string[];
  filing_instructions: string[];
  is_draft: boolean;
  disclaimer: string;
}

export interface LegalAidInfoItem {
  is_eligible: boolean;
  eligibility_criteria: string[];
  applicable_authority: string;
  helpline: string;
  application_steps: string[];
  statutory_basis: string;
}

export interface CaseSummaryItem {
  dispute_category: string;
  jurisdiction: Record<string, string>;
  confirmed_facts: Record<string, any>;
  missing_facts: string[];
  assessment_status: string;
}

export interface AssistantAnswer {
  kind: "answer" | "greeting";
  id: string;
  decisionBadge: DecisionBadgeType;
  oneLineSummary: string;
  explanation: string[];
  legalPoints: Array<{ explanation: string; citation: CitationItem }>;
  documentsToGather: string[];
  factsToConfirm: string[];
  nextSteps: Array<{
    step: number;
    text: string;
  }>;
  deadline?: NonNullable<BackendAskResponse["deadline"]>;
  citations: CitationItem[];
  isLowConfidence?: boolean;
  confidenceReason?: string;
  followUpChips?: string[];
  isEmergency?: boolean;
  language?: "en" | "kn" | "hi";
  generationStatus?: string;
  generationError?: string;
  retryAfterSeconds?: number;
  isRetryable?: boolean;
  // Interactive Problem-Solving Extensions
  responseType?:
  | "DIRECT_ANSWER"
  | "CASE_ASSESSMENT"
  | "CLARIFICATION"
  | "LEGAL_ACTION_PLAN"
  | "CASE_FOLLOW_UP"
  | "DOCUMENT_GENERATION"
  | "DOCUMENT_ANALYSIS"
  | "LEGAL_AID"
  | "URGENT_ASSISTANCE"
  | "OUT_OF_SCOPE";
  workflowState?: string;
  conversationId?: string;
  caseId?: string;
  assessmentQuestions?: AssessmentQuestionItem[];
  caseSummary?: CaseSummaryItem;
  actionPlan?: LegalActionPlanItem;
  documentDraft?: DocumentDraftItem;
  legalAidInfo?: LegalAidInfoItem;
  urgentAssistance?: {
    category: string;
    helpline: string;
    action: string;
    secondary_helplines?: string[];
  };
  availableActions?: string[];
}

export interface FictionalAdvocate {
  id: string;
  name: string;
  court: string;
  practiceAreas: string;
  languages: string[];
  enrolmentBadge: string;
  activityBadge: string;
  feeRange: string;
}

export interface CaseBriefData {
  facts: string;
  timeline: string;
  parties: string;
  documents: string[];
  relevantSections: string[];
  probableForum: string;
  deadline: string;
}

export interface ScanExplainResult {
  fileName: string;
  fileSize: string;
  whatThisIs: string;
  deadlinesFound: string;
  amounts: string;
  whatToDoNext: string;
}

// ---------------------------------------------------------------------------
// Fictional Advocates (Belagavi District & Sessions Court aware)
// ---------------------------------------------------------------------------
export const MOCK_MATCHED_ADVOCATES: FictionalAdvocate[] = [
  {
    id: "adv_1",
    name: "Adv. Sujata V. Patil",
    court: "Belagavi District & Sessions Court",
    practiceAreas: "Tenancy disputes, Rent Controller proceedings, Civil recovery",
    languages: ["Kannada", "English", "Marathi"],
    enrolmentBadge: "Enrolment verified",
    activityBadge: "Court activity confirmed",
    feeRange: "₹1,500 – ₹3,000 / consult",
  },
  {
    id: "adv_2",
    name: "Adv. Anand R. Kulkarni",
    court: "Belagavi District & Sessions Court",
    practiceAreas: "Section 138 NI Act, Negotiable Instruments, Commercial debt",
    languages: ["Kannada", "English", "Hindi"],
    enrolmentBadge: "Enrolment verified",
    activityBadge: "Court activity confirmed",
    feeRange: "₹2,000 – ₹4,000 / consult",
  },
  {
    id: "adv_3",
    name: "Adv. Basavaraj S. Hiremath",
    court: "Belagavi District & Sessions Court",
    practiceAreas: "Ancestral property, Hindu Succession Act, Partition suits",
    languages: ["Kannada", "English"],
    enrolmentBadge: "Enrolment verified",
    activityBadge: "Court activity confirmed",
    feeRange: "₹1,800 – ₹3,500 / consult",
  },
];

interface BackendAskResponse {
  kind: AssistantAnswer["kind"];
  query: string;
  detected_language: string;
  answer: string;
  decision_badge: DecisionBadgeType;
  sources_found: boolean;
  citations: Array<{
    source_title: string;
    source_type: string;
    act_or_judgment_identifier?: string;
    section_or_paragraph?: string;
    clause_heading?: string;
    official_source_url?: string;
    content_checksum?: string;
    relevant_text?: string;
    is_verified_in_corpus?: boolean;
  }>;
  legal_points?: Array<{ explanation: string; source_checksum: string }>;
  documents_to_gather?: string[];
  facts_to_confirm?: string[];
  suggested_next_steps: string[];
  deadline?: {
    title: string;
    days_remaining?: number;
    target_date?: string;
    statutory_basis?: string;
    action_label?: string;
  } | null;
  confidence_level: string;
  confidence_note?: string | null;
  follow_up_suggestions: string[];
  disclaimer: string;
  retrieved_chunks_count: number;
  generation_status?: string;
  generation_error?: string | null;
  retry_after_seconds?: number | null;
  is_retryable?: boolean;
  provider_name?: string | null;
  response_type?: AssistantAnswer["responseType"];
  workflow_state?: string;
  conversation_id?: string;
  case_id?: string;
  assessment_questions?: AssessmentQuestionItem[];
  case_summary?: CaseSummaryItem;
  action_plan?: LegalActionPlanItem;
  document_draft?: DocumentDraftItem;
  legal_aid_info?: LegalAidInfoItem;
  urgent_assistance?: AssistantAnswer["urgentAssistance"];
  available_actions?: string[];
}

// ---------------------------------------------------------------------------
// Live Grounded Legal AI Assistant Engine (Live Backend RAG + Groq)
// ---------------------------------------------------------------------------
export async function getAssistantAnswer(
  query: string,
  preferredLanguage?: string,
  signal?: AbortSignal,
  options?: {
    conversationId?: string;
    caseId?: string;
    assessmentAnswers?: Record<string, any>;
    actionType?: string;
    actionPayload?: Record<string, any>;
  },
): Promise<AssistantAnswer> {
  const trimmed = query.trim();
  const lower = trimmed.toLowerCase();

  const res = await api.post<BackendAskResponse>("/api/v1/legal/ask", {
    query: trimmed,
    preferred_language: preferredLanguage || "en",
    max_sources: 5,
    conversation_id: options?.conversationId,
    case_id: options?.caseId,
    assessment_answers: options?.assessmentAnswers,
    action_type: options?.actionType,
    action_payload: options?.actionPayload,
  }, { signal });

  const failure = getAssistantFailureFromResponse(res);
  if (failure) throw new AssistantServiceError(failure);

  const paragraphs = res.answer.split(/\n\s*\n/).map((paragraph) => paragraph.trim()).filter(Boolean);
  const citations = res.citations.map((citation, index) => ({
    id: citation.content_checksum || `cit_${index}`,
    act: citation.source_title,
    section: citation.section_or_paragraph || "Statutory provision",
    title: citation.clause_heading || citation.source_title,
    snippet: citation.relevant_text || "",
    url: citation.official_source_url || "",
  }));
  const legalPoints = (res.legal_points ?? []).flatMap((point) => {
    const citation = citations.find((item) => item.id === point.source_checksum);
    return citation ? [{ explanation: point.explanation, citation }] : [];
  });
  const summary = paragraphs[0] ?? res.answer;

  return {
    kind: res.kind,
    id: `ans_${Date.now()}`,
    decisionBadge: res.decision_badge,
    oneLineSummary: summary,
    explanation: res.kind === "greeting" ? paragraphs : paragraphs.slice(1).filter(
      (paragraph) => !legalPoints.some((point) => point.explanation === paragraph)
    ),
    legalPoints,
    documentsToGather: res.documents_to_gather ?? [],
    factsToConfirm: res.facts_to_confirm ?? [],
    nextSteps: res.suggested_next_steps.map((text, index) => ({
      step: index + 1,
      text: text.replace(/^(?:Step\s*\d+:?|\d+\.|-\s*)/i, "").trim(),
    })),
    deadline: res.deadline ?? undefined,
    citations,
    isLowConfidence: res.confidence_level === "LOW",
    confidenceReason: res.confidence_note || undefined,
    followUpChips: res.follow_up_suggestions,
    isEmergency: res.decision_badge === "Urgent" && (/arrest|custody|lockup|assault|violence|emergency|112/i.test(lower) || res.response_type === "URGENT_ASSISTANCE"),
    language: res.detected_language === "hi" || res.detected_language === "kn" ? res.detected_language : "en",
    generationStatus: res.generation_status,
    generationError: res.generation_error ?? undefined,
    retryAfterSeconds: res.retry_after_seconds ?? undefined,
    isRetryable: res.is_retryable,
    responseType: res.response_type || "DIRECT_ANSWER",
    workflowState: res.workflow_state || "ASSESSMENT_COMPLETED",
    conversationId: res.conversation_id,
    caseId: res.case_id,
    assessmentQuestions: res.assessment_questions || [],
    caseSummary: res.case_summary,
    actionPlan: res.action_plan,
    documentDraft: res.document_draft,
    legalAidInfo: res.legal_aid_info,
    urgentAssistance: res.urgent_assistance,
    availableActions: res.available_actions || [],
  };
}

export async function submitAssessmentAnswers(
  conversationId: string,
  answers: Record<string, any>,
  preferredLanguage?: string,
  signal?: AbortSignal,
): Promise<AssistantAnswer> {
  return getAssistantAnswer("Submitting assessment answers", preferredLanguage, signal, {
    conversationId,
    actionType: "submit_assessment",
    assessmentAnswers: answers,
  });
}

export async function executeAssistantAction(
  conversationId: string,
  actionType: string,
  actionPayload?: Record<string, any>,
  preferredLanguage?: string,
  signal?: AbortSignal,
): Promise<AssistantAnswer> {
  return getAssistantAnswer(`Action: ${actionType}`, preferredLanguage, signal, {
    conversationId,
    actionType,
    actionPayload,
  });
}
