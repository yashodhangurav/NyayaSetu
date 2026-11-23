"use client";

import React, { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import styles from "../chat.module.css";

const THINKING_STEPS = [
  "Understanding your problem...",
  "Checking Karnataka and central law...",
  "Verifying citations...",
];

/** One quiet line: a pulsing dot plus cycling status text. */
export function ThinkingState() {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStepIndex((previous) => (previous + 1) % THINKING_STEPS.length);
    }, 900);
    return () => clearInterval(interval);
  }, []);

  return (
    <div role="status" aria-live="polite" className="flex items-center gap-2 py-1">
      <span className={styles.pulseDot} aria-hidden="true" />
      <span
        key={stepIndex}
        className={cn(styles.fadeIn, "text-xs leading-relaxed text-[#85725f] motion-reduce:animate-none")}
      >
        {THINKING_STEPS[stepIndex]}
      </span>
    </div>
  );
}
