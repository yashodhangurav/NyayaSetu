"use client";

import React, { useEffect, useState } from "react";
import { Scale, CheckCircle2, ShieldCheck, UserCheck, X } from "lucide-react";
import { MOCK_MATCHED_ADVOCATES, type FictionalAdvocate } from "@/services/dashboard/chat-assistant";
import { Badge, Button } from "@/components/dashboard/ui";
import { DefinitionList } from "./primitives/DefinitionList";
import { AdvocateCardsSkeleton } from "./primitives/Skeletons";
import { cn } from "@/lib/utils";
import styles from "../chat.module.css";

interface AdvocateMatchInlineProps {
  onClose: () => void;
  onRequestConsultation: (advocateName: string) => void;
  /** Reserved for a real advocate-data fetch; never simulated here. */
  loading?: boolean;
}

const closeButton =
  "grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-8";

export function AdvocateMatchInline({
  onClose,
  onRequestConsultation,
  loading = false,
}: AdvocateMatchInlineProps) {
  const [requested, setRequested] = useState<string | null>(null);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  const handleRequest = (advocate: FictionalAdvocate) => {
    setRequested(advocate.id);
    onRequestConsultation(advocate.name);
  };

  if (loading) return <AdvocateCardsSkeleton count={3} />;

  return (
    <div className={cn(styles.fadeIn, "mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4.5 shadow-[0_1px_2px_rgba(42,28,18,0.04)] sm:p-5")}>
      <div className="flex items-start justify-between gap-3 border-b border-[#e2d5c1]/70 pb-3">
        <div className="flex min-w-0 items-start gap-2.5">
          <span className="grid size-7 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
            <Scale className="size-4" aria-hidden="true" />
          </span>
          <div className="min-w-0">
            <h3 className="font-serif text-[16px] font-normal leading-snug text-[#2a1c12]">
              Matched for this case
            </h3>
            <p className="mt-1 break-words text-[11px] leading-relaxed text-[#85725f]">
              Belagavi District &amp; Sessions Court · Merit-matched (BCI Rule 36 compliant)
            </p>
          </div>
        </div>
        <button type="button" onClick={onClose} aria-label="Close advocate match list" className={closeButton}>
          <X className="size-4" aria-hidden="true" />
        </button>
      </div>

      {/* Stacked advocate cards, capped at three. */}
      <div className="mt-3.5 space-y-3">
        {MOCK_MATCHED_ADVOCATES.slice(0, 3).map((advocate) => (
          <div
            key={advocate.id}
            className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-3.5"
          >
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div className="min-w-0 flex-1 space-y-1">
                <div className="flex flex-wrap items-center gap-1.5">
                  <h4 className="min-w-0 break-words text-[13px] font-medium text-[#2a1c12]">
                    {advocate.name}
                  </h4>
                  <Badge tone="mint" className={cn(styles.pill, "gap-1 px-2 py-0 text-[9.5px]")}>
                    <CheckCircle2 className="size-2.5 shrink-0" aria-hidden="true" />
                    {advocate.enrolmentBadge}
                  </Badge>
                  <Badge tone="stamp" className={cn(styles.pill, "gap-1 px-2 py-0 text-[9.5px]")}>
                    <ShieldCheck className="size-2.5 shrink-0 text-[#9a6a35]" aria-hidden="true" />
                    {advocate.activityBadge}
                  </Badge>
                </div>
                <DefinitionList
                  items={[
                    { label: "Focus", value: advocate.practiceAreas },
                    {
                      label: "Court & language",
                      value: `${advocate.court} · ${advocate.languages.join(", ")}`,
                    },
                  ]}
                />
              </div>

              <div className="flex w-full shrink-0 flex-wrap items-center justify-between gap-2 sm:w-auto sm:flex-col sm:items-end sm:justify-start">
                <span className="font-mono text-[11.5px] font-medium text-[#2a1c12]">
                  {advocate.feeRange}
                </span>
                <Button
                  size="sm"
                  variant={requested === advocate.id ? "secondary" : "primary"}
                  onClick={() => handleRequest(advocate)}
                  disabled={requested === advocate.id}
                  className="min-h-10 px-3 text-[11px] select-none sm:min-h-8"
                >
                  {requested === advocate.id ? (
                    <>
                      <UserCheck className="mr-1 size-3 text-[#2e7d32]" aria-hidden="true" />
                      Requested
                    </>
                  ) : (
                    "Request consultation"
                  )}
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
