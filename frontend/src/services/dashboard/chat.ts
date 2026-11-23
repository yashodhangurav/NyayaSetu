import { api } from "@/lib/api-client";
import { DISCLAIMER } from "./api";
import type { Citation, Message } from "@/types/dashboard";

export interface BackendCitationItem {
  source_title: string;
  source_type: string;
  act_or_judgment_identifier?: string;
  section_or_paragraph?: string;
  clause_heading?: string;
  official_source_url?: string;
  content_checksum?: string;
  is_verified_in_corpus: boolean;
}

export interface BackendLegalAskResponse {
  query: string;
  detected_language: string;
  answer: string;
  decision_badge?: string;
  sources_found: boolean;
  citations: BackendCitationItem[];
  unverified_citations_detected: string[];
  suggested_next_steps: string[];
  deadline?: {
    title: string;
    days_remaining?: number;
    target_date?: string;
    statutory_basis?: string;
    action_label?: string;
  } | null;
  confidence_level?: string;
  confidence_note?: string | null;
  follow_up_suggestions?: string[];
  disclaimer: string;
  retrieved_chunks_count: number;
  assessed_at: string;
}

/**
 * Returns initial conversation history.
 * Empty by default so user starts with a clean single-column agent interface
 * and the 4 starter inquiry cards, with zero fake/dummy preloaded messages.
 */
export async function getConversation(): Promise<Message[]> {
  return [];
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/**
 * Executes grounded question answering via the live RAG Legal Assistant API (/api/v1/legal/ask)
 * with token stream simulation.
 */
export async function streamAnswer(
  question: string,
  onChunk: (chunk: string) => void,
): Promise<{ message: Message }> {
  let responseText = "";
  let citations: Citation[] = [];
  let disclaimerText = DISCLAIMER;

  const res = await api.post<BackendLegalAskResponse>("/api/v1/legal/ask", {
    query: question,
    preferred_language: "en",
    max_sources: 5,
  });

  responseText = res.answer;
  if (res.disclaimer) disclaimerText = res.disclaimer;

  if (res.citations && res.citations.length > 0) {
    citations = res.citations.map((item, idx) => ({
      id: item.content_checksum || `cit_${idx}`,
      act: item.source_title,
      section: item.section_or_paragraph || "Statutory Provision",
      title: item.clause_heading || item.source_title,
      snippet: `Grounded in ${item.source_type.replace(/_/g, " ")}. Identifier: ${item.act_or_judgment_identifier || "Official Gazette"}.`,
      url: item.official_source_url || "https://www.indiacode.nic.in",
    }));
  }

  // Smoothly emit words for an editorial streaming experience
  const words = responseText.split(" ");
  for (let i = 0; i < words.length; i += 3) {
    await sleep(25);
    onChunk(words.slice(i, i + 3).join(" ") + (i + 3 < words.length ? " " : ""));
  }

  const message: Message = {
    id: `msg_${Date.now()}`,
    conversationId: "conv_1",
    role: "assistant",
    content: responseText,
    citations,
    disclaimer: disclaimerText,
    createdAt: new Date().toISOString(),
  };

  return { message };
}
