"use client";

import React, { useEffect, useState } from "react";
import {
  AlertTriangle,
  CalendarClock,
  Clock,
  HelpCircle,
  PhoneCall,
  Scale,
} from "lucide-react";
import {
  type AssistantAnswer,
  calculate138Deadlines,
} from "@/services/dashboard/chat-assistant";
import { CitationChip } from "@/components/dashboard/shared";
import { Button } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";
import { CaseBriefFlow } from "./CaseBriefFlow";
import { AdvocateMatchInline } from "./AdvocateMatchInline";
import { FlagErrorDialog } from "./FlagErrorDialog";
import { ActionBar } from "./primitives/ActionBar";
import { BrandMark } from "./primitives/BrandMark";
import { DecisionBadge } from "./primitives/DecisionBadge";
import { SectionLabel } from "./primitives/SectionLabel";
import { SourcesAccordion } from "./primitives/SourcesAccordion";
import styles from "../chat.module.css";

interface AssistantAnswerCardProps {
  answer: AssistantAnswer;
  onSaveToCases: (title: string, summary: string) => void;
  onAddToDeadlines: (title: string, dueDate: string) => void;
  onRequestConsultation: (advocateName: string) => void;
  onFollowUpClick: (prompt: string) => void;
  onShowToast: (message: string) => void;
}

