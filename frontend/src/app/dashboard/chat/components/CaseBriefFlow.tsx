"use client";

import React, { useEffect, useState } from "react";
import { ArrowRight, Check, FileText, Share2, BookmarkCheck, Shield, X } from "lucide-react";
import { Button } from "@/components/dashboard/ui";
import type { CaseBriefData } from "@/services/dashboard/chat-assistant";
import { DefinitionList } from "./primitives/DefinitionList";
import { BriefCardSkeleton } from "./primitives/Skeletons";
import { cn } from "@/lib/utils";
import styles from "../chat.module.css";

interface CaseBriefFlowProps {
  onClose: () => void;
  onSaveToCases: (brief: CaseBriefData) => void;
  onShareWithAdvocate: (brief: CaseBriefData) => void;
  /** Reserved for a real brief-generation fetch; never simulated here. */
  loading?: boolean;
}

const QUESTIONS = [
  {
    key: "facts",
    question: "1. What happened?",
    sub: "Describe the core incident or dispute clearly.",
    chips: [
      "Security deposit withheld past 30 days",
      "Commercial cheque dishonoured by bank",
      "Unilateral contract termination without dues",
      "Received advocate statutory demand notice",
    ],
  },
  {
    key: "timeline",
    question: "2. When did this take place?",
    sub: "Approximate dates help determine statutory limitation.",
    chips: [
      "Within the last 7 calendar days",
      "Between 15 to 30 days ago",
      "1 to 3 months ago",
      "Over 6 months ago",
    ],
  },
  {
    key: "parties",
    question: "3. Who is involved?",
    sub: "Identify the counter-party or organization.",
    chips: [
      "Individual landlord / House owner",
      "Commercial vendor / Enterprise client",
      "Employer / Corporate HR department",
      "Family member / Coparcener",
    ],
  },
  {
    key: "documents",
    question: "4. What documents do you currently hold?",
    sub: "Documentary records establish court admissibility.",
    chips: [
      "Signed Lease agreement & bank transfers",
      "Original cheque & bank return memo",
      "WhatsApp & email correspondence",
      "Work contract & salary pay slips",
    ],
  },
  {
    key: "outcome",
    question: "5. What outcome do you want to achieve?",
    sub: "Your preferred legal or negotiated resolution.",
    chips: [
      "Full monetary refund with interest",
      "Formal reply to legal notice",
      "Criminal prosecution under Sec 138",
      "Amicable mediation & settlement",
    ],
  },
];

const closeButton =
  "grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-8";

