"use client";

import React, { useState } from "react";
import {
  CalendarClock,
  ChevronDown,
  Copy,
  ThumbsUp,
  ThumbsDown,
  Flag,
  Share2,
  FolderPlus,
  Scale,
  PhoneCall,
  HelpCircle,
  Check,
} from "lucide-react";
import type { AssistantAnswer } from "@/services/dashboard/chat-assistant";
import { CitationChip } from "@/components/dashboard/shared";
import { Badge, Button } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";
import { CaseBriefFlow } from "./CaseBriefFlow";
import { AdvocateMatchInline } from "./AdvocateMatchInline";
import { FlagErrorDialog } from "./FlagErrorDialog";

interface AssistantAnswerCardProps {
  answer: AssistantAnswer;
  onSaveToCases: (title: string, summary: string) => void;
  onRequestConsultation: (advocateName: string) => void;
  onFollowUpClick: (prompt: string) => void;
  onShowToast: (message: string) => void;
}

function AnswerDetails({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <details className="group border-t border-[#ded4c5]">
      <summary className="flex cursor-pointer list-none items-center justify-between gap-4 py-3.5 font-sans text-[15px] font-medium text-[#493727] outline-offset-2 hover:text-[#855a2c] focus-visible:outline-2 [&::-webkit-details-marker]:hidden">
        {title}
        <ChevronDown className="size-4 shrink-0 text-[#816541] transition-transform group-open:rotate-180" aria-hidden="true" />
      </summary>
      <div className="space-y-3 pb-4 text-[15px] leading-6 text-[#4f4033]">{children}</div>
    </details>
  );
}

