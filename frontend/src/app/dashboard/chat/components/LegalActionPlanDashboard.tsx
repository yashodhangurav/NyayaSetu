"use client";

import React, { useState } from "react";
import {
  ChevronDown,
  CheckCircle2,
  Circle,
  Clock,
  AlertTriangle,
  FileText,
  Scale,
  MapPin,
  Briefcase,
  ListChecks,
} from "lucide-react";
import type {
  LegalActionPlanItem,
  ActionStepItem,
  CaseSummaryItem,
} from "@/services/dashboard/chat-assistant";
import { Badge, Button } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";

interface LegalActionPlanDashboardProps {
  plan: LegalActionPlanItem;
  caseSummary?: CaseSummaryItem;
  onToggleStep?: (stepId: string, completed: boolean) => void;
  onDraftDocument?: (assistanceAction: string) => void;
  onFindAdvocate?: () => void;
  onFollowUpClick?: (prompt: string) => void;
}

const PRIORITY_STYLES: Record<ActionStepItem["priority"], { badge: string; dot: string }> = {
  URGENT: { badge: "text-[#c0392b] bg-[#fdf2f2] border-[#c0392b]/40", dot: "bg-[#c0392b]" },
  HIGH: { badge: "text-[#b54708] bg-[#fff9e8] border-[#f0d080]", dot: "bg-[#b54708]" },
  MEDIUM: { badge: "text-[#493727] bg-[#f4efe6] border-[#d9cebd]", dot: "bg-[#9a6a35]" },
  LOW: { badge: "text-[#5b4a3b] bg-[#f4efe6] border-[#e2d5c1]", dot: "bg-[#c5a578]" },
};

