import { api } from "@/lib/api-client";

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
}

// ---------------------------------------------------------------------------
// Live Grounded Legal AI Assistant Engine (Live Backend RAG + Groq)
// ---------------------------------------------------------------------------
export async function getAssistantAnswer(
  query: string,
  preferredLanguage?: string,
  signal?: AbortSignal,
): Promise<AssistantAnswer> {
  const trimmed = query.trim();
  const lower = trimmed.toLowerCase();

  const res = await api.post<BackendAskResponse>("/api/v1/legal/ask", {
    query: trimmed,
    preferred_language: preferredLanguage || "en",
    max_sources: 5,
  }, { signal });

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
    isEmergency: res.decision_badge === "Urgent" && /arrest|custody|lockup|assault|violence|emergency|112/i.test(lower),
    language: res.detected_language === "hi" || res.detected_language === "kn" ? res.detected_language : "en",
  };
}
