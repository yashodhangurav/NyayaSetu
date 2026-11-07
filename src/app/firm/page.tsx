"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { firmTimeline, writtenCommitments, clientProfiles, proBonoDetails } from "@/data/firm";
import { CheckCircle2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function FirmPage() {
  const [activeMilestoneYear, setActiveMilestoneYear] = React.useState("2011");

  const currentMilestone = firmTimeline.find((m) => m.year === activeMilestoneYear) || firmTimeline[0];

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Header Hero */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div className="lg:col-span-7 space-y-6">
              <div className="flex items-center space-x-3">
                <Badge variant="stamp">THE FIRM</Badge>
                <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
                  224 S. LaSalle Street · 31st Floor
                </span>
              </div>

              <h1 className="font-serif text-[42px] sm:text-[64px] lg:text-[84px] leading-[0.95] tracking-[-0.045em] font-normal text-[#2a1c12]">
                Fifteen years on LaSalle Street.
              </h1>

              <p className="font-serif text-[22px] sm:text-[28px] leading-[1.2] text-[#5b4a3b]">
                Founded in 2011 on one foundational rule: the partner you hire is the one who does the work.
              </p>

              <div className="space-y-4 text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
                <p>
                  In 2011, federal prosecutor Margaret Ellery and national corporate M&A partner Tomasz Kowal left large law firms to establish a boutique focused entirely on courtroom trials, private company sales, and confidential investigations.
                </p>
                <p>
                  Today, seven equity partners and thirty-four counsel and associates occupy the 31st floor of 224 S. LaSalle Street. We have tried 34 cases to verdict, completed over sixty company sales, and kept 92% of active litigation matters within their original written budget caps.
                </p>
              </div>

              <div className="pt-2 flex flex-wrap gap-4">
                <Link href="/people">
                  <Button variant="primary" size="lg">
                    Meet the Partners
                  </Button>
                </Link>
                <Link href="/matters">
                  <Button variant="outline" size="lg">
                    View Case Ledger
                  </Button>
                </Link>
              </div>
            </div>

            {/* Architecture Images (5 cols) */}
            <div className="lg:col-span-5 grid grid-cols-2 gap-4">
              <div className="relative aspect-[3/4] overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1]">
                <Image
                  src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=960"
                  alt="224 S. LaSalle facade"
                  fill
                  sizes="(max-width: 600px) 50vw, 25vw"
                  className="object-cover object-center filter contrast-[1.02]"
                />
                <div className="absolute bottom-2 left-2 right-2 bg-[#2a1c12]/80 px-2 py-1 text-[10px] uppercase font-mono tracking-wider text-[#fffaf2]">
                  LaSalle Facade
                </div>
              </div>

              <div className="relative aspect-[3/4] overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1]">
                <Image
                  src="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200"
                  alt="31st Floor conference suite"
                  fill
                  sizes="(max-width: 600px) 50vw, 25vw"
                  className="object-cover object-center filter contrast-[1.02]"
                />
                <div className="absolute bottom-2 left-2 right-2 bg-[#2a1c12]/80 px-2 py-1 text-[10px] uppercase font-mono tracking-wider text-[#fffaf2]">
                  31st Floor Suite
                </div>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. Interactive 15-Year Historical Timeline (2011–2026) */}
      <section className="py-16 sm:py-20 lg:py-28 border-b border-[#e2d5c1]">
        <Container size="xl">
          <div className="max-w-3xl space-y-4 mb-12">
            <Badge variant="stamp">HISTORICAL TIMELINE</Badge>
            <h2 className="font-serif text-[32px] sm:text-[44px] font-normal leading-[1.0] text-[#2a1c12]">
              15 Years of Landmark Representation
            </h2>
            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6]">
              Trace the evolution of Ellery Kowal LLP from a two-lawyer boutique to LaSalle Street’s premier commercial litigation and M&A practice.
            </p>
          </div>

          {/* Stepper Year Pills */}
          <div className="flex border border-[#e2d5c1] bg-[#ebe1d1]/50 p-1.5 overflow-x-auto hide-scrollbar gap-2 mb-8">
            {firmTimeline.map((item) => {
              const isActive = item.year === activeMilestoneYear;
              return (
                <button
                  key={item.year}
                  type="button"
                  onClick={() => setActiveMilestoneYear(item.year)}
                  className={`px-5 py-2.5 text-xs font-mono uppercase tracking-wider font-semibold transition-colors cursor-pointer shrink-0 ${
                    isActive
                      ? "bg-[#2a1c12] text-[#fffaf2]"
                      : "text-[#5b4a3b] hover:text-[#2a1c12] hover:bg-[#fffaf2]/60"
                  }`}
                >
                  {item.year}
                </button>
              );
            })}
          </div>

          {/* Active Milestone Card */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentMilestone.year}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
              className="border border-[#e2d5c1] bg-[#fffaf2] p-8 sm:p-12 shadow-[0_4px_24px_rgba(42,28,18,0.04)]"
            >
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                <div className="lg:col-span-4 space-y-3">
                  <div className="font-serif text-6xl text-[#9a6a35] font-normal">
                    {currentMilestone.year}
                  </div>
                  <Badge variant="gold">MILESTONE</Badge>
                </div>

                <div className="lg:col-span-8 space-y-4">
                  <h3 className="font-serif text-2xl sm:text-3xl font-normal text-[#2a1c12]">
                    {currentMilestone.title}
                  </h3>
                  <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
                    {currentMilestone.description}
                  </p>

                  {currentMilestone.keyMatters && (
                    <div className="pt-4 border-t border-[#e2d5c1] space-y-2">
                      <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                        Notable Matters That Year:
                      </div>
                      <ul className="space-y-1.5 text-xs sm:text-sm text-[#2a1c12]">
                        {currentMilestone.keyMatters.map((km, kmi) => (
                          <li key={kmi} className="flex items-center space-x-2">
                            <span className="text-[#9a6a35] font-bold">—</span>
                            <span>{km}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </Container>
      </section>

      {/* 3. Four Written Operational Commitments */}
      <section className="py-16 sm:py-20 lg:py-28 border-b border-[#e2d5c1] bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="max-w-3xl space-y-4 mb-14">
            <Badge variant="stamp">OPERATIONAL INTEGRITY</Badge>
            <h2 className="font-serif text-[34px] sm:text-[48px] lg:text-[58px] leading-[0.98] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Written commitments, not marketing promises.
            </h2>
            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6]">
              Every client engagement is governed by four enforceable operational policies delivered before representation begins.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {writtenCommitments.map((c) => (
              <div
                key={c.id}
                className="border border-[#e2d5c1] bg-[#fffaf2] p-8 flex flex-col justify-between shadow-[0_4px_20px_rgba(42,28,18,0.03)] hover:border-[#cfbe9e] transition-colors"
              >
                <div>
                  <div className="flex items-center justify-between border-b border-[#e2d5c1] pb-4 mb-5">
                    <span className="font-serif text-3xl font-normal text-[#9a6a35]">
                      {c.number}
                    </span>
                    <Badge variant="stamp">POLICY ARTIFACT</Badge>
                  </div>

                  <h3 className="font-serif text-[24px] font-normal leading-[1.15] text-[#2a1c12]">
                    {c.title}
                  </h3>

                  <p className="mt-3 text-sm text-[#2a1c12] font-medium leading-relaxed">
                    {c.summary}
                  </p>

                  <p className="mt-3 text-xs text-[#5b4a3b] leading-[1.65]">
                    {c.fullPolicy}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-[#e2d5c1] flex items-center justify-between text-xs font-mono text-[#85725f]">
                  <span className="truncate max-w-[280px]">{c.artifactTitle}</span>
                  <CheckCircle2 className="h-4 w-4 text-[#9a6a35] shrink-0" />
                </div>
              </div>
            ))}
          </div>
        </Container>
      </section>

      {/* 4. Client Archetypes */}
      <section className="py-16 sm:py-20 lg:py-28 border-b border-[#e2d5c1]">
        <Container size="xl">
          <div className="max-w-3xl space-y-4 mb-14">
            <Badge variant="stamp">WHO WE SERVE</Badge>
            <h2 className="font-serif text-[34px] sm:text-[48px] lg:text-[58px] leading-[0.98] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Three client profiles.
            </h2>
            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6]">
              Our lean staffing model is tailored specifically for companies where legal outcomes affect enterprise survival or family wealth.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {clientProfiles.map((cp) => (
              <div
                key={cp.id}
                className="border border-[#e2d5c1] bg-[#fffaf2] p-8 space-y-6 flex flex-col justify-between shadow-[0_4px_20px_rgba(42,28,18,0.03)]"
              >
                <div>
                  <h3 className="font-serif text-2xl font-normal leading-tight text-[#2a1c12] border-b border-[#e2d5c1] pb-4">
                    {cp.title}
                  </h3>
                  <p className="mt-4 text-xs sm:text-sm text-[#5b4a3b] leading-relaxed">
                    {cp.description}
                  </p>

                  <div className="mt-6 pt-4 border-t border-[#e2d5c1]/60 space-y-2">
                    <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                      Typical Engagements:
                    </div>
                    <ul className="space-y-1.5 text-xs text-[#2a1c12]">
                      {cp.typicalMatters.map((tm, tmi) => (
                        <li key={tmi} className="flex items-start">
                          <span className="mr-2 text-[#9a6a35]">•</span>
                          <span>{tm}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="pt-4 border-t border-[#e2d5c1]">
                  <Link href="/contact" className="text-xs font-semibold uppercase tracking-wider text-[#9a6a35] hover:underline">
                    Discuss Your Matter →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </Container>
      </section>

      {/* 5. LaSalle Street Pro Bono Legal Clinic */}
      <section className="py-16 sm:py-24 bg-[#24180f] text-[#f3ece1] border-t border-[#3f2c1f]">
        <Container size="xl">
          <div className="border border-[#3f2c1f] bg-[#2f2116] p-8 sm:p-12">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              <div className="lg:col-span-8 space-y-4">
                <div className="flex items-center space-x-3">
                  <Badge variant="dark">COMMUNITY COMMITMENT</Badge>
                  <span className="text-xs font-mono text-[#d1a46a]">Founded {proBonoDetails.founded}</span>
                </div>

                <h3 className="font-serif text-3xl sm:text-4xl font-normal text-[#f3ece1]">
                  {proBonoDetails.title}
                </h3>

                <p className="text-sm sm:text-base text-[#b8a695] leading-relaxed">
                  {proBonoDetails.mission}
                </p>

                <div className="flex flex-wrap items-center gap-6 pt-2 text-xs font-mono text-[#d1a46a]">
                  <span>Annual Commitment: {proBonoDetails.hoursAnnually}</span>
                  <span>·</span>
                  <span>Lead Partners: {proBonoDetails.partnerInCharge}</span>
                </div>
              </div>

              <div className="lg:col-span-4 flex flex-col justify-center items-start lg:items-end">
                <div className="p-6 border border-[#3f2c1f] bg-[#24180f] space-y-3 w-full max-w-sm">
                  <div className="text-xs uppercase tracking-wider font-mono text-[#d1a46a]">
                    Clinic Inquiries:
                  </div>
                  <div className="text-sm text-[#f3ece1] font-mono">
                    {proBonoDetails.contactEmail}
                  </div>
                  <p className="text-[11px] text-[#85725f] leading-relaxed">
                    Held second Friday of each month at 224 S. LaSalle, 31st Floor. Advance registration required.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </Container>
      </section>
    </div>
  );
}

