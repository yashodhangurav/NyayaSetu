"use client";

import * as React from "react";
import Image from "next/image";
import { Container } from "@/components/layout/container";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface ClientQuote {
  id: string;
  practiceTag: string;
  image: string;
  quote: string;
  authorTitle: string;
  clientContext: string;
}

const clientQuotesList: ClientQuote[] = [
  {
    id: "q-1",
    practiceTag: "Civil & Property",
    image: "https://framerusercontent.com/images/1P4ZiDmUViRZSPDF7pkkL0gc.webp?width=1200&height=900",
    quote: "“When our landlord refused to return our security deposit, NyayaSetu’s AI evaluated the tenancy agreement and generated a formal statutory demand. We matched with a local advocate, and the deposit was credited within a week.”",
    authorTitle: "Software Engineer & Tenant",
    clientContext: "Bengaluru · Consulted November 2025",
  },
  {
    id: "q-2",
    practiceTag: "Startup & Corporate",
    image: "https://framerusercontent.com/images/WzoMN0cZR1mFFYB1iI5EK9yVJ6I.webp?width=1200&height=900",
    quote: "“Before taking our first institutional angel check, we used NyayaSetu to assess our co-founder agreement. The advocate we matched with caught a reverse-vesting ambiguity that saved us months of future friction.”",
    authorTitle: "Co-Founder & CEO",
    clientContext: "D2C Brand, Mumbai · Consulted October 2025",
  },
  {
    id: "q-3",
    practiceTag: "Cheque Bounce & Debt",
    image: "https://framerusercontent.com/images/liEbKSf6YjDEu7fliChEDT6SQSw.webp?width=1200&height=900",
    quote: "“Our vendor defaulted on ₹14 Lakh of payments. Within 24 hours of uploading the return memo, we received an accurate statutory notice draft. The debtor settled within the 15-day cure window without court litigation.”",
    authorTitle: "Director of Operations",
    clientContext: "Manufacturing MSME, Pune · Consulted August 2025",
  },
  {
    id: "q-4",
    practiceTag: "Consumer & Cyber",
    image: "https://framerusercontent.com/images/6qS34tlW6OMwiM6MECqiTnffU.webp?width=1200&height=900",
    quote: "“After an unauthorized bank debit of ₹1.8 Lakh, the platform guided us through the RBI 72-hour zero-liability window and generated the Ombudsman petition. The full amount was reimbursed by the bank.”",
    authorTitle: "Small Business Owner",
    clientContext: "New Delhi · Consulted July 2025",
  },
  {
    id: "q-5",
    practiceTag: "Employment & Labor",
    image: "https://framerusercontent.com/images/MX27nh2ggEqrOo8VishzkP6djaU.webp?width=1200&height=900",
    quote: "“My previous employer sent a legal notice threatening a ₹20 Lakh penalty for a 2-year non-compete clause. The advocate explained Section 27 and replied firmly. The former employer withdrew their claim immediately.”",
    authorTitle: "Senior Product Manager",
    clientContext: "Hyderabad · Consulted May 2025",
  },
];

export function ClientQuotes() {
  const [activeIndex, setActiveIndex] = React.useState(0);

  const current = clientQuotesList[activeIndex];

  const handlePrev = () => {
    setActiveIndex((prev) => (prev === 0 ? clientQuotesList.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setActiveIndex((prev) => (prev === clientQuotesList.length - 1 ? 0 : prev + 1));
  };

  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-12 sm:mb-16 gap-4">
          <h2 className="font-serif text-[40px] sm:text-[52px] lg:text-[62px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
            What citizens
            <br />
            <span className="text-[#a89682]">tell us.</span>
          </h2>

          <p className="text-[13px] text-[#85725f]">
            Shared with permission. Real outcomes from individuals, MSMEs, and startups across India.
          </p>
        </div>

        {/* Featured Card */}
        <div className="border border-[#e2d5c1] bg-[#ffffff] rounded-lg overflow-hidden shadow-[0_8px_30px_rgba(42,28,18,0.06)] grid grid-cols-1 lg:grid-cols-12">
          {/* Left Column: Image with Tag */}
          <div className="lg:col-span-5 relative aspect-[4/3] lg:aspect-auto min-h-[300px]">
            <Image
              src={current.image}
              alt={current.practiceTag}
              fill
              className="object-cover object-center"
            />
            <div className="absolute bottom-4 left-4 z-10">
              <span className="px-3 py-1 bg-[#fffaf2]/90 backdrop-blur-xs border border-[#e2d5c1] text-xs font-medium text-[#2a1c12] rounded-[2px]">
                {current.practiceTag}
              </span>
            </div>
          </div>

          {/* Right Column: Quote Text, Attribution, Controls */}
          <div className="lg:col-span-7 p-8 sm:p-12 lg:p-16 flex flex-col justify-between space-y-8">
            <div className="space-y-6">
              <p className="font-serif text-[24px] sm:text-[30px] lg:text-[34px] leading-[1.25] text-[#2a1c12] font-normal tracking-tight">
                {current.quote}
              </p>

              <div>
                <div className="font-sans font-bold text-[15px] text-[#2a1c12]">
                  {current.authorTitle}
                </div>
                <div className="text-[13px] text-[#85725f] mt-0.5">
                  {current.clientContext}
                </div>
              </div>
            </div>

            {/* Bottom Controls: Dash Indicators on Left, Arrows on Right */}
            <div className="flex items-center justify-between pt-6 border-t border-[#e2d5c1]/60">
              {/* 5 Progress Dashes */}
              <div className="flex items-center space-x-2">
                {clientQuotesList.map((_, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setActiveIndex(idx)}
                    className={`h-[2px] transition-all cursor-pointer ${
                      idx === activeIndex
                        ? "w-8 bg-[#2a1c12]"
                        : "w-5 bg-[#e2d5c1] hover:bg-[#85725f]"
                    }`}
                    aria-label={`Go to testimonial ${idx + 1}`}
                  />
                ))}
              </div>

              {/* Square Navigation Arrows */}
              <div className="flex items-center space-x-2">
                <button
                  type="button"
                  onClick={handlePrev}
                  className="p-2.5 border border-[#e2d5c1] bg-[#faf7f2] hover:bg-[#ebe1d1] text-[#2a1c12] transition-colors rounded-[2px] cursor-pointer"
                  aria-label="Previous quote"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>
                <button
                  type="button"
                  onClick={handleNext}
                  className="p-2.5 border border-[#e2d5c1] bg-[#faf7f2] hover:bg-[#ebe1d1] text-[#2a1c12] transition-colors rounded-[2px] cursor-pointer"
                  aria-label="Next quote"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
