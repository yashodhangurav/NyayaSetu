"use client";

import * as React from "react";
import { Container } from "@/components/layout/container";
import { faqs } from "@/data/faqs";

export function FaqSection() {
  const [openIndex, setOpenIndex] = React.useState<number | null>(null);

  const toggle = (idx: number) => {
    setOpenIndex((prev) => (prev === idx ? null : idx));
  };

  // Top 5 FAQs for the homepage
  const displayFaqs = faqs.slice(0, 5);

  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-start">
          {/* Left Column: Heading & Subhead */}
          <div className="lg:col-span-5 space-y-4">
            <h2 className="font-serif text-[40px] sm:text-[52px] lg:text-[62px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
              Questions,
              <br />
              <span className="text-[#a89682]">answered.</span>
            </h2>
            <p className="text-[14px] sm:text-[15px] text-[#5b4a3b] leading-[1.6] pt-2">
              Still unsure? Call <span className="font-medium text-[#2a1c12]">1800-NYAYA-SETU (1800-692-9273)</span> and our legal triage desk will guide you.
            </p>
          </div>

          {/* Right Column: Accordion Items */}
          <div className="lg:col-span-7 divide-y divide-[#e2d5c1] border-y border-[#e2d5c1]">
            {displayFaqs.map((faq, idx) => {
              const isOpen = openIndex === idx;
              return (
                <div key={faq.id} className="py-5 sm:py-6">
                  <button
                    type="button"
                    onClick={() => toggle(idx)}
                    className="w-full flex items-center justify-between text-left group cursor-pointer"
                    aria-expanded={isOpen}
                  >
                    <span className="font-sans font-medium text-[16px] sm:text-[18px] text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors pr-4">
                      {faq.question}
                    </span>
                    <span className="flex items-center justify-center w-7 h-7 rounded-full border border-[#e2d5c1] text-[#2a1c12] group-hover:border-[#9a6a35] group-hover:text-[#9a6a35] transition-colors shrink-0 text-sm font-light">
                      {isOpen ? "−" : "+"}
                    </span>
                  </button>

                  {isOpen && (
                    <div className="pt-4 pr-8 text-[14px] sm:text-[14.5px] leading-[1.65] text-[#5b4a3b]">
                      {faq.answer}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </Container>
    </section>
  );
}
