import React from "react";
import { cn } from "@/lib/utils";
import styles from "../../chat.module.css";

/** Beige bar used inside the two loading placeholders below. */
function Bar({ className }: { className?: string }) {
  return <div className={cn(styles.skeleton, "h-3", className)} />;
}

/** Placeholder for a real advocate-data fetch. Not used for mock toggles. */
export function AdvocateCardsSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="mt-4 space-y-3" aria-busy="true" aria-label="Loading matched advocates">
      {Array.from({ length: count }).map((_, index) => (
        <div
          key={index}
          className="space-y-3 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4"
        >
          <Bar className="w-1/2" />
          <Bar className="w-3/4" />
          <Bar className="w-2/3" />
          <Bar className="h-8 w-28" />
        </div>
      ))}
    </div>
  );
}

/** Placeholder for a real case-brief generation fetch. */
export function BriefCardSkeleton() {
  return (
    <div
      className="mt-4 space-y-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5"
      aria-busy="true"
      aria-label="Loading case brief"
    >
      <Bar className="h-5 w-44" />
      <div className="grid gap-3 sm:grid-cols-2">
        <Bar className="h-12 w-full" />
        <Bar className="h-12 w-full" />
        <Bar className="h-12 w-full" />
        <Bar className="h-12 w-full" />
      </div>
    </div>
  );
}
