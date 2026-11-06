"use client";

import * as React from "react";
import Image from "next/image";
import { Container } from "@/components/layout/container";

interface LawyerNote {
  id: 1 | 2 | 3;
  name: string;
  role: string;
  avatar: string;
  quote: string;
  highlightText: string;
}

const lawyerNotes: LawyerNote[] = [
  {
    id: 1,
    name: "Adv. Rajeshwari Sen",
    role: "Supreme Court Advocate · note 1",
    avatar: "https://framerusercontent.com/images/0LArNLIabDDiZZoFMZhtVP1Dudc.webp?width=720&height=900",
    quote:
      "“Under Section 27 of the Indian Contract Act 1872, all agreements in restraint of trade, profession, or lawful business are void. Post-employment non-compete covenants cannot be enforced against employees in India.”",
    highlightText: "void under Section 27¹",
  },
  {
    id: 2,
    name: "Adv. Vikramaditya Deshmukh",
    role: "Corporate Counsel · note 2",
    avatar: "https://framerusercontent.com/images/aduozO96ZbkNp24VgIVFxOelF4.webp?width=720&height=900",
    quote:
      "“Indian courts do not award punitive contractual damages under Section 74. The employer must prove genuine actual financial injury, making arbitrary penalty sums legally unenforceable.”",
    highlightText: "reasonable compensation only²",
  },
  {
    id: 3,
    name: "Adv. Ananya Sundaram",
    role: "Commercial Litigator · note 3",
    avatar: "https://framerusercontent.com/images/aP4i3MQtE6NvStb54fOi7D2gxG8.webp?width=720&height=900",
    quote:
      "“Parties cannot confer jurisdiction on a court that inherently lacks territorial or pecuniary competence under the Code of Civil Procedure.”",
    highlightText: "courts where dispute arose³",
  },
];

