"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { ArrowRight, ChevronDown, Check } from "lucide-react";

interface PartnerProfile {
  name: string;
  practice: string;
  avatar: string;
}

const partnersList: PartnerProfile[] = [
  {
    name: "Adv. Rajeshwari Sen",
    practice: "Civil & Property Law",
    avatar: "https://framerusercontent.com/images/0LArNLIabDDiZZoFMZhtVP1Dudc.webp?width=720&height=900",
  },
  {
    name: "Adv. Vikramaditya Deshmukh",
    practice: "Startup & Corporate Law",
    avatar: "https://framerusercontent.com/images/aduozO96ZbkNp24VgIVFxOelF4.webp?width=720&height=900",
  },
  {
    name: "Adv. Harshvardhan Kapoor",
    practice: "Criminal Defense & Bail",
    avatar: "https://framerusercontent.com/images/aP4i3MQtE6NvStb54fOi7D2gxG8.webp?width=720&height=900",
  },
  {
    name: "Adv. Ananya Sundaram",
    practice: "Consumer & Cyber Law",
    avatar: "https://framerusercontent.com/images/9wg0juCfo5rrwm9BHnLZFuKX3g.webp?width=720&height=900",
  },
];

const workOptions = [
  {
    title: "Section 138 NI Act statutory legal notice (Cheque Bounce)",
    price: "₹2,499",
    turnaround: "flat fee, delivered in 3 business days",
    deliverables: [
      "Statutory 15-day demand notice drafting",
      "Bar Council verified advocate sign-off",
      "Dispatch via Registered Speed Post & email",
      "Online tracking ID & proof of service logged",
    ],
  },
  {
    title: "Co-founder agreement & reverse vesting deed",
    price: "₹4,999",
    turnaround: "flat fee, delivered in 4 business days",
    deliverables: [
      "Custom equity split & 4-year vesting schedule",
      "IP assignment deed & confidentiality covenant",
      "Deadlock resolution & dispute protocols",
      "30-minute advocate video review call",
    ],
  },
  {
    title: "RERA builder delay refund & interest petition",
    price: "₹5,999",
    turnaround: "flat fee, delivered in 5 business days",
    deliverables: [
      "Statutory delay calculation under Section 18 RERA",
      "Affidavit and complaint draft for RERA tribunal",
      "Index of builder receipts and correspondence",
      "Filing guidance before the State Authority",
    ],
  },
];

