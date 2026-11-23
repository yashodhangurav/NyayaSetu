import React from "react";
import {
  Check,
  Copy,
  Flag,
  FolderPlus,
  Scale,
  Share2,
  ThumbsDown,
  ThumbsUp,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface ActionBarProps {
  onSaveToCases: () => void;
  briefActive: boolean;
  onToggleBrief: () => void;
  advocatesActive: boolean;
  onToggleAdvocates: () => void;
  copied: boolean;
  onCopy: () => void;
  feedback: "up" | "down" | null;
  onFeedback: (value: "up" | "down") => void;
  flagActive: boolean;
  onToggleFlag: () => void;
}

const textButton =
  "inline-flex min-h-10 items-center gap-1.5 rounded-[2px] px-2 text-[11px] font-medium text-[#5b4a3b] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:min-h-8";

const iconButton =
  "grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-8";

/** Single quiet action row beneath a structured answer. */
export function ActionBar({
  onSaveToCases,
  briefActive,
  onToggleBrief,
  advocatesActive,
  onToggleAdvocates,
  copied,
  onCopy,
  feedback,
  onFeedback,
  flagActive,
  onToggleFlag,
}: ActionBarProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-1 border-t border-[#e2d5c1]/70 pt-2">
      <div className="flex flex-wrap items-center gap-0.5">
        <button type="button" onClick={onSaveToCases} className={textButton}>
          <FolderPlus className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
          Save to My Cases
        </button>
        <button
          type="button"
          onClick={onToggleBrief}
          aria-pressed={briefActive}
          className={cn(textButton, briefActive && "bg-[#ebe1d1]/70 text-[#2a1c12]")}
        >
          <Share2 className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
          Prepare case brief
        </button>
        <button
          type="button"
          onClick={onToggleAdvocates}
          aria-pressed={advocatesActive}
          className={cn(textButton, advocatesActive && "bg-[#ebe1d1]/70 text-[#2a1c12]")}
        >
          <Scale className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
          Find advocate
        </button>
      </div>

      <div className="flex items-center gap-0.5 text-[#85725f]">
        <button
          type="button"
          onClick={onCopy}
          aria-label="Copy answer"
          title="Copy answer"
          className={iconButton}
        >
          {copied ? (
            <Check className="size-3.5 text-[#2e7d32]" aria-hidden="true" />
          ) : (
            <Copy className="size-3.5" aria-hidden="true" />
          )}
        </button>
        <button
          type="button"
          onClick={() => onFeedback("up")}
          aria-label="Helpful"
          aria-pressed={feedback === "up"}
          title="Helpful"
          className={cn(iconButton, feedback === "up" && "text-[#2e7d32]")}
        >
          <ThumbsUp className="size-3.5" aria-hidden="true" />
        </button>
        <button
          type="button"
          onClick={() => onFeedback("down")}
          aria-label="Not helpful"
          aria-pressed={feedback === "down"}
          title="Not helpful"
          className={cn(iconButton, feedback === "down" && "text-[#c0392b]")}
        >
          <ThumbsDown className="size-3.5" aria-hidden="true" />
        </button>
        <button
          type="button"
          onClick={onToggleFlag}
          aria-label="Flag an error"
          aria-pressed={flagActive}
          title="Flag an error"
          className={cn(iconButton, flagActive && "bg-[#ebe1d1]/70 text-[#2a1c12]")}
        >
          <Flag className="size-3.5" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}
