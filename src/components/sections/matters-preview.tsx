"use client";

import * as React from "react";
import Link from "next/link";
import { Container } from "@/components/layout/container";

interface MatterItem {
  id: string;
  result: string;
  unit?: string;
  title: string;
  summary: string;
  forum: string;
  year: string;
  category: "Civil & Property" | "Commercial & Debt" | "Criminal & Bail";
}

const mattersList: MatterItem[] = [
  {
    id: "m-1",
    result: "₹1.4",
    unit: "Cr",
    title: "Delayed possession interest and full refund against real estate builder",
    summary: "Recovered complete principal deposit plus 10.85% annual interest for apartment buyers under Section 18 of RERA.",
    forum: "MahaRERA / Bombay HC",
    year: "2025",
    category: "Civil & Property",
  },
  {
    id: "m-2",
    result: "Quashed",
    title: "Anticipatory bail and quashing of motivated FIR under Section 528 BNSS",
    summary: "Defended tech executive against malicious commercial allegations, securing anticipatory bail and full FIR quashing.",
    forum: "Delhi High Court",
    year: "2025",
    category: "Criminal & Bail",
  },
  {
    id: "m-3",
    result: "₹38",
    unit: "Lakh",
    title: "Summary decree & attachment under Section 138 Negotiable Instruments Act",
    summary: "Secured commercial settlement and court attachment decree for MSME vendor following dishonour of commercial cheques.",
    forum: "Commercial Court",
    year: "2024",
    category: "Commercial & Debt",
  },
  {
    id: "m-4",
    result: "Dismissed",
    title: "Frivolous commercial breach and damages arbitration claim dismissed",
    summary: "Dismantled one-sided non-compete penalty claims under Section 27 of the Indian Contract Act with costs awarded.",
    forum: "High Court Bench",
    year: "2024",
    category: "Commercial & Debt",
  },
  {
    id: "m-5",
    result: "₹8.5",
    unit: "Lakh",
    title: "Reversal of unauthorized cyber banking debits within 72-hour RBI rule",
    summary: "Coordinated emergency cyber portal reporting and Ombudsman petition securing 100% reimbursement of stolen funds.",
    forum: "Banking Ombudsman",
    year: "2023",
    category: "Commercial & Debt",
  },
  {
    id: "m-6",
    result: "Decreed",
    title: "Partition decree dividing ancestral land equally among coparceners",
    summary: "Established lawful coparcenary shares for female heirs under Hindu Succession Act, securing registered title deeds.",
    forum: "Civil Court Senior Div",
    year: "2023",
    category: "Civil & Property",
  },
];

export function MattersPreview() {
  const [selectedFilter, setSelectedFilter] = React.useState<string>("All");

  const filteredMatters =
    selectedFilter === "All"
      ? mattersList
      : mattersList.filter((m) => m.category === selectedFilter);

  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        {/* Section Header */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between mb-12 sm:mb-16 gap-6">
          <div>
            <h2 className="font-serif text-[40px] sm:text-[52px] lg:text-[62px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
              Groundwork in law.
              <br />
              <span className="text-[#a89682]">That’s why disputes resolve.</span>
            </h2>
          </div>

          <div className="flex flex-col items-start lg:items-end space-y-3">
            <span className="text-[13px] text-[#85725f]">
              Notable precedents, tribunal relief, and advocate outcomes across Indian forums.
            </span>
            {/* Filter Tabs */}
            <div className="flex items-center space-x-1 border border-[#e2d5c1] bg-[#ece2d3]/50 p-1 rounded-[3px]">
              {["All", "Civil & Property", "Commercial & Debt", "Criminal & Bail"].map((tab) => (
                <button
                  key={tab}
                  type="button"
                  onClick={() => setSelectedFilter(tab)}
                  className={`px-3.5 py-1.5 text-xs font-medium rounded-[2px] transition-colors cursor-pointer ${
                    selectedFilter === tab
                      ? "bg-[#2a1c12] text-[#fffaf2]"
                      : "text-[#5b4a3b] hover:text-[#2a1c12]"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Column Labels */}
        <div className="grid grid-cols-12 pb-3 border-b border-[#e2d5c1] text-[12px] text-[#85725f] font-sans">
          <div className="col-span-3 sm:col-span-3">Relief / Order</div>
          <div className="col-span-6 sm:col-span-6">Precedent & Matter</div>
          <div className="col-span-2 sm:col-span-2">Forum / Bench</div>
          <div className="col-span-1 sm:col-span-1 text-right">Year</div>
        </div>

        {/* Ledger Rows */}
        <div className="divide-y divide-[#e2d5c1]">
          {filteredMatters.map((item) => (
            <div
              key={item.id}
              className="grid grid-cols-12 py-6 sm:py-7 items-baseline gap-2 transition-colors hover:bg-[#fffaf2]/40"
            >
              {/* Result Column */}
              <div className="col-span-3 sm:col-span-3 pr-2">
                <span className="font-serif text-[28px] sm:text-[36px] font-normal text-[#2a1c12] leading-none tracking-tight">
                  {item.result}
                </span>
                {item.unit && (
                  <span className="text-[12px] font-sans text-[#85725f] ml-1">
                    {item.unit}
                  </span>
                )}
              </div>

              {/* Matter Column */}
              <div className="col-span-6 sm:col-span-6 pr-4 sm:pr-8">
                <h3 className="font-sans font-semibold text-[14.5px] sm:text-[15.5px] text-[#2a1c12] leading-snug">
                  {item.title}
                </h3>
                <p className="text-[13px] sm:text-[13.5px] text-[#5b4a3b] mt-1 leading-relaxed">
                  {item.summary}
                </p>
              </div>

              {/* Forum Column */}
              <div className="col-span-2 sm:col-span-2 text-[13px] text-[#5b4a3b]">
                {item.forum}
              </div>

              {/* Year Column */}
              <div className="col-span-1 sm:col-span-1 text-right text-[13px] font-mono text-[#85725f]">
                {item.year}
              </div>
            </div>
          ))}
        </div>

        {/* Bottom Bar: Disclaimer on Left, Link on Right */}
        <div className="mt-8 pt-4 flex flex-col sm:flex-row items-baseline justify-between gap-4 text-[13px]">
          <p className="text-[#85725f]">
            Reported precedents and case studies from Indian courts. Client identities withheld for confidentiality.
          </p>
          <Link
            href="/matters"
            className="font-medium text-[#2a1c12] hover:text-[#9a6a35] underline underline-offset-4 transition-colors whitespace-nowrap"
          >
            All representative precedents
          </Link>
        </div>
      </Container>
    </section>
  );
}
