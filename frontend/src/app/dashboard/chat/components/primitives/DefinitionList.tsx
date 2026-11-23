import React from "react";
import { cn } from "@/lib/utils";

export interface DefinitionItem {
  label: string;
  value: React.ReactNode;
  /** Render the value in the docket mono face (dates, amounts, sections). */
  mono?: boolean;
  /** Small icon preceding the label. */
  icon?: React.ReactNode;
  /** Use the existing amber/red token for time-critical rows. */
  important?: boolean;
}

/** Document-style label/value rows with hairline separators. */
export function DefinitionList({
  items,
  className,
}: {
  items: DefinitionItem[];
  className?: string;
}) {
  return (
    <dl className={cn("divide-y divide-[#e2d5c1]/70", className)}>
      {items.map((item, index) => (
        <div
          key={`${item.label}-${index}`}
          className="grid gap-1 py-2.5 first:pt-0 last:pb-0 sm:grid-cols-[minmax(0,170px)_minmax(0,1fr)] sm:gap-5"
        >
          <dt className="flex min-w-0 items-center gap-1.5 text-[11px] font-medium uppercase tracking-[0.1em] text-[#85725f]">
            {item.icon}
            <span className="min-w-0 break-words">{item.label}</span>
          </dt>
          <dd
            className={cn(
              "min-w-0 break-words text-[13px] leading-relaxed text-[#2a1c12]",
              item.mono && "font-mono",
              item.important && "text-[#b54708]"
            )}
          >
            {item.value}
          </dd>
        </div>
      ))}
    </dl>
  );
}
