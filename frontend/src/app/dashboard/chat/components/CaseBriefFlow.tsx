"use client";

import React, { useState } from "react";
import { FileText, ArrowRight, Check, X, Shield, BookmarkCheck, Share2 } from "lucide-react";
import { Button } from "@/components/dashboard/ui";
import type { CaseBriefData } from "@/services/dashboard/chat-assistant";

interface CaseBriefFlowProps {
  onClose: () => void;
  onSaveToCases: (brief: CaseBriefData) => void;
  onShareWithAdvocate: (brief: CaseBriefData) => void;
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

export function CaseBriefFlow({
  onClose,
  onSaveToCases,
  onShareWithAdvocate,
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

  const handleSelectChip = (chip: string) => {
    const key = stepDef.key;
    const nextAnswers = { ...answers, [key]: chip };
    setAnswers(nextAnswers);
    setCustomInput("");

    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep((s) => s + 1);
    } else {
      setIsCompleted(true);
    }
  };

  const handleCustomSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customInput.trim()) return;
    const key = stepDef.key;
    const nextAnswers = { ...answers, [key]: customInput.trim() };
    setAnswers(nextAnswers);
    setCustomInput("");

    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep((s) => s + 1);
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

  if (isCompleted) {
    return (
      <div className="mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-xs animate-in-up">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#e2d5c1]/70 pb-3">
          <div className="flex items-center gap-2">
            <span className="grid size-7 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
              <FileText className="size-4" aria-hidden="true" />
            </span>
            <div>
              <h3 className="font-serif text-[17px] font-normal text-[#2a1c12] leading-none">
                Formal Case Matter Brief
              </h3>
              <p className="mt-1 text-[11px] text-[#85725f]">
                Generated from citizen factual intake · Belagavi District Court Jurisdiction
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close Case Brief"
            className="rounded-[2px] p-1 text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>

        {/* Structured Grid */}
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-xs">
          <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3 space-y-1">
            <span className="text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
              Core Facts
            </span>
            <p className="text-[#2a1c12] leading-relaxed font-medium">{briefData.facts}</p>
          </div>

          <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3 space-y-1">
            <span className="text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
              Timeline & Limitation
            </span>
            <p className="text-[#2a1c12] leading-relaxed font-medium">{briefData.timeline}</p>
            <p className="text-[11px] font-mono text-[#b54708] pt-1">
              Limitation deadline: {briefData.deadline}
            </p>
          </div>

          <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3 space-y-1">
            <span className="text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
              Parties Involved
            </span>
            <p className="text-[#2a1c12] leading-relaxed font-medium">{briefData.parties}</p>
          </div>

          <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3 space-y-1">
            <span className="text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
              Probable Court Forum
            </span>
            <p className="text-[#2a1c12] leading-relaxed font-medium">{briefData.probableForum}</p>
          </div>
        </div>

        {/* Documents & Sections */}
        <div className="mt-3.5 space-y-2 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/20 p-3 text-xs">
          <div>
            <span className="text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
              Preserved Evidentiary Documents
            </span>
            <p className="text-[#2a1c12] leading-relaxed mt-0.5">
              {briefData.documents.join("; ")}
            </p>
          </div>
          <div className="pt-1.5 border-t border-[#e2d5c1]/60">
            <span className="text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
              Applicable Statutory Provisions
            </span>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {briefData.relevantSections.map((sec) => (
                <span
                  key={sec}
                  className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-2 py-0.5 font-mono text-[11px] text-[#2a1c12]"
                >
                  {sec}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-4 pt-3 border-t border-[#e2d5c1]/70 flex flex-wrap items-center justify-between gap-2.5">
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="primary"
              onClick={() => setShowConsentModal(true)}
              className="text-xs"
            >
              <Share2 className="size-3.5 mr-1" aria-hidden="true" />
              Share with advocate (asks consent)
            </Button>
            <Button
              size="sm"
              variant="secondary"
              onClick={() => onSaveToCases(briefData)}
              className="text-xs"
            >
              <BookmarkCheck className="size-3.5 mr-1 text-[#9a6a35]" aria-hidden="true" />
              Save to My Cases
            </Button>
          </div>
          <span className="text-[11px] text-[#85725f] flex items-center gap-1">
            <Shield className="size-3 text-[#2e7d32]" />
            DPDP Act, 2023 Encrypted Dossier
          </span>
        </div>

        {/* Consent Modal */}
        {showConsentModal && (
          <div className="fixed inset-0 z-60 grid place-items-center bg-[#24180f]/60 p-4 backdrop-blur-xs animate-fade">
            <div className="w-full max-w-md rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-pop animate-in-up space-y-3.5">
              <h4 className="font-serif text-[18px] font-normal text-[#2a1c12]">
                Statutory Consent Required
              </h4>
              <p className="text-xs text-[#5b4a3b] leading-relaxed">
                Under the Digital Personal Data Protection Act, 2023 (DPDP) and Bar Council of India standards, your case brief will only be transmitted to verified advocates you specifically authorize.
              </p>
              <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 p-3 text-[11.5px] text-[#2a1c12] space-y-1">
                <p className="font-medium">• Scope: Transmit Case Brief to empanelled advocate for preliminary evaluation.</p>
                <p className="font-medium">• Retention: Advise-only privilege; revocable anytime in privacy settings.</p>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setShowConsentModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  size="sm"
                  variant="primary"
                  onClick={() => {
                    setShowConsentModal(false);
                    onShareWithAdvocate(briefData);
                  }}
                >
                  <Check className="size-3.5 mr-1" />
                  Grant Consent & Transmit
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4.5 sm:p-5 shadow-xs animate-in-up">
      {/* Questionnaire Header */}
      <div className="flex items-center justify-between border-b border-[#e2d5c1]/70 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-sans uppercase tracking-[0.1em] font-semibold text-[#9a6a35]">
              Question {currentStep + 1} of 5
            </span>
            <span className="text-[11px] text-[#85725f]">· Case Brief Questionnaire</span>
          </div>
          <h3 className="font-serif text-[17px] font-normal text-[#2a1c12] mt-0.5">
            {stepDef.question}
          </h3>
          <p className="text-[11.5px] text-[#5b4a3b] mt-0.5">{stepDef.sub}</p>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Cancel case brief questionnaire"
          className="rounded-[2px] p-1 text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      </div>

      {/* Quick Reply Chips */}
      <div className="mt-3.5 space-y-2">
        <p className="text-[11px] font-sans uppercase tracking-[0.08em] font-medium text-[#85725f]">
          Quick responses (select one to proceed):
        </p>
        <div className="flex flex-wrap gap-2">
          {stepDef.chips.map((chip) => (
            <button
              key={chip}
              type="button"
              onClick={() => handleSelectChip(chip)}
              className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/35 px-3 py-1.5 text-xs text-[#2a1c12] hover:border-[#9a6a35] hover:bg-[#ebe1d1]/70 transition-colors text-left cursor-pointer"
            >
              {chip}
            </button>
          ))}
        </div>
      </div>

      {/* Free Text Input */}
      <form onSubmit={handleCustomSubmit} className="mt-3.5 pt-3 border-t border-[#e2d5c1]/60">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            placeholder="Or type custom details here..."
            className="flex-1 h-9 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 text-xs text-[#2a1c12] placeholder:text-[#85725f]/60 focus:outline-none focus:border-[#9a6a35] focus:ring-1 focus:ring-[#9a6a35]"
          />
          <Button
            type="submit"
            size="sm"
            variant="primary"
            disabled={!customInput.trim()}
            className="h-9 px-3 text-xs"
          >
            Next <ArrowRight className="size-3.5 ml-1" />
          </Button>
        </div>
      </form>
    </div>
  );
}