export function TransparencyPreview() {
  const [selectedPartnerIndex, setSelectedPartnerIndex] = React.useState(0);
  const [selectedWorkIndex, setSelectedWorkIndex] = React.useState(0);
  const [dateVal, setDateVal] = React.useState("");
  const [timeVal, setTimeVal] = React.useState("11:30 AM IST");
  const [nameVal, setNameVal] = React.useState("");
  const [contactVal, setContactVal] = React.useState("");
  const [submitted, setSubmitted] = React.useState(false);

  const selectedPartner = partnersList[selectedPartnerIndex];
  const selectedWork = workOptions[selectedWorkIndex];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        {/* Centered Editorial Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 sm:mb-20">
          <h2 className="font-serif text-[40px] sm:text-[54px] lg:text-[64px] leading-[1.02] tracking-[-0.035em] font-normal text-[#2a1c12]">
            Know your options, the cost
            <br />
            <span className="text-[#a89682]">and the next step.</span>
          </h2>
        </div>

        {/* 3-Card Showcase Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8 items-start">
          {/* Card 1: 30-min Advocate Consultation Scheduler */}
          <div className="border border-[#e2d5c1] bg-[#ffffff] rounded-lg p-6 sm:p-7 shadow-[0_4px_24px_rgba(42,28,18,0.04)] flex flex-col justify-between">
            <div>
              {/* Header */}
              <div className="flex items-center justify-between text-[12px] pb-4 mb-5 border-b border-[#e2d5c1]/60">
                <span className="font-medium text-[#2a1c12]">
                  Advocate Consultation · 30 minutes
                </span>
                <span className="text-[#85725f]">Indian Standard Time</span>
              </div>

              {/* Partner Avatar Selector */}
              <div className="flex items-center space-x-2.5 mb-4">
                {partnersList.map((p, idx) => (
                  <button
                    key={p.name}
                    type="button"
                    onClick={() => setSelectedPartnerIndex(idx)}
                    className={`relative h-10 w-10 rounded-full overflow-hidden transition-all cursor-pointer ${
                      selectedPartnerIndex === idx
                        ? "ring-2 ring-[#9a6a35] scale-105"
                        : "opacity-60 hover:opacity-100 ring-1 ring-[#e2d5c1]"
                    }`}
                    aria-label={`Select ${p.name}`}
                  >
                    <Image
                      src={p.avatar}
                      alt={p.name}
                      fill
                      className="object-cover object-[50%_18%]"
                    />
                  </button>
                ))}
              </div>

              {/* Selected Partner Display */}
              <div className="mb-6">
                <h3 className="font-serif text-[22px] font-normal text-[#2a1c12] leading-tight">
                  {selectedPartner.name}
                </h3>
                <p className="text-[12.5px] text-[#85725f] mt-0.5">
                  {selectedPartner.practice}
                </p>
              </div>

              {/* Booking Form Inputs */}
              <form onSubmit={handleSubmit} className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <input
                      type="text"
                      placeholder="dd/mm/yyyy"
                      value={dateVal}
                      onChange={(e) => setDateVal(e.target.value)}
                      className="w-full text-[13px] px-3 py-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#faf7f2] text-[#2a1c12] placeholder:text-[#a89682] focus:border-[#2a1c12] focus:outline-hidden"
                    />
                  </div>
                  <div className="relative">
                    <select
                      value={timeVal}
                      onChange={(e) => setTimeVal(e.target.value)}
                      className="w-full text-[13px] px-3 py-2.5 pr-8 rounded-[2px] border border-[#e2d5c1] bg-[#faf7f2] text-[#2a1c12] appearance-none focus:border-[#2a1c12] focus:outline-hidden"
                    >
                      <option value="10:30 AM IST">10:30 AM IST</option>
                      <option value="12:00 PM IST">12:00 PM IST</option>
                      <option value="2:30 PM IST">2:30 PM IST</option>
                      <option value="4:30 PM IST">4:30 PM IST</option>
                      <option value="6:00 PM IST">6:00 PM IST</option>
                    </select>
                    <ChevronDown className="h-3.5 w-3.5 text-[#85725f] absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <input
                      type="text"
                      placeholder="Your name"
                      value={nameVal}
                      onChange={(e) => setNameVal(e.target.value)}
                      className="w-full text-[13px] px-3 py-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#faf7f2] text-[#2a1c12] placeholder:text-[#a89682] focus:border-[#2a1c12] focus:outline-hidden"
                    />
                  </div>
                  <div>
                    <input
                      type="text"
                      placeholder="Phone or email"
                      value={contactVal}
                      onChange={(e) => setContactVal(e.target.value)}
                      className="w-full text-[13px] px-3 py-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#faf7f2] text-[#2a1c12] placeholder:text-[#a89682] focus:border-[#2a1c12] focus:outline-hidden"
                    />
                  </div>
                </div>

                {/* Subtitle / Venue Note */}
                <p className="text-[12px] text-[#85725f] pt-2">
                  With {selectedPartner.name}, via video call or chamber consultation
                </p>

                {/* Compound Action Button */}
                <div className="pt-2">
                  {submitted ? (
                    <div className="p-3 bg-[#e8efe7] text-[#2d5a27] text-xs font-medium rounded-[2px] text-center">
                      Requested! Your consultation details will be confirmed via SMS & email.
                    </div>
                  ) : (
                    <button
                      type="submit"
                      className="group inline-flex items-center w-full justify-between bg-[#2a1c12] text-[#fffaf2] hover:bg-[#9a6a35] transition-colors rounded-[2px] overflow-hidden"
                    >
                      <span className="px-4 py-3 text-[14px] font-medium tracking-tight">
                        Request this consultation
                      </span>
                      <span className="flex items-center justify-center w-10 py-3 border-l border-white/20 bg-[#fffaf2]/10 group-hover:bg-[#fffaf2]/20 transition-colors">
                        <ArrowRight className="h-4 w-4" />
                      </span>
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          {/* Card 2: Schedule A Fixed Fees Document Sheet */}
          <div className="border border-[#e2d5c1] bg-[#ffffff] rounded-lg p-6 sm:p-7 shadow-[0_4px_24px_rgba(42,28,18,0.04)] flex flex-col justify-between">
            <div>
              {/* Header */}
              <div className="flex items-center justify-between text-[12px] pb-4 mb-5 border-b border-[#e2d5c1]/60">
                <span className="font-medium text-[#2a1c12]">
                  Schedule A · Fixed fees
                </span>
                {/* Monogram SVG */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="-242 -690 975 700"
                  className="h-4 w-auto shrink-0"
                >
                  <path
                    fill="#9a6a35"
                    d="M179.56-333.16v-39.8H41.6q-36.04 0-55.94-4.28t-30.32-14.56-16.02-28.78-12.6-46.5h-29.04v228.04h29.04q7-27.44 12.6-45.72t16.02-29.06 30.32-15.06 55.94-4.28ZM-128.6-38.48l-73.04-155.28h-30.16L-212.36 0h515.24v-28.48q-33.2-4.44-49.54-9.5t-22.9-16.74q-7.56-12.56-9.06-36.06t-1.5-64.58v-369.28q0-44.44 1.78-68.22t11.02-36.34q7.12-10.44 23.18-14.94t47.02-6.82V-680h-499.12l-10 176.92h30.16l63.04-138.44h235v603.04Z"
                  />
                  <path
                    fill="#2a1c12"
                    d="m204-275-52-2.4 314.72-292.68q20.44-19 30.94-28.72t10.5-21.72q0-14-14.48-21t-41.28-10V-680q31 2 59.04 3t56.68 1q27.4 0 56.8-1t75.04-3v28.48q-32.56 4-56.38 11.32t-45.98 21.76-51.52 40.36Zm79.96-107.72 76.56-56.88 204.56 299.4q27.12 36.36 45.96 57.7t34.64 31.8 33.92 15.12 43.36 7.66V.44q-40.48-2-61.84-2.66t-39.08-.66q-17.68 0-36.16.72T547.96 0Zm-63-163.2v411.84q0 30.36 1.5 49.32t6.94 29.28q7.56 13 24.8 17.78t50.68 9.22V0q-32.04-2-52.12-2.5t-37.84-1-44.4-.5q-24.88 0-42.26.5t-36.96 1T39.12 0v-28.48q32.12-4.44 49.8-9t25.24-17.24q6.32-10.32 7.82-29.28t1.5-51.08v-409.84q0-32.12-1.72-51.08t-7.6-29.28q-7.56-12.68-25.24-17.46t-49.8-8.78V-680q32.6 1 52.18 2t36.96 1.5 42.26.5q26.64 0 44.4-.5t37.84-1.5 52.12-2v28.48q-33.44 4-50.46 8.5t-25.02 18.5q-5.88 10.32-7.16 29t-1.28 49.6"
                  />
                </svg>
              </div>

              {/* The Work Select */}
              <div className="mb-6">
                <label className="block text-[11px] uppercase tracking-wider text-[#85725f] mb-1.5">
                  The service
                </label>
                <div className="relative">
                  <select
                    value={selectedWorkIndex}
                    onChange={(e) => setSelectedWorkIndex(Number(e.target.value))}
                    className="w-full text-[13px] px-3.5 py-2.5 pr-8 rounded-[2px] border border-[#e2d5c1] bg-[#faf7f2] text-[#2a1c12] appearance-none focus:border-[#2a1c12] focus:outline-hidden font-medium"
                  >
                    {workOptions.map((w, idx) => (
                      <option key={w.title} value={idx}>
                        {w.title}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="h-3.5 w-3.5 text-[#85725f] absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                </div>
              </div>

              {/* Pricing Display */}
              <div className="mb-6">
                <div className="font-serif text-[42px] font-normal text-[#2a1c12] leading-none">
                  {selectedWork.price}
                </div>
                <div className="text-[13px] text-[#85725f] mt-2">
                  {selectedWork.turnaround}
                </div>
              </div>

              {/* Dashed Separator */}
              <div className="border-t border-dashed border-[#e2d5c1] my-5" />

              {/* Checklist */}
              <ul className="space-y-2.5 text-[13px] text-[#5b4a3b]">
                {selectedWork.deliverables.map((item) => (
                  <li key={item} className="flex items-start">
                    <span className="text-[#9a6a35] mr-2 text-[14px] leading-tight font-bold">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Card 3: AI Case Dossier Report */}
          <div className="border border-[#e2d5c1] bg-[#ffffff] rounded-lg p-6 sm:p-7 shadow-[0_4px_24px_rgba(42,28,18,0.04)] flex flex-col justify-between">
            <div>
              {/* Header */}
              <div className="flex items-center justify-between text-[12px] pb-4 mb-5 border-b border-[#e2d5c1]/60">
                <span className="font-medium text-[#2a1c12]">AI Case Dossier</span>
                <span className="text-[#85725f]">Instant Evaluation</span>
              </div>

              {/* Salutation & Body Paragraph */}
              <h3 className="font-serif text-[20px] font-normal text-[#2a1c12] mb-3">
                Case Assessment · Tenancy Deposit
              </h3>
              <p className="text-[13.5px] leading-[1.6] text-[#5b4a3b] mb-6">
                Landlord has withheld <strong className="font-semibold text-[#2a1c12]">₹1,40,000 security deposit</strong> for 38 days without itemized deductions. Under state rent laws and Section 73 of the Indian Contract Act, retention without lawful cause entitles tenant to 12% statutory interest.
              </p>

              {/* Progress Bar */}
              <div className="space-y-1.5 mb-6">
                <div className="w-full bg-[#f4efe6] h-1.5 rounded-full overflow-hidden">
                  <div className="bg-[#9a6a35] h-full w-[78%]" />
                </div>
                <div className="text-[12px] text-[#85725f]">
                  78% Legal Merit Score
                </div>
              </div>

              {/* Dashed Separator */}
              <div className="border-t border-dashed border-[#e2d5c1] my-5" />

              {/* Timeline Items */}
              <div className="space-y-2.5 text-[12.5px]">
                <div className="grid grid-cols-12 gap-2 text-[#5b4a3b]">
                  <span className="col-span-3 font-mono text-[#85725f]">Step 1</span>
                  <span className="col-span-9 text-[#2a1c12]">AI formal demand notice generated</span>
                </div>
                <div className="grid grid-cols-12 gap-2 text-[#5b4a3b]">
                  <span className="col-span-3 font-mono text-[#85725f]">Step 2</span>
                  <span className="col-span-9 text-[#2a1c12]">Speed post delivery tracking recorded</span>
                </div>
                <div className="grid grid-cols-12 gap-2 text-[#5b4a3b]">
                  <span className="col-span-3 font-mono text-[#85725f]">Step 3</span>
                  <span className="col-span-9 text-[#2a1c12]">15-day statutory cure window logged</span>
                </div>
              </div>

              {/* Dashed Separator */}
              <div className="border-t border-dashed border-[#e2d5c1] my-5" />

              {/* Next Phase Callout */}
              <p className="text-[13px] leading-relaxed text-[#5b4a3b]">
                Next: <strong className="font-semibold text-[#2a1c12]">Summary recovery suit in Small Causes Court</strong>. Verified advocate briefing prepared.
              </p>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