export function ContractAnnotator() {
  const [activeNote, setActiveNote] = React.useState<1 | 2 | 3 | null>(null);

  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28 overflow-hidden">
      <Container size="xl">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center">
          {/* Left Column: Photograph with floating annotated contract sheet */}
          <div className="lg:col-span-6 relative">
            <div className="relative rounded-lg overflow-hidden border border-[#e2d5c1] shadow-[0_8px_30px_rgba(42,28,18,0.06)] aspect-[4/3] w-full">
              {/* Coffee table photograph */}
              <Image
                src="https://framerusercontent.com/images/1P4ZiDmUViRZSPDF7pkkL0gc.webp?width=1200&height=900"
                alt="Contract review desk with documents and annotations"
                fill
                sizes="(max-width: 1024px) 100vw, 50vw"
                className="object-cover object-center"
              />

              {/* Floating Annotated Document Card */}
              <div className="absolute inset-x-6 bottom-6 sm:inset-x-8 sm:bottom-8 bg-[#fffaf2]/95 backdrop-blur-md rounded-md p-5 sm:p-6 border border-[#e2d5c1] shadow-[0_12px_36px_rgba(42,28,18,0.14)]">
                <div className="flex items-center justify-between text-[11px] sm:text-[12px] text-[#85725f] pb-3 mb-3 border-b border-[#e2d5c1]/60 font-sans">
                  <span>Employment Agreement</span>
                  <span>Clause 14 · reviewed</span>
                </div>

                <h4 className="font-sans font-bold text-[14px] sm:text-[15px] text-[#2a1c12] mb-2.5">
                  Article 14. Restrictive Covenants
                </h4>

                <p className="font-serif text-[13px] sm:text-[14px] leading-[1.75] text-[#2a1c12]/90">
                  <span className="font-sans font-semibold text-[12px] text-[#85725f] mr-1.5">14.1</span>
                  Employee covenants that for twenty-four (24) months following separation, Employee shall not{" "}
                  <del className="text-[#a04e46] line-through decoration-[#a04e46]/60">
                    directly or indirectly join any competing business
                  </del>{" "}
                  <button
                    type="button"
                    onClick={() => setActiveNote(1)}
                    onMouseEnter={() => setActiveNote(1)}
                    className={`inline-block px-1 rounded-[2px] transition-all font-medium cursor-pointer ${
                      activeNote === 1
                        ? "bg-[#e89f97] text-[#6b1c15] ring-2 ring-[#a04e46]"
                        : "bg-[#fae2df] text-[#a04e46]"
                    }`}
                  >
                    void under Section 27¹
                  </button>{" "}
                  nor solicit clients, subject to liquidated damages of{" "}
                  <del className="text-[#a04e46] line-through decoration-[#a04e46]/60">
                    ₹25,00,000 penalty
                  </del>{" "}
                  <button
                    type="button"
                    onClick={() => setActiveNote(2)}
                    onMouseEnter={() => setActiveNote(2)}
                    className={`inline-block px-1 rounded-[2px] transition-all font-medium cursor-pointer ${
                      activeNote === 2
                        ? "bg-[#e89f97] text-[#6b1c15] ring-2 ring-[#a04e46]"
                        : "bg-[#fae2df] text-[#a04e46]"
                    }`}
                  >
                    reasonable compensation only²
                  </button>{" "}
                  with exclusive jurisdiction in{" "}
                  <del className="text-[#a04e46] line-through decoration-[#a04e46]/60">
                    foreign arbitration
                  </del>{" "}
                  <button
                    type="button"
                    onClick={() => setActiveNote(3)}
                    onMouseEnter={() => setActiveNote(3)}
                    className={`inline-block px-1 rounded-[2px] transition-all font-medium cursor-pointer ${
                      activeNote === 3
                        ? "bg-[#e89f97] text-[#6b1c15] ring-2 ring-[#a04e46]"
                        : "bg-[#fae2df] text-[#a04e46]"
                    }`}
                  >
                    courts where dispute arose³
                  </button>
                  .
                </p>
              </div>
            </div>
          </div>

          {/* Right Column: Title, Subhead, and 3 Lawyer Notes */}
          <div className="lg:col-span-6 space-y-6">
            <div>
              <h2 className="font-serif text-[40px] sm:text-[52px] lg:text-[60px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
                Reviewed by advocates
                <br />
                <span className="text-[#a89682]">who argue in court.</span>
              </h2>
              <p className="mt-4 text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6] max-w-xl">
                Most legal disputes in India turn on one-sided clauses buried in contracts. See how our AI and High Court advocates flag unconscionable terms before you sign.
              </p>
            </div>

            <div className="border-t border-[#e2d5c1] pt-6 space-y-6">
              {lawyerNotes.map((item) => {
                const isActive = activeNote === item.id;
                return (
                  <div
                    key={item.id}
                    onMouseEnter={() => setActiveNote(item.id)}
                    onClick={() => setActiveNote(item.id)}
                    className={`p-3.5 -mx-3.5 rounded-md transition-all cursor-pointer flex items-start space-x-4 ${
                      isActive
                        ? "bg-[#fffaf2] shadow-xs border border-[#e2d5c1]"
                        : "hover:bg-[#fffaf2]/50 border border-transparent"
                    }`}
                  >
                    {/* Lawyer Avatar */}
                    <div className="relative h-11 w-11 rounded-full overflow-hidden shrink-0 ring-1 ring-[#e2d5c1]">
                      <Image
                        src={item.avatar}
                        alt={item.name}
                        fill
                        className="object-cover object-[50%_18%]"
                      />
                    </div>

                    {/* Content */}
                    <div className="space-y-1">
                      <div className="flex items-baseline space-x-2">
                        <span className="font-sans font-bold text-[14.5px] text-[#2a1c12]">
                          {item.name}
                        </span>
                        <span className="text-[12px] text-[#85725f]">
                          {item.role}
                        </span>
                      </div>
                      <p className="text-[13.5px] leading-[1.6] text-[#5b4a3b]">
                        {item.quote}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
