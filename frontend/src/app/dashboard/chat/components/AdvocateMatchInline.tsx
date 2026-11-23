"use client";

import React, { useState } from "react";
import { Scale, CheckCircle2, ShieldCheck, UserCheck, X } from "lucide-react";
import { MOCK_MATCHED_ADVOCATES, type FictionalAdvocate } from "@/services/dashboard/chat-assistant";
import { Badge, Button } from "@/components/dashboard/ui";

interface AdvocateMatchInlineProps {
  onClose: () => void;
  onRequestConsultation: (advocateName: string) => void;
}

export function AdvocateMatchInline({
  onClose,
  onRequestConsultation,
}: AdvocateMatchInlineProps) {
  const [requested, setRequested] = useState<string | null>(null);

  const handleRequest = (adv: FictionalAdvocate) => {
    setRequested(adv.id);
    onRequestConsultation(adv.name);
  };

  return (
    <div className="mt-4 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4.5 sm:p-5 shadow-xs animate-in-up">
      <div className="flex items-center justify-between border-b border-[#e2d5c1]/70 pb-3">
        <div className="flex items-center gap-2">
          <span className="grid size-7 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
            <Scale className="size-4" aria-hidden="true" />
          </span>
          <div>
            <h3 className="font-serif text-[16px] font-normal text-[#2a1c12] leading-none">
              Matched for this case
            </h3>
            <p className="mt-1 text-[11px] text-[#85725f]">
              Jurisdiction: <span className="font-medium text-[#2a1c12]">Belagavi District & Sessions Court</span> · Merit-matched (BCI Rule 36 compliant)
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close advocate match list"
          className="rounded-[2px] p-1 text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors"
        >
          <X className="size-4" aria-hidden="true" />
        </button>
      </div>

      {/* Advocates List */}
      <div className="mt-3.5 divide-y divide-[#e2d5c1]/60">
        {MOCK_MATCHED_ADVOCATES.map((adv) => (
          <div key={adv.id} className="py-3.5 first:pt-1 last:pb-1">
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
              <div className="space-y-1.5 min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h4 className="text-xs sm:text-[13.5px] font-semibold text-[#2a1c12]">
                    {adv.name}
                  </h4>
                  <Badge tone="mint" className="text-[9.5px] py-0">
                    <CheckCircle2 className="size-2.5 mr-0.5 inline" aria-hidden="true" />
                    {adv.enrolmentBadge}
                  </Badge>
                  <Badge tone="stamp" className="text-[9.5px] py-0">
                    <ShieldCheck className="size-2.5 mr-0.5 inline text-[#9a6a35]" aria-hidden="true" />
                    {adv.activityBadge}
                  </Badge>
                </div>

                <p className="text-xs text-[#5b4a3b] leading-relaxed">
                  <span className="font-medium text-[#2a1c12]">Focus:</span> {adv.practiceAreas}
                </p>
                <p className="text-[11px] text-[#85725f] leading-normal">
                  <span className="font-medium text-[#2a1c12]">Court & Language:</span> {adv.court} · {adv.languages.join(", ")}
                </p>
              </div>

              <div className="sm:text-right shrink-0 flex sm:flex-col items-center sm:items-end justify-between sm:justify-start gap-2 pt-1 sm:pt-0">
                <span className="text-[11.5px] font-mono font-medium text-[#2a1c12]">
                  {adv.feeRange}
                </span>
                <Button
                  size="sm"
                  variant={requested === adv.id ? "secondary" : "primary"}
                  onClick={() => handleRequest(adv)}
                  disabled={requested === adv.id}
                  className="h-8 text-[11px] px-3 select-none"
                >
                  {requested === adv.id ? (
                    <>
                      <UserCheck className="size-3 mr-1 text-[#2e7d32]" />
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