export function AssistantAnswerCard({
  answer,
  onSaveToCases,
  onRequestConsultation,
  onFollowUpClick,
  onShowToast,
}: AssistantAnswerCardProps) {
  const extraCitations = answer.citations.filter((citation) =>
    !answer.legalPoints.some((point) => point.citation.id === citation.id)
  );
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);
  const [showCaseBrief, setShowCaseBrief] = useState(false);
  const [showAdvocates, setShowAdvocates] = useState(false);
  const [showFlagInput, setShowFlagInput] = useState(false);

  const handleCopy = () => {
    const textToCopy = [
      answer.oneLineSummary,
      ...answer.explanation,
      ...answer.legalPoints.map(({ explanation, citation }) =>
        `${explanation} (${citation.act}, ${citation.section}) ${citation.url}`
      ),
      ...(answer.nextSteps.length ? ["What to do next", ...answer.nextSteps.map((s) => `${s.step}. ${s.text}`)] : []),
      ...(answer.documentsToGather.length ? ["Documents to gather", ...answer.documentsToGather] : []),
      ...(answer.factsToConfirm.length ? ["Details that could change the answer", ...answer.factsToConfirm] : []),
      ...(answer.deadline ? [
        answer.deadline.title,
        answer.deadline.statutory_basis,
        answer.deadline.target_date,
        "Have an empanelled advocate review any statutory deadline.",
      ] : []),
      answer.confidenceReason,
    ].filter(Boolean).join("\n\n");
    void navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    onShowToast("Answer copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const badgeToneMap: Record<AssistantAnswer["decisionBadge"], "mint" | "warn" | "neutral" | "danger"> = {
    "Self-help first": "mint",
    "Time-sensitive": "warn",
    "Advocate advised": "neutral",
    Urgent: "danger",
  };

  return (
    <div className="space-y-4 animate-in-up">
      <div className="min-w-0 rounded-[2px] border border-[#d9cebd] border-t-[3px] border-t-[#966931] bg-[#fffaf2] px-4 py-5 text-[#2a1c12] sm:px-7 sm:py-6 [overflow-wrap:anywhere]">
        {/* 1. Decision badge + one-line answer */}
        <div className="space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className="text-sm font-medium text-[#725330]">Short answer</span>
            <Badge tone={badgeToneMap[answer.decisionBadge]}>
              {answer.decisionBadge}
            </Badge>
          </div>
          <p className="max-w-[54ch] font-serif text-[22px] leading-[1.28] text-[#2a1c12] sm:text-[26px]">
            {answer.oneLineSummary}
          </p>
        </div>

        {answer.isEmergency && (
          <div className="pt-2 border-t border-[#e2d5c1]/70 flex flex-wrap items-center gap-2.5">
            <a
              href="tel:112"
              className="inline-flex h-9 items-center justify-center gap-1.5 rounded-[2px] border border-[#c0392b] bg-[#c0392b] px-4 text-xs font-sans uppercase tracking-[0.08em] font-semibold text-[#fffaf2] transition-colors hover:bg-[#a93226]"
            >
              <PhoneCall className="size-3.5" aria-hidden="true" />
              Call 112 Police
            </a>
            <a
              href="tel:15100"
              className="inline-flex h-9 items-center justify-center gap-1.5 rounded-[2px] border border-[#2a1c12] bg-[#2a1c12] px-4 text-xs font-sans uppercase tracking-[0.08em] font-semibold text-[#fffaf2] transition-colors hover:bg-[#9a6a35] hover:border-[#9a6a35]"
            >
              <PhoneCall className="size-3.5" aria-hidden="true" />
              Call 15100 (Free Legal Aid)
            </a>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => setShowAdvocates((prev) => !prev)}
              className="h-9 text-xs"
            >
              <Scale className="size-3.5 mr-1 text-[#9a6a35]" aria-hidden="true" />
              Connect to an advocate urgently
            </Button>
          </div>
        )}

        {answer.deadline && (
          <div className="mt-4 space-y-1 rounded-[2px] border border-[#e2d5c1] bg-[#fff8e7] p-3 text-sm">
            <div className="flex flex-wrap items-center gap-2 font-semibold">
              <CalendarClock className="size-4 text-[#b54708]" aria-hidden="true" />
              {answer.deadline.title}
            </div>
            {answer.deadline.statutory_basis && <p>{answer.deadline.statutory_basis}</p>}
            {answer.deadline.target_date && <p>Estimated deadline {answer.deadline.target_date}</p>}
            <p>Have an empanelled advocate review any statutory deadline.</p>
          </div>
        )}

        {answer.isLowConfidence && answer.confidenceReason && (
          <p className="mt-3 flex items-start gap-2 text-sm leading-6 text-[#6a4d2b]">
            <HelpCircle className="mt-1 size-4 shrink-0" aria-hidden="true" />
            {answer.confidenceReason}
          </p>
        )}

        {answer.nextSteps.length > 0 && (
          <section className="mt-5 rounded-[2px] bg-[#f4eee4] px-4 py-4 sm:px-5">
            <h3 className="font-serif text-[21px] leading-tight">What to do next</h3>
            <ol className="mt-1 divide-y divide-[#ded4c5]">
              {answer.nextSteps.map((step) => (
                <li key={step.step} className="flex gap-3 pt-3 pb-3 last:pb-0">
                  <span aria-hidden="true" className="w-5 shrink-0 font-mono text-sm leading-6 text-[#805c33]">
                    {step.step}.
                  </span>
                  <span className="max-w-[65ch] font-sans text-[15px] leading-6">{step.text}</span>
                </li>
              ))}
            </ol>
          </section>
        )}

        <div className="mt-5">
          {(answer.legalPoints.length > 0 || answer.explanation.length > 0 || extraCitations.length > 0) && (
            <AnswerDetails title="Legal explanation and sources">
              {answer.explanation.map((paragraph, index) => <p key={index}>{paragraph}</p>)}
              {answer.legalPoints.map((point, index) => (
                <div key={index} className="max-w-[65ch] space-y-1.5 border-l-2 border-[#c5a578] pl-3">
                  <p>{point.explanation}</p>
                  <CitationChip citation={point.citation} />
                </div>
              ))}
              {extraCitations.map((citation) => <CitationChip key={citation.id} citation={citation} />)}
            </AnswerDetails>
          )}
          {[
            { title: "Documents to gather", items: answer.documentsToGather },
            { title: "Details to confirm", items: answer.factsToConfirm },
          ].map(({ title, items }) => items.length > 0 && (
            <AnswerDetails key={title} title={title}>
              <ul className="list-disc space-y-2 pl-5 marker:text-[#966931]">
                {items.map((item, index) => <li key={index}>{item}</li>)}
              </ul>
            </AnswerDetails>
          ))}
        </div>

        {answer.followUpChips && answer.followUpChips.length > 0 && (
          <AnswerDetails title="Follow-up questions">
            <div className="flex flex-wrap gap-2">
              {answer.followUpChips.map((chip) => (
                <button
                  key={chip}
                  type="button"
                  onClick={() => onFollowUpClick(chip)}
                  className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 px-3 py-1 text-xs text-[#5b4a3b] hover:border-[#9a6a35] hover:text-[#2a1c12] transition-colors cursor-pointer"
                >
                  {chip}
                </button>
              ))}
            </div>
          </AnswerDetails>
        )}
        <AnswerDetails title="Answer tools">
          <div className="pt-2 border-t border-[#e2d5c1]/60 flex flex-wrap items-center justify-between gap-1 text-xs">
            <div className="flex flex-wrap items-center gap-1">
              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  onSaveToCases(answer.decisionBadge, answer.oneLineSummary);
                  onShowToast("Saved matter summary to My Cases");
                }}
                className="h-8 text-[11px] px-2 text-[#5b4a3b]"
              >
                <FolderPlus className="size-3.5 mr-1" aria-hidden="true" />
                Save to My Cases
              </Button>

              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  setShowCaseBrief((v) => !v);
                  setShowAdvocates(false);
                }}
                className={cn("h-8 text-[11px] px-2 text-[#5b4a3b]", showCaseBrief && "bg-[#ebe1d1]/60 text-[#2a1c12]")}
              >
                <Share2 className="size-3.5 mr-1 text-[#9a6a35]" aria-hidden="true" />
                Prepare case brief
              </Button>

              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  setShowAdvocates((v) => !v);
                  setShowCaseBrief(false);
                }}
                className={cn("h-8 text-[11px] px-2 text-[#5b4a3b]", showAdvocates && "bg-[#ebe1d1]/60 text-[#2a1c12]")}
              >
                <Scale className="size-3.5 mr-1 text-[#9a6a35]" aria-hidden="true" />
                Find advocate
              </Button>
            </div>

            <div className="flex items-center gap-0.5 text-[#85725f]">
              <button
                type="button"
                onClick={handleCopy}
                aria-label="Copy answer"
                className="grid size-8 place-items-center rounded-[2px] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
              >
                {copied ? <Check className="size-3.5 text-[#2e7d32]" /> : <Copy className="size-3.5" />}
              </button>
              <button
                type="button"
                onClick={() => {
                  setFeedback("up");
                  onShowToast("Feedback recorded: Helpful");
                }}
                aria-label="Helpful"
                className={cn(
                  "grid size-8 place-items-center rounded-[2px] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors",
                  feedback === "up" && "text-[#2e7d32]"
                )}
              >
                <ThumbsUp className="size-3.5" />
              </button>
              <button
                type="button"
                onClick={() => {
                  setFeedback("down");
                  onShowToast("Feedback recorded: Needs revision");
                }}
                aria-label="Not helpful"
                className={cn(
                  "grid size-8 place-items-center rounded-[2px] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors",
                  feedback === "down" && "text-[#c0392b]"
                )}
              >
                <ThumbsDown className="size-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setShowFlagInput((v) => !v)}
                aria-label="Flag an error"
                className="grid size-8 place-items-center rounded-[2px] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
                title="Flag an error"
              >
                <Flag className="size-3.5" />
              </button>
            </div>
          </div>

        </AnswerDetails>

        {/* Flag Error Inline Form */}
        {showFlagInput && (
          <FlagErrorDialog
            onClose={() => setShowFlagInput(false)}
            onSubmitFlag={() => {
              setShowFlagInput(false);
              onShowToast("Sent to reviewing advocates");
            }}
          />
        )}
      </div>

      {/* Inline Case Brief Flow */}
      {showCaseBrief && (
        <CaseBriefFlow
          onClose={() => setShowCaseBrief(false)}
          onSaveToCases={(brief) => {
            onSaveToCases("Formal Case Matter Brief", brief.facts);
            onShowToast("Case brief saved to My Cases");
          }}
          onShareWithAdvocate={() => {
            setShowCaseBrief(false);
            setShowAdvocates(true);
            onShowToast("Consent logged under DPDP Act · Advocates matched below");
          }}
        />
      )}

      {/* Inline Advocate Matches */}
      {showAdvocates && (
        <AdvocateMatchInline
          onClose={() => setShowAdvocates(false)}
          onRequestConsultation={(name) => {
            onRequestConsultation(name);
            onShowToast(`Consultation request sent to ${name}`);
          }}
        />
      )}


    </div>
  );
}
