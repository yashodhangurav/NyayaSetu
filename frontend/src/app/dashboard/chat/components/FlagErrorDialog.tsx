"use client";

import React, { useState } from "react";
import { Flag, X, Send } from "lucide-react";
import { Button } from "@/components/dashboard/ui";

interface FlagErrorDialogProps {
  onClose: () => void;
  onSubmitFlag: (feedback: string) => void;
}

export function FlagErrorDialog({
  onClose,
  onSubmitFlag,
}: FlagErrorDialogProps) {
  const [feedback, setFeedback] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) return;
    onSubmitFlag(feedback.trim());
  };

  return (
    <div className="mt-3 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-3.5 shadow-xs animate-in-up">
      <div className="flex items-center justify-between border-b border-[#e2d5c1]/60 pb-2">
        <span className="flex items-center gap-1.5 text-xs font-semibold text-[#2a1c12]">
          <Flag className="size-3.5 text-[#b54708]" aria-hidden="true" />
          Flag an error in this answer
        </span>
        <button
          type="button"
          onClick={onClose}
          aria-label="Cancel flagging"
          className="rounded-[2px] p-0.5 text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12]"
        >
          <X className="size-3.5" aria-hidden="true" />
        </button>
      </div>
      <form onSubmit={handleSubmit} className="mt-2.5 flex items-center gap-2">
        <input
          type="text"
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="State what is inaccurate or outdated (e.g. Karnataka amendment section)..."
          className="flex-1 h-8.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 text-xs text-[#2a1c12] placeholder:text-[#85725f]/60 focus:outline-none focus:border-[#9a6a35] focus:ring-1 focus:ring-[#9a6a35]"
          autoFocus
        />
        <Button
          type="submit"
          size="sm"
          variant="primary"
          disabled={!feedback.trim()}
          className="h-8.5 text-xs px-3"
        >
          Submit <Send className="size-3 ml-1" />
        </Button>
      </form>
      <p className="mt-1.5 text-[10.5px] text-[#85725f]">
        Your correction will be audited against current High Court and Gazette revisions.
      </p>
    </div>
  );
}