export function CaseBriefFlow({
  onClose,
  onSaveToCases,
  onShareWithAdvocate,
  loading = false,
}: CaseBriefFlowProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({
    facts: "",
    timeline: "",
    parties: "",
    documents: "",
    outcome: "",
  });
  const [customInput, setCustomInput] = useState("");
  const [isCompleted, setIsCompleted] = useState(false);
  const [showConsentModal, setShowConsentModal] = useState(false);

  const stepDef = QUESTIONS[currentStep];

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      if (showConsentModal) setShowConsentModal(false);
      else onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [showConsentModal, onClose]);

  const handleSelectChip = (chip: string) => {
    const key = stepDef.key;
    setAnswers({ ...answers, [key]: chip });
    setCustomInput("");

    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep((step) => step + 1);
    } else {
      setIsCompleted(true);
    }
  };

  const handleCustomSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!customInput.trim()) return;
    const key = stepDef.key;
    setAnswers({ ...answers, [key]: customInput.trim() });
    setCustomInput("");

    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep((step) => step + 1);
    } else {
      setIsCompleted(true);
    }
  };

  // Generated Case Brief Data
  const briefData: CaseBriefData = {
    facts: answers.facts || "Security deposit withheld past 30 days without handover inspection report.",
    timeline: answers.timeline || "Within the last 30 calendar days.",
    parties: answers.parties || "Tenancy lessor / Landlord.",
    documents: [
      answers.documents || "Signed Lease Agreement, bank transfer ledger, key return receipt",
    ],
    relevantSections: [
      "Transfer of Property Act, 1882 · Sec 108",
      "Karnataka Rent Act, 1999 · Sec 27",
    ],
    probableForum: "Court of Small Causes / Rent Controller (Belagavi Jurisdiction)",
    deadline: "Notice reply due within 15 days of formal demand receipt",
  };

  if (loading) return <BriefCardSkeleton />;

  if (isCompleted) {
    return (
      <div className={cn(styles.fadeIn, "mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-[0_1px_2px_rgba(42,28,18,0.04)]")}>
        <div className="flex items-start justify-between gap-3 border-b border-[#e2d5c1]/70 pb-3">
          <div className="flex min-w-0 items-start gap-2.5">
            <span className="grid size-7 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
              <FileText className="size-4" aria-hidden="true" />
            </span>
            <div className="min-w-0">
              <h3 className="font-serif text-[17px] font-normal leading-snug text-[#2a1c12]">
                Formal Case Matter Brief
              </h3>
              <p className="mt-1 break-words text-[11px] leading-relaxed text-[#85725f]">
                Generated from citizen factual intake · Belagavi District Court Jurisdiction
              </p>
            </div>
          </div>
          <button type="button" onClick={onClose} aria-label="Close case brief" className={closeButton}>
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>

        <div className="mt-4">
          <DefinitionList
            items={[
              { label: "Core facts", value: briefData.facts },
              { label: "Timeline & limitation", value: briefData.timeline },
              { label: "Deadline", value: briefData.deadline, mono: true, important: true },
              { label: "Parties involved", value: briefData.parties },
              { label: "Probable forum", value: briefData.probableForum },
            ]}
          />
        </div>

        <div className="mt-3 border-t border-[#e2d5c1]/70 pt-3">
          <DefinitionList
            items={[
              { label: "Preserved documents", value: briefData.documents.join("; ") },
              {
                label: "Statutory provisions",
                value: (
                  <span className="flex flex-wrap gap-1.5">
                    {briefData.relevantSections.map((section) => (
                      <span
                        key={section}
                        className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-2 py-0.5 font-mono text-[11px] text-[#2a1c12]"
                      >
                        {section}
                      </span>
                    ))}
                  </span>
                ),
              },
            ]}
          />
        </div>

        <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-[#e2d5c1]/70 pt-3">
          <div className="flex flex-wrap items-center gap-2">
            <Button
              size="sm"
              variant="primary"
              onClick={() => setShowConsentModal(true)}
              className="min-h-10 text-xs sm:min-h-9"
            >
              <Share2 className="mr-1 size-3.5" aria-hidden="true" />
              Share with advocate
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => onSaveToCases(briefData)}
              className="min-h-10 text-xs sm:min-h-9"
            >
              <BookmarkCheck className="mr-1 size-3.5 text-[#9a6a35]" aria-hidden="true" />
              Save to My Cases
            </Button>
          </div>
          <span className="flex items-center gap-1 text-[11px] text-[#85725f]">
            <Shield className="size-3 text-[#2e7d32]" aria-hidden="true" />
            DPDP Act, 2023 encrypted dossier
          </span>
        </div>

        {showConsentModal && (
          <div className="fixed inset-0 z-60 grid place-items-center bg-[#24180f]/60 p-4 backdrop-blur-xs animate-fade">
            <div className="w-full max-w-md space-y-3.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-pop animate-in-up">
              <h4 className="font-serif text-[18px] font-normal text-[#2a1c12]">
                Statutory consent required
              </h4>
              <p className="text-xs leading-relaxed text-[#5b4a3b]">
                Under the Digital Personal Data Protection Act, 2023 (DPDP) and Bar Council of India
                standards, your case brief will only be transmitted to verified advocates you
                specifically authorise.
              </p>
              <div className="space-y-1 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 p-3 text-[11.5px] leading-relaxed text-[#2a1c12]">
                <p>· Scope: transmit case brief to an empanelled advocate for preliminary evaluation.</p>
                <p>· Retention: advice-only privilege; revocable anytime in privacy settings.</p>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <Button size="sm" variant="ghost" onClick={() => setShowConsentModal(false)} className="min-h-10 sm:min-h-9">
                  Cancel
                </Button>
                <Button
                  size="sm"
                  variant="primary"
                  onClick={() => {
                    setShowConsentModal(false);
                    onShareWithAdvocate(briefData);
                  }}
                  className="min-h-10 sm:min-h-9"
                >
                  <Check className="mr-1 size-3.5" aria-hidden="true" />
                  Grant consent & transmit
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={cn(styles.fadeIn, "mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4.5 shadow-[0_1px_2px_rgba(42,28,18,0.04)] sm:p-5")}>
      <div className="flex items-start justify-between gap-3 border-b border-[#e2d5c1]/70 pb-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-medium uppercase tracking-[0.1em] text-[#9a6a35]">
              Question {currentStep + 1} of 5
            </span>
            <span className="text-[11px] text-[#85725f]">· Case brief questionnaire</span>
          </div>
          <h3 className="mt-0.5 font-serif text-[17px] font-normal leading-snug text-[#2a1c12]">
            {stepDef.question}
          </h3>
          <p className="mt-0.5 text-[11.5px] leading-relaxed text-[#5b4a3b]">{stepDef.sub}</p>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Cancel case brief questionnaire"
          className={closeButton}
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      </div>

      <div className="mt-3.5 space-y-2">
        <p className="text-[11px] font-medium uppercase tracking-[0.08em] text-[#85725f]">
          Quick responses (select one to proceed)
        </p>
        <div className="flex flex-wrap gap-2">
          {stepDef.chips.map((chip) => (
            <button
              key={chip}
              type="button"
              onClick={() => handleSelectChip(chip)}
              className="min-h-10 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/35 px-3 py-1.5 text-left text-xs text-[#2a1c12] transition-colors hover:border-[#9a6a35] hover:bg-[#ebe1d1]/70 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:min-h-8"
            >
              {chip}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleCustomSubmit} className="mt-3.5 border-t border-[#e2d5c1]/60 pt-3">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={customInput}
            onChange={(event) => setCustomInput(event.target.value)}
            placeholder="Or type custom details here..."
            className="h-10 min-w-0 flex-1 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 text-xs text-[#2a1c12] placeholder:text-[#85725f]/60 focus:border-[#9a6a35] focus:outline-none focus:ring-1 focus:ring-[#9a6a35] sm:h-9"
          />
          <Button
            type="submit"
            size="sm"
            variant="primary"
            disabled={!customInput.trim()}
            className="min-h-10 px-3 text-xs sm:min-h-9"
          >
            Next <ArrowRight className="ml-1 size-3.5" aria-hidden="true" />
          </Button>
        </div>
      </form>
    </div>
  );
}
