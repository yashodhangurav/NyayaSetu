"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";

interface PartnerDetail {
  id: string;
  num: string;
  name: string;
  role: string;
  practice: string;
  image: string;
  summary: string;
  inPractice: string;
  admitted: string;
}

const partnersList: PartnerDetail[] = [
  {
    id: "rajeshwari-sen",
    num: "01",
    name: "Adv. Rajeshwari Sen",
    role: "Senior Advocate",
    practice: "Civil & Property Law",
    image: "https://framerusercontent.com/images/0LArNLIabDDiZZoFMZhtVP1Dudc.webp?width=1200&height=1500",
    summary:
      "24 years of active standing before the Supreme Court of India and High Court of Delhi. Specializes in constitutional writs, property partition, commercial arbitration, and land revenue appeals.",
    inPractice: "24 years (D/1420/2000)",
    admitted: "Supreme Court of India · Delhi High Court",
  },
  {
    id: "vikramaditya-deshmukh",
    num: "02",
    name: "Adv. Vikramaditya Deshmukh",
    role: "Advocate",
    practice: "Startup & Corporate Law",
    image: "https://framerusercontent.com/images/aduozO96ZbkNp24VgIVFxOelF4.webp?width=1200&height=1500",
    summary:
      "Advises emerging tech startups, venture funds, and family businesses on founder equity vesting, Companies Act compliance, and NCLT corporate dispute resolution.",
    inPractice: "19 years (MAH/2841/2005)",
    admitted: "Bombay High Court · NCLT Mumbai",
  },
  {
    id: "harshvardhan-kapoor",
    num: "03",
    name: "Adv. Harshvardhan Kapoor",
    role: "Advocate",
    practice: "Criminal Defense & Bail",
    image: "https://framerusercontent.com/images/aP4i3MQtE6NvStb54fOi7D2gxG8.webp?width=1200&height=1500",
    summary:
      "Represents individuals in white-collar defenses, economic offenses inquiries, anticipatory bail under BNSS, and High Court FIR quashing petitions.",
    inPractice: "18 years (D/892/2006)",
    admitted: "High Court of Delhi · Sessions Courts",
  },
  {
    id: "ananya-sundaram",
    num: "04",
    name: "Adv. Ananya Sundaram",
    role: "Advocate",
    practice: "Consumer & Cyber Law",
    image: "https://framerusercontent.com/images/9wg0juCfo5rrwm9BHnLZFuKX3g.webp?width=1200&height=1500",
    summary:
      "Specializes in consumer dispute litigation against large corporate entities, cyber fraud remediation, and tech regulatory compliance.",
    inPractice: "14 years (KAR/1140/2010)",
    admitted: "Karnataka High Court · NCDRC New Delhi",
  },
  {
    id: "sunita-banerjee",
    num: "05",
    name: "Adv. Sunita Banerjee",
    role: "Advocate",
    practice: "Family & Matrimonial Law",
    image: "https://framerusercontent.com/images/0LArNLIabDDiZZoFMZhtVP1Dudc.webp?width=1200&height=1500",
    summary:
      "Guides individuals through mutual consent divorce, shared child parenting agreements, domestic violence proceedings, and succession planning.",
    inPractice: "21 years (WB/512/2003)",
    admitted: "Calcutta High Court · Family Courts",
  },
  {
    id: "pradeep-nair",
    num: "06",
    name: "Adv. Pradeep Nair",
    role: "Advocate",
    practice: "Real Estate & RERA",
    image: "https://framerusercontent.com/images/aP4i3MQtE6NvStb54fOi7D2gxG8.webp?width=1200&height=1500",
    summary:
      "Represents homebuyers and commercial landholders before RERA authorities and High Courts in delayed possession and title encumbrance disputes.",
    inPractice: "16 years (K/784/2008)",
    admitted: "Kerala High Court · RERA Appellate",
  },
  {
    id: "alok-chawla",
    num: "07",
    name: "Adv. Alok Chawla",
    role: "Advocate",
    practice: "Cheque Bounce & Debt Recovery",
    image: "https://framerusercontent.com/images/aduozO96ZbkNp24VgIVFxOelF4.webp?width=1200&height=1500",
    summary:
      "Assists businesses and contractors in recovering dishonoured commercial payments under Section 138 NI Act and summary commercial suits.",
    inPractice: "15 years (D/2210/2009)",
    admitted: "Delhi High Court · Commercial Courts",
  },
];

