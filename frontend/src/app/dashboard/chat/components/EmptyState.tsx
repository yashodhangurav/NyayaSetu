"use client";

import React from "react";
import { ArrowUpRight, Scale, Clock, FileWarning, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";
import styles from "../chat.module.css";

interface EmptyStateProps {
  onSelectPrompt: (prompt: string) => void;
  userName?: string;
}

const STARTER_CARDS = [
  {
    title: "Landlord not returning my deposit",
    icon: Scale,
    prompt: "My landlord is not returning my security deposit after lease termination.",
  },
  {
    title: "Cheque bounced, what now?",
    icon: Clock,
    prompt: "A commercial cheque bounced due to insufficient funds. What are my deadlines?",
  },
  {
    title: "I received a legal notice",
    icon: FileWarning,
    prompt: "I received a formal advocate legal notice. How do I evaluate my reply timeline?",
  },
  {
    title: "Someone was arrested",
    icon: ShieldAlert,
    prompt: "Someone was arrested by the police. What are their immediate legal rights?",
  },
];

export function EmptyState({ onSelectPrompt, userName }: EmptyStateProps) {
  const greeting = userName ? `Namaste, ${userName}` : "Namaste";

  return (
    <div className={cn(styles.fadeIn, "py-8 text-center sm:py-12")}>
      <h2 className="font-serif text-[26px] font-normal leading-tight tracking-tight text-[#2a1c12] sm:text-[32px]">
        {greeting}. How can we assist your matter today?
      </h2>
      <p className="mx-auto mt-2 max-w-[560px] text-xs leading-relaxed text-[#85725f] sm:text-[13px]">
        Ask statutory questions in English, Kannada, or Hindi. Grounded in central bare acts and
        Karnataka rules.
      </p>

      {/* Hairline starter cards: one line each, subtle hover. */}
      <div className="mx-auto mt-8 grid max-w-[640px] grid-cols-1 gap-2 text-left sm:grid-cols-2">
        {STARTER_CARDS.map((card) => {
          const Icon = card.icon;
          return (
            <button
              key={card.title}
              type="button"
              onClick={() => onSelectPrompt(card.prompt)}
              className="group inline-flex min-h-12 items-center gap-2.5 rounded-[2px] border border-[#e2d5c1] bg-transparent px-3.5 text-left transition-colors hover:border-[#9a6a35] hover:bg-[#ebe1d1]/30 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1]/40"
            >
              <Icon className="size-4 shrink-0 text-[#9a6a35]" aria-hidden="true" />
              <span className="min-w-0 flex-1 truncate text-[13px] text-[#2a1c12] transition-colors group-hover:text-[#9a6a35]">
                {card.title}
              </span>
              <ArrowUpRight
                className="size-3.5 shrink-0 text-[#85725f] transition-colors group-hover:text-[#2a1c12]"
                aria-hidden="true"
              />
            </button>
          );
        })}
      </div>
    </div>
  );
}
