import React from "react";
import { BookOpen, ChevronDown } from "lucide-react";
import { CitationChip } from "@/components/dashboard/shared";
import type { CitationItem } from "@/services/dashboard/chat-assistant";
import { cn } from "@/lib/utils";
import styles from "../../chat.module.css";

interface SourcesAccordionProps {
  citations: CitationItem[];
  reviewedDate: string;
  open: boolean;
  onToggle: () => void;
}

/** Collapsed-by-default sources row that reveals mono citation chips. */
export function SourcesAccordion({
  citations,
  reviewedDate,
  open,
  onToggle,
}: SourcesAccordionProps) {
  if (citations.length === 0) return null;

  return (
    <div className="border-t border-[#e2d5c1]/70 pt-3">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        aria-controls="assistant-sources-panel"
        className="inline-flex min-h-10 items-center gap-1.5 rounded-[2px] text-xs font-medium text-[#85725f] transition-colors hover:text-[#2a1c12] hover:bg-[#ebe1d1]/40 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#ebe1d1]/70 sm:min-h-8"
      >
        <BookOpen className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
        <span>Sources ({citations.length})</span>
        <ChevronDown
          className={cn("size-3 transition-transform duration-150", open && "rotate-180")}
          aria-hidden="true"
        />
      </button>

      {open && (
        <div
          id="assistant-sources-panel"
          className={cn(
            styles.fadeIn,
            "mt-2 space-y-2 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/20 p-3"
          )}
        >
          <div className="flex flex-wrap gap-1.5">
            {citations.map((citation) => (
              <CitationChip key={citation.id} citation={citation} />
            ))}
          </div>
          <p className="border-t border-[#e2d5c1]/60 pt-1.5 text-[11px] leading-relaxed text-[#85725f]">
            Based on current law, last reviewed {reviewedDate}.
          </p>
        </div>
      )}
    </div>
  );
}