function StepCard({
  step,
  index,
  total,
  onToggle,
  onDraftDocument,
}: {
  step: ActionStepItem;
  index: number;
  total: number;
  onToggle?: (id: string, completed: boolean) => void;
  onDraftDocument?: (action: string) => void;
}) {
  const [expanded, setExpanded] = useState(index === 0);
  const isCompleted = step.status === "completed";
  const style = PRIORITY_STYLES[step.priority];

  return (
    <div
      className={cn(
        "rounded-[2px] border transition-colors",
        isCompleted
          ? "border-[#2e7d32]/30 bg-[#f0faf0]"
          : "border-[#d9cebd] bg-white/60"
      )}
    >
      {/* Step header */}
      <div className="flex items-start gap-3 p-3.5 sm:p-4">
        {/* Checkbox */}
        <button
          type="button"
          onClick={() => onToggle?.(step.id, !isCompleted)}
          aria-label={isCompleted ? "Mark as pending" : "Mark as completed"}
          className="mt-0.5 shrink-0 cursor-pointer"
        >
          {isCompleted ? (
            <CheckCircle2 className="size-5 text-[#2e7d32]" aria-hidden="true" />
          ) : (
            <Circle className="size-5 text-[#b89f81]" aria-hidden="true" />
          )}
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono text-xs text-[#816541]">
              Step {index + 1}/{total}
            </span>
            <span
              className={cn(
                "inline-flex items-center rounded-[2px] border px-2 py-0.5 font-sans text-[11px] font-semibold uppercase tracking-wide",
                style.badge
              )}
            >
              {step.priority}
            </span>
            {step.deadline && (
              <span className="inline-flex items-center gap-1 font-sans text-[11px] text-[#b54708]">
                <Clock className="size-3" aria-hidden="true" />
                {step.deadline}
              </span>
            )}
          </div>
          <h4
            className={cn(
              "mt-1 font-serif text-[16px] leading-snug",
              isCompleted ? "text-[#5b7a5b] line-through" : "text-[#2a1c12]"
            )}
          >
            {step.title}
          </h4>
        </div>

        {/* Expand toggle */}
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="shrink-0 cursor-pointer p-1 text-[#816541] hover:text-[#2a1c12]"
          aria-label={expanded ? "Collapse step" : "Expand step"}
        >
          <ChevronDown
            className={cn("size-4 transition-transform", expanded && "rotate-180")}
            aria-hidden="true"
          />
        </button>
      </div>

      {/* Expanded details */}
      {expanded && (
        <div className="border-t border-[#e2d5c1] px-4 pb-4 pt-3 space-y-3">
          <p className="font-sans text-sm text-[#4f4033] leading-relaxed">{step.description}</p>

          {step.relevant_authority && (
            <div className="flex items-start gap-2 font-sans text-sm text-[#5b4a3b]">
              <MapPin className="mt-0.5 size-4 shrink-0 text-[#9a6a35]" aria-hidden="true" />
              <span>
                <strong>Authority: </strong>{step.relevant_authority}
              </span>
            </div>
          )}

          {step.required_documents.length > 0 && (
            <div>
              <p className="font-sans text-xs font-semibold uppercase tracking-widest text-[#816541] mb-1.5">
                Required documents
              </p>
              <ul className="space-y-1">
                {step.required_documents.map((doc, i) => (
                  <li key={i} className="flex items-start gap-2 font-sans text-sm text-[#4f4033]">
                    <FileText className="mt-0.5 size-3.5 shrink-0 text-[#9a6a35]" aria-hidden="true" />
                    {doc}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {step.assistance_action && onDraftDocument && (
            <button
              type="button"
              onClick={() => onDraftDocument(step.assistance_action!)}
              className="inline-flex h-8 items-center gap-1.5 rounded-[2px] border border-[#d9cebd] bg-[#f4efe6] px-3 font-sans text-xs text-[#5b4a3b] hover:border-[#9a6a35] hover:text-[#2a1c12] transition-colors cursor-pointer"
            >
              <FileText className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
              {step.assistance_action === "draft_complaint"
                ? "Draft complaint →"
                : step.assistance_action === "find_advocate"
                  ? "Find advocate →"
                  : step.assistance_action === "legal_aid"
                    ? "Get free legal aid →"
                    : `${step.assistance_action} →`}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export function LegalActionPlanDashboard({
  plan,
  caseSummary,
  onToggleStep,
  onDraftDocument,
  onFindAdvocate,
  onFollowUpClick,
}: LegalActionPlanDashboardProps) {
  const [localSteps, setLocalSteps] = useState<ActionStepItem[]>(plan.steps);

  const handleToggle = (stepId: string, completed: boolean) => {
    setLocalSteps((prev) =>
      prev.map((s) => (s.id === stepId ? { ...s, status: completed ? "completed" : "pending" } : s))
    );
    onToggleStep?.(stepId, completed);
  };

  const completedCount = localSteps.filter((s) => s.status === "completed").length;
  const totalCount = localSteps.length;

  return (
    <div className="space-y-4 animate-in-up">
      <div className="min-w-0 rounded-[2px] border border-[#d9cebd] border-t-[3px] border-t-[#966931] bg-[#fffaf2] p-5 text-[#2a1c12] sm:p-6">
        {/* Header */}
        <div className="border-b border-[#ded4c5] pb-4 space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <ListChecks className="size-5 text-[#9a6a35]" aria-hidden="true" />
              <h3 className="font-serif text-[22px] font-normal text-[#2a1c12]">
                Your Legal Roadmap
              </h3>
            </div>
            <span className="font-mono text-xs text-[#816541]">
              {completedCount}/{totalCount} completed
            </span>
          </div>

          {/* Case meta */}
          <div className="flex flex-wrap gap-3 text-xs font-sans text-[#5b4a3b]">
            {plan.legal_domain && (
              <span className="flex items-center gap-1">
                <Briefcase className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
                {plan.legal_domain}
              </span>
            )}
            {plan.jurisdiction && (
              <span className="flex items-center gap-1">
                <MapPin className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
                {plan.jurisdiction}
              </span>
            )}
            {plan.dispute_category && (
              <span className="flex items-center gap-1">
                <Scale className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
                {plan.dispute_category}
              </span>
            )}
          </div>

          {/* Progress bar */}
          <div className="h-1.5 w-full overflow-hidden rounded-[1px] bg-[#e6dcce]">
            <div
              className="h-full bg-[#2e7d32] transition-all duration-500"
              style={{ width: `${(completedCount / Math.max(totalCount, 1)) * 100}%` }}
            />
          </div>
        </div>

        {/* Case summary */}
        {plan.case_summary && (
          <div className="mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] px-4 py-3">
            <p className="font-sans text-xs font-semibold uppercase tracking-widest text-[#816541] mb-1">
              Case summary
            </p>
            <p className="font-sans text-sm text-[#4f4033] leading-relaxed">{plan.case_summary}</p>
            {plan.possible_remedy && (
              <p className="mt-1.5 font-sans text-sm font-medium text-[#2a1c12]">
                Possible remedy: {plan.possible_remedy}
              </p>
            )}
          </div>
        )}

        {/* Recommended first action */}
        {plan.recommended_first_action && (
          <div className="mt-4 flex items-start gap-2 rounded-[2px] border border-[#f0d080] bg-[#fff9e8] px-4 py-3">
            <AlertTriangle className="mt-0.5 size-4 shrink-0 text-[#b54708]" aria-hidden="true" />
            <div>
              <p className="font-sans text-xs font-semibold text-[#7c5000]">Start here:</p>
              <p className="font-sans text-sm text-[#4f4033]">{plan.recommended_first_action}</p>
            </div>
          </div>
        )}

        {/* Steps */}
        <div className="mt-5 space-y-2">
          <p className="font-sans text-xs font-semibold uppercase tracking-widest text-[#816541] mb-3">
            Action steps
          </p>
          {localSteps.map((step, idx) => (
            <StepCard
              key={step.id}
              step={step}
              index={idx}
              total={totalCount}
              onToggle={handleToggle}
              onDraftDocument={onDraftDocument}
            />
          ))}
        </div>

        {/* Required documents sidebar summary */}
        {plan.required_documents.length > 0 && (
          <div className="mt-5 rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] px-4 py-3">
            <p className="font-sans text-xs font-semibold uppercase tracking-widest text-[#816541] mb-2">
              Documents you will need
            </p>
            <ul className="grid gap-1 sm:grid-cols-2">
              {plan.required_documents.map((doc, idx) => (
                <li key={idx} className="flex items-start gap-2 font-sans text-sm text-[#4f4033]">
                  <FileText className="mt-0.5 size-3.5 shrink-0 text-[#9a6a35]" aria-hidden="true" />
                  {doc}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Alternative options */}
        {plan.alternative_options.length > 0 && (
          <details className="mt-4 group border-t border-[#ded4c5]">
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4 py-3.5 font-sans text-[14px] font-medium text-[#493727] outline-offset-2 hover:text-[#855a2c] [&::-webkit-details-marker]:hidden">
              Alternative options ({plan.alternative_options.length})
              <ChevronDown className="size-4 shrink-0 text-[#816541] transition-transform group-open:rotate-180" aria-hidden="true" />
            </summary>
            <ul className="space-y-2 pb-4">
              {plan.alternative_options.map((opt, idx) => (
                <li key={idx} className="flex items-start gap-2 font-sans text-sm text-[#4f4033]">
                  <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-[#9a6a35]" aria-hidden="true" />
                  {opt}
                </li>
              ))}
            </ul>
          </details>
        )}

        {/* CTA row */}
        <div className="mt-5 flex flex-wrap gap-2 border-t border-[#ded4c5] pt-4">
          {onFindAdvocate && (
            <Button
              size="sm"
              variant="secondary"
              onClick={onFindAdvocate}
              className="h-9 text-xs"
            >
              <Scale className="size-3.5 mr-1.5 text-[#9a6a35]" aria-hidden="true" />
              Find an Advocate
            </Button>
          )}
          {onFollowUpClick && (
            <>
              <button
                type="button"
                onClick={() => onFollowUpClick(`What documents do I need for ${plan.dispute_category || "my case"}?`)}
                className="inline-flex h-9 items-center rounded-[2px] border border-[#d9cebd] bg-white/70 px-3 font-sans text-xs text-[#5b4a3b] hover:border-[#9a6a35] hover:text-[#2a1c12] transition-colors cursor-pointer"
              >
                What documents do I need?
              </button>
              <button
                type="button"
                onClick={() => onFollowUpClick(`What are the court fees for ${plan.dispute_category || "this case"}?`)}
                className="inline-flex h-9 items-center rounded-[2px] border border-[#d9cebd] bg-white/70 px-3 font-sans text-xs text-[#5b4a3b] hover:border-[#9a6a35] hover:text-[#2a1c12] transition-colors cursor-pointer"
              >
                What are the court fees?
              </button>
            </>
          )}
        </div>

        {/* Fees / costs */}
        {plan.verified_fees_or_costs && (
          <p className="mt-3 font-sans text-xs text-[#5b4a3b]">
            Estimated costs: {plan.verified_fees_or_costs}
          </p>
        )}

        <p className="mt-3 font-sans text-[11px] leading-relaxed text-[#8c7b6a] border-t border-[#e2d5c1] pt-3">
          NyayaSetu provides AI-assisted information only. This roadmap should be reviewed by a qualified advocate before you take any action. NyayaSetu does not provide legal advice.
        </p>
      </div>
    </div>
  );
}
