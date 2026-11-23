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
        "fixed top-20 right-6 z-50 flex items-center gap-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-4 py-3 text-xs font-medium text-[#2a1c12] shadow-[0_8px_24px_-12px_rgba(42,28,18,0.18)] animate-in-up",
        toast.type === "warn" && "border-[#b54708]/40 bg-[#fff8e7] text-[#b54708]"
      )}
    >
      <CheckCircle2 className="size-4 shrink-0 text-[#2e7d32]" aria-hidden="true" />
      <span>{toast.message}</span>
      <button
        type="button"
        onClick={onDismiss}
        aria-label="Close notification"
        className="ml-2 rounded-[2px] p-0.5 text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
      >
        <X className="size-3.5" aria-hidden="true" />
      </button>
    </div>
  );
}
