"use client";

import React, { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";

const THINKING_STEPS = [
  "Understanding your problem...",
  "Checking Karnataka and central law...",
  "Verifying citations...",
];

export function ThinkingState() {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStepIndex((prev) => (prev + 1) % THINKING_STEPS.length);
    }, 900);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      role="status"
      aria-live="polite"
      className="flex items-center gap-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-4 py-3 text-xs text-[#5b4a3b] shadow-xs"
    >
      <span className="grid size-6 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
        <Sparkles className="size-3.5 animate-spin motion-reduce:animate-none" aria-hidden="true" />
      </span>
      <span className="font-sans font-medium text-[#2a1c12] transition-opacity duration-300">
        {THINKING_STEPS[stepIndex]}
      </span>
      <div className="ml-auto flex items-center gap-1" aria-hidden="true">
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </div>
  );
}
