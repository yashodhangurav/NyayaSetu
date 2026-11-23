"use client";

import React from "react";
import { FileCheck, CalendarClock, IndianRupee, ArrowRight, X, ShieldAlert } from "lucide-react";
import { Button } from "@/components/dashboard/ui";
import type { ScanExplainResult } from "@/services/dashboard/chat-assistant";

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
  return (
    <div className="mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-xs animate-in-up">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[#e2d5c1]/70 pb-3">
        <div className="flex items-center gap-2">
          <span className="grid size-7 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
            <FileCheck className="size-4" aria-hidden="true" />
          </span>
          <div>
            <h3 className="font-serif text-[17px] font-normal text-[#2a1c12] leading-none">
              Scan & Explain Analysis
            </h3>
            <p className="mt-1 text-[11px] text-[#85725f]">
              File: <span className="font-mono text-[#2a1c12]">{result.fileName}</span> ({result.fileSize}) · OCR Verified
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close document analysis"
          className="rounded-[2px] p-1 text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      </div>

      {/* Grid of Results */}
      <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        {/* What this is */}
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3.5 space-y-1">
          <div className="flex items-center gap-1.5 text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
            <FileCheck className="size-3 text-[#9a6a35]" />
            What this is
          </div>
          <p className="text-[#2a1c12] leading-relaxed font-medium">{result.whatThisIs}</p>
        </div>

        {/* Deadlines found */}
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3.5 space-y-1">
          <div className="flex items-center gap-1.5 text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#b54708]">
            <CalendarClock className="size-3 text-[#b54708]" />
            Deadlines found
          </div>
          <p className="text-[#2a1c12] leading-relaxed font-mono font-medium">{result.deadlinesFound}</p>
        </div>

        {/* Amounts */}
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3.5 space-y-1">
          <div className="flex items-center gap-1.5 text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#85725f]">
            <IndianRupee className="size-3 text-[#9a6a35]" />
            Amounts identified
          </div>
          <p className="text-[#2a1c12] leading-relaxed font-mono font-medium">{result.amounts}</p>
        </div>

        {/* What to do next */}
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/25 p-3.5 space-y-1">
          <div className="flex items-center gap-1.5 text-[10.5px] font-sans uppercase tracking-[0.1em] font-semibold text-[#2e7d32]">
            <ShieldAlert className="size-3 text-[#2e7d32]" />
            What to do next
          </div>
          <p className="text-[#2a1c12] leading-relaxed font-medium">{result.whatToDoNext}</p>
        </div>
      </div>

      {/* Footer prompt */}
      <div className="mt-4 pt-3 border-t border-[#e2d5c1]/70 flex flex-wrap items-center justify-between gap-2">
        <span className="text-[11px] text-[#85725f]">
          Would you like to draft a reply or consult an advocate?
        </span>
        <Button
          size="sm"
          variant="primary"
          onClick={() => onAskFollowUp(`How do I legally reply to the notice in ${result.fileName}?`)}
          className="text-xs h-8"
        >
          Draft statutory reply <ArrowRight className="size-3 ml-1" />
        </Button>
      </div>
    </div>
  );
}