export function AssistantAnswerCard({
  answer,
  onSaveToCases,
  onAddToDeadlines,
  onRequestConsultation,
  onFollowUpClick,
  onShowToast,
}: AssistantAnswerCardProps) {
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);
  const [showCaseBrief, setShowCaseBrief] = useState(false);
  const [showAdvocates, setShowAdvocates] = useState(false);
  const [showFlagInput, setShowFlagInput] = useState(false);

  // Reactive deadline calculation state (for cheque bounce / 138)
  const [memoDate, setMemoDate] = useState<string>(() => {
    return answer.deadlineCalculation?.memoDate || new Date().toISOString().split("T")[0];
  });

  const activeDeadlines = answer.deadlineCalculation
    ? calculate138Deadlines(memoDate)
    : undefined;

  // Escape closes the most recently expanded inline block.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      // Inline panels own their own Escape handling (so a consent modal
      // closes before the whole brief does).
      if (showFlagInput) setShowFlagInput(false);
      else if (sourcesOpen) setSourcesOpen(false);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [showFlagInput, sourcesOpen]);

  const handleCopy = () => {
    const textToCopy = [
      answer.oneLineSummary,
      ...answer.explanation,
      ...answer.nextSteps.map((s) => `${s.step}. ${s.text}`),
    ].join("\n\n");
    void navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    onShowToast("Answer copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const followUps = answer.followUpChips?.slice(0, 3) ?? [];
  const followUpRow = followUps.length > 0 && (
    <div className="flex flex-wrap gap-1.5">
      {followUps.map((chip) => (
        <button
          key={chip}
          type="button"
          onClick={() => onFollowUpClick(chip)}
          className={cn(
            styles.pill,
            "min-h-10 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 px-3.5 text-xs text-[#5b4a3b] transition-colors hover:border-[#9a6a35] hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:min-h-8"
          )}
        >
          {chip}
        </button>
      ))}
    </div>
  );

  // -------------------------------------------------------------------------
  // EMERGENCY — the only red block in the assistant surface.
  // -------------------------------------------------------------------------
  if (answer.isEmergency) {
    return (
      <div className={cn(styles.fadeIn, "space-y-4")}>
        <div className="rounded-[2px] border border-[#c0392b]/40 bg-[#fffaf2] p-5 shadow-[0_1px_2px_rgba(42,28,18,0.04)] space-y-4 sm:p-6">
          <div className="flex flex-wrap items-start justify-between gap-3 border-b border-[#e2d5c1] pb-3">
            <div className="flex min-w-0 items-start gap-2.5">
              <BrandMark />
              <div className="min-w-0 space-y-1.5">
                <div className="flex flex-wrap items-center gap-2">
                  <SectionLabel className="text-[#c0392b]">
                    Emergency safeguards active
                  </SectionLabel>
                  <span className="font-mono text-[10px] text-[#85725f]">
                    Article 22 Protected
                  </span>
                </div>
                <h3 className="font-serif text-[17px] font-normal leading-snug text-[#2a1c12] sm:text-[19px]">
                  {answer.oneLineSummary}
                </h3>
              </div>
            </div>
            <DecisionBadge variant={answer.decisionBadge} />
          </div>

          <ul className="space-y-2 text-[13px] leading-relaxed text-[#2a1c12]">
            {answer.emergencyBullets?.map((bullet, index) => (
              <li key={index} className="flex items-start gap-2.5">
                <span
                  className="mt-2 size-1.5 shrink-0 rounded-full bg-[#c0392b]"
                  aria-hidden="true"
                />
                <span className="min-w-0 break-words">{bullet}</span>
              </li>
            ))}
          </ul>

          <div className="flex flex-wrap items-center gap-2 border-t border-[#e2d5c1]/70 pt-3">
            <a
              href="tel:112"
              className="inline-flex min-h-10 items-center justify-center gap-1.5 rounded-[2px] border border-[#c0392b] bg-[#c0392b] px-4 text-xs font-medium uppercase tracking-[0.08em] text-[#fffaf2] transition-colors hover:bg-[#a93226] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#96271c]"
            >
              <PhoneCall className="size-3.5" aria-hidden="true" />
              Call 112 Police
            </a>
            <a
              href="tel:15100"
              className="inline-flex min-h-10 items-center justify-center gap-1.5 rounded-[2px] border border-[#2a1c12] bg-[#2a1c12] px-4 text-xs font-medium uppercase tracking-[0.08em] text-[#fffaf2] transition-colors hover:border-[#9a6a35] hover:bg-[#9a6a35] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#7c5226]"
            >
              <PhoneCall className="size-3.5" aria-hidden="true" />
              Call 15100 (Free Legal Aid)
            </a>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => setShowAdvocates((value) => !value)}
              aria-pressed={showAdvocates}
              className="min-h-10 text-xs sm:min-h-9"
            >
              <Scale className="mr-1 size-3.5 text-[#9a6a35]" aria-hidden="true" />
              Connect to an advocate urgently
            </Button>
          </div>

          {answer.citations.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 border-t border-[#e2d5c1]/60 pt-3">
              <span className="text-[10px] font-medium uppercase tracking-[0.1em] text-[#85725f]">
                Statutory source
              </span>
              {answer.citations.map((citation) => (
                <CitationChip key={citation.id} citation={citation} />
              ))}
            </div>
          )}
        </div>

        {showAdvocates && (
          <AdvocateMatchInline
            onClose={() => setShowAdvocates(false)}
            onRequestConsultation={(name) => {
              onRequestConsultation(name);
              onShowToast(`Urgent consultation request transmitted to ${name}`);
            }}
          />
        )}

        {followUpRow}
      </div>
    );
  }

  // -------------------------------------------------------------------------
  // STANDARD ANSWER — no bubble, no card: quiet sections on the cream page.
  // -------------------------------------------------------------------------
  return (
    <div className={cn(styles.fadeIn, "space-y-5")}>
      {/* SUMMARY — brand mark and variant badge share the first line. */}
      <section className="space-y-2">
        <div className="flex flex-wrap items-center gap-2.5">
          <BrandMark />
          <SectionLabel>SUMMARY</SectionLabel>
          <DecisionBadge variant={answer.decisionBadge} className="ml-auto" />
        </div>
        <p className="font-serif text-[17px] font-normal leading-snug text-[#2a1c12] sm:text-[19px]">
          {answer.oneLineSummary}
        </p>
        {answer.isLowConfidence && (
          <p className="flex items-start gap-1.5 text-xs leading-relaxed text-[#85725f]">
            <HelpCircle
              className="mt-px size-3.5 shrink-0 text-[#9a6a35]"
              aria-hidden="true"
            />
            <span className="min-w-0 break-words">
              <span className="font-medium text-[#5b4a3b]">
                I&apos;m not fully sure about this one.
              </span>{" "}
              {answer.confidenceReason} Marked as Advocate advised — we recommend organising your
              facts into a case brief below.
            </span>
          </p>
        )}
      </section>

      {/* EXPLANATION */}
      {answer.explanation.length > 0 && (
        <section className="space-y-2">
          <SectionLabel>EXPLANATION</SectionLabel>
          <div className="space-y-2 text-[13px] leading-relaxed text-[#5b4a3b]">
            {answer.explanation.map((paragraph, index) => (
              <p key={index} className="min-w-0 break-words">
                {paragraph}
              </p>
            ))}
          </div>
        </section>
      )}

      {/* NEXT STEPS */}
      {answer.nextSteps.length > 0 && (
        <section className="space-y-2">
          <SectionLabel>NEXT STEPS</SectionLabel>
          <ol className="space-y-2 text-[13px] text-[#2a1c12]">
            {answer.nextSteps.map((step) => (
              <li key={step.step} className="flex items-start gap-2.5">
                <span className="mt-0.5 grid size-5 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/60 font-mono text-[10.5px] font-medium text-[#2a1c12]">
                  {step.step}
                </span>
                <div className="min-w-0 flex-1 leading-relaxed">
                  <span className="break-words">{step.text}</span>
                  {step.isFortyEightHours && (
                    <span className="ml-2 inline-flex items-center gap-1 rounded-[2px] border border-[#e2d5c1] bg-[#fff8e7] px-2 py-0.5 text-[10px] font-medium uppercase tracking-[0.08em] text-[#b54708]">
                      <Clock className="size-2.5" aria-hidden="true" />
                      Do this in 48 hours
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ol>
        </section>
      )}

      {/* DEADLINES — statutory calculator with its required basis note. */}
      {activeDeadlines && (
        <section className="space-y-2">
          <SectionLabel>DEADLINES</SectionLabel>
          <div className="space-y-3 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-4">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#e2d5c1]/60 pb-2">
              <div className="flex items-center gap-2">
                <CalendarClock className="size-4 text-[#b54708]" aria-hidden="true" />
                <span className="text-xs font-medium text-[#2a1c12]">
                  Section 138 statutory limitation calculator
                </span>
              </div>
              <Button
                size="sm"
                variant="primary"
                onClick={() => {
                  onAddToDeadlines(
                    "Sec 138 Legal Notice Due",
                    activeDeadlines.noticeDueDate
                  );
                  onShowToast(
                    `Added to Court Deadlines: Notice due ${activeDeadlines.noticeDueDate}`
                  );
                }}
                className="min-h-10 px-2.5 text-[11px] sm:min-h-8"
              >
                Add to Court Deadlines
              </Button>
            </div>

            <div className="flex flex-wrap items-center gap-3 text-xs">
              <label
                htmlFor={`memoDateInput-${answer.id}`}
                className="font-medium text-[#5b4a3b]"
              >
                Bank memo date:
              </label>
              <input
                id={`memoDateInput-${answer.id}`}
                type="date"
                value={memoDate}
                onChange={(event) => setMemoDate(event.target.value)}
                className="h-10 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-2.5 font-mono text-xs text-[#2a1c12] focus:border-[#9a6a35] focus:outline-none focus:ring-1 focus:ring-[#9a6a35] sm:h-8"
              />
            </div>

            <div className="grid grid-cols-1 gap-2 pt-1 text-xs sm:grid-cols-3">
              {[
                ["1. Notice Due (+30 days)", activeDeadlines.noticeDueDate],
                ["2. Payment Window (+15 days)", activeDeadlines.paymentWindowEndDate],
                ["3. Complaint Due (+30 days)", activeDeadlines.complaintDueDate],
              ].map(([label, date]) => (
                <div
                  key={label}
                  className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-2.5"
                >
                  <span className="block text-[10px] font-medium uppercase tracking-[0.08em] text-[#85725f]">
                    {label}
                  </span>
                  <span className="mt-0.5 block break-words font-mono text-xs font-medium text-[#2a1c12]">
                    {date}
                  </span>
                </div>
              ))}
            </div>

            <p className="text-[10.5px] leading-relaxed text-[#85725f]">
              {activeDeadlines.statutoryNote} Requires review by an empanelled advocate.
            </p>
          </div>
        </section>
      )}

      {/* SOURCES — collapsed by default. */}
      <SourcesAccordion
        citations={answer.citations}
        reviewedDate={answer.sourcesReviewedDate}
        open={sourcesOpen}
        onToggle={() => setSourcesOpen((value) => !value)}
      />

      {/* ACTIONS */}
      <ActionBar
        onSaveToCases={() => {
          onSaveToCases(answer.decisionBadge, answer.oneLineSummary);
          onShowToast("Saved matter summary to My Cases");
        }}
        briefActive={showCaseBrief}
        onToggleBrief={() => {
          setShowCaseBrief((value) => !value);
          setShowAdvocates(false);
        }}
        advocatesActive={showAdvocates}
        onToggleAdvocates={() => {
          setShowAdvocates((value) => !value);
          setShowCaseBrief(false);
        }}
        copied={copied}
        onCopy={handleCopy}
        feedback={feedback}
        onFeedback={(value) => {
          setFeedback(value);
          onShowToast(
            value === "up" ? "Feedback recorded: Helpful" : "Feedback recorded: Needs revision"
          );
        }}
        flagActive={showFlagInput}
        onToggleFlag={() => setShowFlagInput((value) => !value)}
      />

      {showFlagInput && (
        <FlagErrorDialog
          onClose={() => setShowFlagInput(false)}
          onSubmitFlag={() => {
            setShowFlagInput(false);
            onShowToast("Sent to reviewing advocates");
          }}
        />
      )}

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

      {showAdvocates && (
        <AdvocateMatchInline
          onClose={() => setShowAdvocates(false)}
          onRequestConsultation={(name) => {
            onRequestConsultation(name);
            onShowToast(`Consultation request sent to ${name}`);
          }}
        />
      )}

      {/* FOLLOW-UPS — up to three quiet pills. */}
      {followUpRow}
    </div>
  );
}
