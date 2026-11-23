import React from "react";
import { Badge } from "@/components/dashboard/ui";
import type { DecisionBadgeType } from "@/services/dashboard/chat-assistant";
import { cn } from "@/lib/utils";
import styles from "../../chat.module.css";

type Tone = "mint" | "warn" | "neutral" | "danger";

const VARIANTS: Record<DecisionBadgeType, { tone: Tone; dot: string }> = {
  "Self-help first": { tone: "mint", dot: "bg-[#2e7d32]" },
  "Time-sensitive": { tone: "warn", dot: "bg-[#b54708]" },
  "Advocate advised": { tone: "neutral", dot: "bg-[#9a6a35]" },
  Urgent: { tone: "danger", dot: "bg-[#c0392b]" },
};

/** Shared four-variant decision badge with a status dot. */
export function DecisionBadge({
  variant,
  className,
}: {
  variant: DecisionBadgeType;
  className?: string;
}) {
  const { tone, dot } = VARIANTS[variant] ?? VARIANTS["Advocate advised"];

  return (
    <Badge
      tone={tone}
      className={cn(styles.pill, "gap-1.5 px-2.5 py-1 text-[11px]", className)}
    >
      <span className={cn("size-1.5 shrink-0 rounded-full", dot)} aria-hidden="true" />
      {variant}
    </Badge>
  );
}
