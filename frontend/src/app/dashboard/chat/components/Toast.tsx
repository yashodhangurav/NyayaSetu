"use client";

import React, { useEffect } from "react";
import { CheckCircle2, X } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ToastMessage {
  id: string;
  message: string;
  type?: "success" | "info" | "warn";
}

export function Toast({
  toast,
  onDismiss,
}: {
  toast: ToastMessage | null;
  onDismiss: () => void;
}) {
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => {
      onDismiss();
    }, 4000);
    return () => clearTimeout(timer);
  }, [toast, onDismiss]);

  if (!toast) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        "fixed top-20 right-6 z-50 flex max-w-[calc(100vw-3rem)] items-center gap-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-4 py-3 text-xs font-medium text-[#2a1c12] shadow-[0_8px_24px_-12px_rgba(42,28,18,0.18)] animate-in-up",
        toast.type === "warn" && "border-[#b54708]/40 bg-[#fff8e7] text-[#b54708]"
      )}
    >
      <CheckCircle2
        className={cn(
          "size-4 shrink-0 text-[#2e7d32]",
          toast.type === "warn" && "text-[#b54708]"
        )}
        aria-hidden="true"
      />
      <span className="min-w-0 break-words">{toast.message}</span>
      <button
        type="button"
        onClick={onDismiss}
        aria-label="Close notification"
        className="grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-8"
      >
        <X className="size-3.5" aria-hidden="true" />
      </button>
    </div>
  );
}
