"use client";

import React from "react";
import { ArrowUpRight, Scale, Clock, FileWarning, ShieldAlert } from "lucide-react";

interface EmptyStateProps {
  onSelectPrompt: (prompt: string) => void;
  userName?: string;
}

const STARTER_CARDS = [
  {
    title: "Landlord not returning my deposit",
    description: "Statutory rights, 15-day notice, and Rent Controller recovery steps.",
    icon: Scale,
    prompt: "My landlord is not returning my security deposit after lease termination.",
  },
  {
    title: "Cheque bounced, what now?",
    description: "Strict 30-day notice limitation under Section 138 of the NI Act.",
    icon: Clock,
    prompt: "A commercial cheque bounced due to insufficient funds. What are my deadlines?",
  },
  {
    title: "I received a legal notice",
    description: "Evaluating reply timelines, legal liability, and advocate response.",
    icon: FileWarning,
    prompt: "I received a formal advocate legal notice. How do I evaluate my reply timeline?",
  },
  {
    title: "Someone was arrested",
    description: "Article 22 constitutional safeguards, 24-hr magistrate rule, and bail.",
    icon: ShieldAlert,
    prompt: "Someone was arrested by the police. What are their immediate legal rights?",
  },
];

export function EmptyState({ onSelectPrompt, userName }: EmptyStateProps) {
  const greeting = userName ? `Namaste, ${userName}` : "Namaste";

  return (
    <div className="py-8 sm:py-12 text-center max-w-[680px] mx-auto animate-fade">
      {/* Editorial Greeting */}
      <h2 className="font-serif text-[28px] sm:text-[34px] font-normal tracking-tight text-[#2a1c12] leading-tight">
        {greeting}. How can we assist your matter today?
      </h2>
      <p className="mt-2 text-xs sm:text-[13.5px] text-[#5b4a3b] leading-relaxed max-w-[560px] mx-auto">
        Ask statutory questions in English, Kannada, or Hindi. Grounded in central bare acts and Karnataka rules.
      </p>

      {/* 2x2 Starter Cards */}
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
        {STARTER_CARDS.map((card) => {
          const Icon = card.icon;
          return (
            <button
              key={card.title}
              type="button"
              onClick={() => onSelectPrompt(card.prompt)}
              className="group flex flex-col justify-between rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4 text-left transition-all hover:border-[#9a6a35] hover:bg-[#ebe1d1]/30 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] shadow-xs cursor-pointer"
            >
              <div className="flex items-start justify-between gap-2">
                <span className="grid size-8 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/40 text-[#9a6a35] group-hover:border-[#9a6a35]/60 transition-colors">
                  <Icon className="size-4" aria-hidden="true" />
                </span>
                <ArrowUpRight className="size-4 text-[#85725f] group-hover:text-[#2a1c12] transition-colors" aria-hidden="true" />
              </div>
              <div className="mt-3.5">
                <p className="text-xs sm:text-[13px] font-semibold text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors leading-snug">
                  {card.title}
                </p>
                <p className="mt-1 text-[11.5px] leading-relaxed text-[#5b4a3b]">
                  {card.description}
                </p>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
