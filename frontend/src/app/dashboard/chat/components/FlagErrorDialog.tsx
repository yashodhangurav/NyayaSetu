"use client";

import React, { useEffect, useState } from "react";
import { Flag, X, Send } from "lucide-react";
import { Button } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";
import styles from "../chat.module.css";

interface FlagErrorDialogProps {
  onClose: () => void;
  onSubmitFlag: (feedback: string) => void;
}

export function FlagErrorDialog({
  onClose,
  onSubmitFlag,
}: FlagErrorDialogProps) {
  const [feedback, setFeedback] = useState("");

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!feedback.trim()) return;
    onSubmitFlag(feedback.trim());
  };

  return (
    <div className={cn(styles.fadeIn, "mt-3 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-3.5 shadow-[0_1px_2px_rgba(42,28,18,0.04)]")}>
      <div className="flex items-center justify-between border-b border-[#e2d5c1]/60 pb-2">
        <span className="flex items-center gap-1.5 text-xs font-medium text-[#2a1c12]">
          <Flag className="size-3.5 text-[#b54708]" aria-hidden="true" />
          Flag an error in this answer
        </span>
        <button
          type="button"
          onClick={onClose}
          aria-label="Cancel flagging"
          className="grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-8"
        >
          <X className="size-3.5" aria-hidden="true" />
        </button>
      </div>
      <form onSubmit={handleSubmit} className="mt-2.5 flex items-center gap-2">
        <input
          type="text"
          value={feedback}
          onChange={(event) => setFeedback(event.target.value)}
          placeholder="State what is inaccurate or outdated..."
          className="h-10 min-w-0 flex-1 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 text-xs text-[#2a1c12] placeholder:text-[#85725f]/60 focus:border-[#9a6a35] focus:outline-none focus:ring-1 focus:ring-[#9a6a35] sm:h-8.5"
          autoFocus
        />
        <Button
          type="submit"
          size="sm"
          variant="primary"
          disabled={!feedback.trim()}
          className="min-h-10 px-3 text-xs sm:min-h-8.5"
        >
          Submit <Send className="ml-1 size-3" aria-hidden="true" />
        </Button>
      </form>
      <p className="mt-1.5 text-[10.5px] leading-relaxed text-[#85725f]">
        Your correction will be audited against current High Court and Gazette revisions.
      </p>
    </div>
  );
}
