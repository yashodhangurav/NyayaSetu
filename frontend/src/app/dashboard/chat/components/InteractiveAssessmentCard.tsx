"use client";

import React, { useState } from "react";
import { HelpCircle, ChevronRight, CheckCircle2, ArrowRight } from "lucide-react";
import type { AssessmentQuestionItem, CaseSummaryItem } from "@/services/dashboard/chat-assistant";
import { Badge, Button } from "@/components/dashboard/ui";

interface InteractiveAssessmentCardProps {
  questions: AssessmentQuestionItem[];
  caseSummary?: CaseSummaryItem;
  onSubmitAnswers: (answers: Record<string, any>) => void;
  onSkip: () => void;
  isSubmitting?: boolean;
}

export function InteractiveAssessmentCard({
  questions,
  caseSummary,
  onSubmitAnswers,
  onSkip,
  isSubmitting = false,
}: InteractiveAssessmentCardProps) {
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [activeStep, setActiveStep] = useState(0);

  if (!questions || questions.length === 0) return null;

  const currentQ = questions[activeStep] || questions[0];
  const total = questions.length;
  const isLast = activeStep === total - 1;

  const handleSelectOption = (fieldKey: string, val: string, isMulti = false) => {
    if (isMulti) {
      const currentArr: string[] = answers[fieldKey] || [];
      const updated = currentArr.includes(val)
        ? currentArr.filter((item) => item !== val)
        : [...currentArr, val];
      setAnswers((prev) => ({ ...prev, [fieldKey]: updated }));
    } else {
      setAnswers((prev) => ({ ...prev, [fieldKey]: val }));
      // Auto-advance on single choice if not last
      if (!isLast) {
        setTimeout(() => setActiveStep((prev) => Math.min(prev + 1, total - 1)), 250);
      }
    }
  };

  const handleTextChange = (fieldKey: string, val: string) => {
    setAnswers((prev) => ({ ...prev, [fieldKey]: val }));
  };

  const handleSubmit = () => {
    onSubmitAnswers(answers);
  };

  return (
    <div className="space-y-4 animate-in-up">
      <div className="min-w-0 rounded-[2px] border border-[#d9cebd] border-t-[3px] border-t-[#966931] bg-[#fffaf2] p-5 text-[#2a1c12] sm:p-6 shadow-xs">
        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#ded4c5] pb-4">
          <div className="flex items-center gap-2">
            <span className="font-serif text-lg font-medium text-[#2a1c12]">
              {caseSummary?.dispute_category || "Interactive Matter Assessment"}
            </span>
            <Badge tone="warn">Assessment Required</Badge>
          </div>
          <span className="font-mono text-xs font-semibold text-[#816541]">
            Step {activeStep + 1} of {total}
          </span>
        </div>

        {/* Progress bar */}
        <div className="mt-3 h-1 w-full overflow-hidden rounded-[1px] bg-[#e6dcce]">
          <div
            className="h-full bg-[#966931] transition-all duration-300"
            style={{ width: `${((activeStep + 1) / total) * 100}%` }}
          />
        </div>

        {/* Question Area */}
        <div className="mt-5 space-y-4">
          <div>
            <h3 className="font-serif text-base font-medium text-[#2a1c12] sm:text-lg">
              {currentQ.question}
            </h3>
            {currentQ.help_text && (
              <p className="mt-1 flex items-start gap-1.5 text-xs text-[#70583b]">
                <HelpCircle className="mt-0.5 size-3.5 shrink-0 text-[#855a2c]" />
                <span>{currentQ.help_text}</span>
              </p>
            )}
          </div>

          {/* Options Display */}
          <div className="space-y-2 pt-2">
            {currentQ.type === "text" || currentQ.type === "date" ? (
              <input
                type={currentQ.type === "date" ? "date" : "text"}
                value={answers[currentQ.field_key] || ""}
                onChange={(e) => handleTextChange(currentQ.field_key, e.target.value)}
                placeholder="Enter details here..."
                className="w-full rounded-[2px] border border-[#cfc3b0] bg-white px-3.5 py-2.5 font-sans text-sm text-[#2a1c12] outline-none transition focus:border-[#966931] focus:ring-1 focus:ring-[#966931]"
              />
            ) : (
              <div className="grid gap-2 sm:grid-cols-1">
                {currentQ.options.map((option, idx) => {
                  const isMulti = currentQ.type === "multiple_choice";
                  const isSelected = isMulti
                    ? (answers[currentQ.field_key] || []).includes(option)
                    : answers[currentQ.field_key] === option;

                  return (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleSelectOption(currentQ.field_key, option, isMulti)}
                      className={`flex w-full items-center justify-between rounded-[2px] border p-3.5 text-left font-sans text-sm transition-all ${isSelected
                        ? "border-[#966931] bg-[#f7eedf] text-[#2a1c12] font-medium shadow-xs"
                        : "border-[#d9cebd] bg-white/70 text-[#493727] hover:border-[#b89f81] hover:bg-white"
                        }`}
                    >
                      <span>{option}</span>
                      {isSelected ? (
                        <CheckCircle2 className="size-4.5 text-[#966931]" />
                      ) : (
                        <div className="size-4.5 rounded-[2px] border border-[#cfc3b0]" />
                      )}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Navigation & Submission Controls */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-[#ded4c5] pt-4">
          <button
            type="button"
            onClick={onSkip}
            className="text-xs text-[#816541] underline-offset-4 hover:underline"
          >
            Skip assessment & view preliminary guidance
          </button>

          <div className="flex items-center gap-2">
            {activeStep > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setActiveStep((prev) => prev - 1)}
              >
                Back
              </Button>
            )}

            {!isLast ? (
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setActiveStep((prev) => Math.min(prev + 1, total - 1))}
              >
                Next <ChevronRight className="ml-1 size-4" />
              </Button>
            ) : (
              <Button
                variant="primary"
                size="sm"
                onClick={handleSubmit}
                disabled={isSubmitting}
              >
                {isSubmitting ? "Generating Action Plan..." : "Submit & Generate Action Plan"}
                <ArrowRight className="ml-1 size-4" />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