export function PartnerShowcase() {
  const [activePartnerId, setActivePartnerId] = React.useState<string>("rajeshwari-sen");

  const activePartner =
    partnersList.find((p) => p.id === activePartnerId) || partnersList[0];
  const otherPartners = partnersList.filter((p) => p.id !== activePartnerId);

  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        {/* Section Header */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between mb-14 sm:mb-16 gap-6">
          <div>
            <h2 className="font-serif text-[40px] sm:text-[52px] lg:text-[62px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
              The advocate you choose
              <br />
              <span className="text-[#a89682]">is the one who represents you.</span>
            </h2>
          </div>

          <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6] max-w-sm">
            Every legal professional on NyayaSetu is verified with their State Bar Council. You connect directly with qualified counsel based on jurisdiction, language, and subject expertise.
          </p>
        </div>

        {/* 2-Column Showcase */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-start">
          {/* Left Column: Portrait Photo */}
          <div className="lg:col-span-5">
            <div className="relative aspect-[3/4] w-full rounded-[2px] overflow-hidden border border-[#e2d5c1] shadow-[0_8px_30px_rgba(42,28,18,0.08)] bg-[#ebe1d1]">
              <Image
                src={activePartner.image}
                alt={activePartner.name}
                fill
                sizes="(max-width: 1024px) 100vw, 40vw"
                className="object-cover object-[50%_18%] filter contrast-[1.02] transition-all duration-500"
              />
            </div>
          </div>

          {/* Right Column: Active Partner Bio + Partner Switcher List */}
          <div className="lg:col-span-7 flex flex-col justify-between">
            {/* Active Partner Bio Block */}
            <div className="space-y-4 pb-8 border-b border-[#e2d5c1]">
              <h3 className="font-serif text-[38px] sm:text-[46px] font-normal text-[#2a1c12] leading-tight tracking-tight">
                {activePartner.name}
              </h3>
              <div className="text-[13px] font-semibold tracking-wide uppercase text-[#9a6a35]">
                {activePartner.role} · {activePartner.practice}
              </div>
              <p className="text-[15px] sm:text-[16px] leading-[1.6] text-[#5b4a3b] max-w-xl">
                {activePartner.summary}
              </p>

              {/* Two Statistics */}
              <div className="grid grid-cols-2 gap-6 pt-4 max-w-md">
                <div>
                  <div className="text-[11.5px] uppercase tracking-wider text-[#85725f] font-sans">
                    Bar Standing
                  </div>
                  <div className="text-[15px] font-semibold text-[#2a1c12] mt-0.5 font-sans">
                    {activePartner.inPractice}
                  </div>
                </div>
                <div>
                  <div className="text-[11.5px] uppercase tracking-wider text-[#85725f] font-sans">
                    Primary Courts
                  </div>
                  <div className="text-[15px] font-semibold text-[#2a1c12] mt-0.5 font-sans">
                    {activePartner.admitted}
                  </div>
                </div>
              </div>
            </div>

            {/* List of Other Partners */}
            <div className="divide-y divide-[#e2d5c1]/70">
              {otherPartners.map((partner) => (
                <button
                  key={partner.id}
                  type="button"
                  onClick={() => setActivePartnerId(partner.id)}
                  className="w-full py-4 flex items-center justify-between text-left group transition-colors hover:text-[#9a6a35] cursor-pointer"
                >
                  <div className="flex items-baseline space-x-4">
                    <span className="font-mono text-xs text-[#85725f]">
                      {partner.num}
                    </span>
                    <span className="font-serif text-[20px] sm:text-[22px] text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors font-normal">
                      {partner.name}
                    </span>
                  </div>
                  <span className="text-[12.5px] font-sans text-[#85725f] group-hover:text-[#2a1c12] transition-colors">
                    {partner.practice}
                  </span>
                </button>
              ))}
            </div>

            {/* Find an Advocate link */}
            <div className="pt-6 border-t border-[#e2d5c1]">
              <Link
                href="/people"
                className="font-medium text-[14.5px] text-[#2a1c12] hover:text-[#9a6a35] underline underline-offset-4 transition-colors"
              >
                Find an Advocate across 28 High Courts
              </Link>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
