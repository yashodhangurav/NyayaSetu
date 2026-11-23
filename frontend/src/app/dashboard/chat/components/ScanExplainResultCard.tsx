"use client";

import React, { useEffect } from "react";
import { FileCheck, CalendarClock, IndianRupee, ArrowRight, X, ShieldAlert } from "lucide-react";
import { Button } from "@/components/dashboard/ui";
import type { ScanExplainResult } from "@/services/dashboard/chat-assistant";
import { DefinitionList } from "./primitives/DefinitionList";
import { cn } from "@/lib/utils";
import styles from "../chat.module.css";

interface ScanExplainResultCardProps {
  result: ScanExplainResult;
  onClose: () => void;
  onAskFollowUp: (prompt: string) => void;
}

export function ScanExplainResultCard({
  result,
  onClose,
  onAskFollowUp,
}: ScanExplainResultCardProps) {
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  return (
    <div className={cn(styles.fadeIn, "mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-[0_1px_2px_rgba(42,28,18,0.04)]")}>
      <div className="flex items-start justify-between gap-3 border-b border-[#e2d5c1]/70 pb-3">
        <div className="flex min-w-0 items-start gap-2.5">
          <span className="grid size-7 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
            <FileCheck className="size-4" aria-hidden="true" />
          </span>
          <div className="min-w-0">
            <h3 className="font-serif text-[17px] font-normal leading-snug text-[#2a1c12]">
              Scan &amp; Explain Analysis
            </h3>
            <p className="mt-1 break-words text-[11px] leading-relaxed text-[#85725f]">
              <span className="font-mono text-[#2a1c12]">{result.fileName}</span> ({result.fileSize}) ·
              OCR verified
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close document analysis"
          className="grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-8"
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      </div>

      <div className="mt-4">
        <DefinitionList
          items={[
            {
              label: "What this is",
              value: result.whatThisIs,
              icon: <FileCheck className="size-3 text-[#9a6a35]" aria-hidden="true" />,
            },
            {
              label: "Deadlines found",
              value: result.deadlinesFound,
              mono: true,
              important: true,
              icon: <CalendarClock className="size-3 text-[#b54708]" aria-hidden="true" />,
            },
            {
              label: "Amounts identified",
              value: result.amounts,
              mono: true,
              icon: <IndianRupee className="size-3 text-[#9a6a35]" aria-hidden="true" />,
            },
            {
              label: "What to do next",
              value: result.whatToDoNext,
              icon: <ShieldAlert className="size-3 text-[#2e7d32]" aria-hidden="true" />,
            },
          ]}
        />
      </div>

      <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-[#e2d5c1]/70 pt-3">
        <span className="text-[11px] leading-relaxed text-[#85725f]">
          Would you like to draft a reply or consult an advocate?
        </span>
        <Button
          size="sm"
          variant="primary"
          onClick={() => onAskFollowUp(`How do I legally reply to the notice in ${result.fileName}?`)}
          className="min-h-10 text-xs sm:min-h-9"
        >
          Draft statutory reply <ArrowRight className="ml-1 size-3" aria-hidden="true" />
        </Button>
      </div>
    </div>
  );
}
