import React from "react";
import { Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

/** 24px assistant brand mark, shown once on the first line of an answer. */
export function BrandMark({ className }: { className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={cn(
        "grid size-6 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]",
        className
      )}
    >
      <Sparkles className="size-3.5" />
    </span>
  );
}
