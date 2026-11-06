"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { practices } from "@/data/practices";
import { partners } from "@/data/lawyers";
import { ArrowRight, CheckCircle2, Phone, Mail, Scale } from "lucide-react";
import { QuickConsultationModal } from "@/components/ui/quick-consultation-modal";

export default function PracticesPage() {
  const [modalOpen, setModalOpen] = React.useState(false);
  const [selectedPractice, setSelectedPractice] = React.useState("Trials & Disputes");

  const handleOpenScope = (practiceTitle: string) => {
    setSelectedPractice(practiceTitle);
    setModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Practices Header Hero */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="max-w-3xl space-y-6">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">OUR PRACTICES</Badge>
              <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
                LaSalle Street · Chicago
              </span>
            </div>

            <h1 className="font-serif text-[42px] sm:text-[64px] lg:text-[84px] leading-[0.95] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Six practices, one floor.
            </h1>

            <p className="font-serif text-[22px] sm:text-[28px] leading-[1.2] text-[#5b4a3b]">
              Every practice is led by a named partner with over fifteen years in Chicago courtrooms and boardrooms.
            </p>

            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
              We do not maintain associate leverage pyramids. When you retain Ellery Kowal, the partner whose name is on the door personally conducts your depositions, drafts your purchase agreements, and argues your motions.
            </p>
          </div>

          {/* Sticky Anchor Navigation Bar */}
          <div className="mt-12 pt-8 border-t border-[#e2d5c1] flex flex-wrap gap-2 sm:gap-3">
            {practices.map((p) => (
              <a
                key={p.id}
                href={`#${p.slug}`}
                className="px-4 py-2 border border-[#e2d5c1] bg-[#fffaf2] text-xs uppercase font-sans tracking-[0.1em] font-medium text-[#2a1c12] hover:bg-[#2a1c12] hover:text-[#fffaf2] transition-colors"
              >
                {p.num} {p.title}
              </a>
            ))}
          </div>
        </Container>
      </section>

      {/* 2. Detailed Practice Dossiers */}
      <div className="divide-y divide-[#e2d5c1]">
        {practices.map((practice) => {
          // Find lead partner objects
          const leadPartners = partners.filter((pt) =>
            (practice.partnerIds || []).includes(pt.id)
          );

          return (
            <section
              key={practice.id}
              id={practice.slug}
              className="py-16 sm:py-20 lg:py-28 scroll-mt-24 transition-colors"
            >
              <Container size="xl">
                {/* Practice Header Strip */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-12">
                  <div className="lg:col-span-8 space-y-4">
                    <div className="flex items-center space-x-4">
                      <span className="font-serif text-4xl text-[#9a6a35]">
                        {practice.num}
                      </span>
                      <Badge variant="gold">{practice.startingFee}</Badge>
                      <span className="text-xs font-mono text-[#85725f]">
                        {practice.feeType}
                      </span>
                    </div>

                    <h2 className="font-serif text-[36px] sm:text-[48px] lg:text-[56px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
                      {practice.title}
                    </h2>

                    <p className="font-serif italic text-[20px] sm:text-[24px] text-[#5b4a3b] leading-[1.25]">
                      “{practice.tagline}”
                    </p>

                    <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65] max-w-2xl pt-2">
                      {practice.description}
                    </p>
                  </div>

                  {/* Fee Basis Callout Card */}
                  <div className="lg:col-span-4 border border-[#e2d5c1] bg-[#fffaf2] p-6 space-y-3 shadow-[0_4px_20px_rgba(42,28,18,0.03)]">
                    <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                      Billing Model & Structure
                    </div>
                    <div className="font-sans font-medium text-sm text-[#2a1c12]">
                      {practice.feeBasis}
                    </div>
                    <p className="text-xs text-[#5b4a3b] leading-relaxed">
                      {practice.feeDetail}
                    </p>
                    <div className="pt-3 border-t border-[#e2d5c1]">
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full"
                        onClick={() => handleOpenScope(practice.title)}
                      >
                        Request Scope & Fee Schedule
                      </Button>
                    </div>
                  </div>
                </div>

                {/* 3 Scope Columns Grid: What We Handle / When Clients Call / Notable Results */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8 pt-8 border-t border-[#e2d5c1]">
                  {/* Column 1: What We Handle */}
                  <div className="border border-[#e2d5c1] bg-[#fffaf2] p-6 space-y-4">
                    <div className="text-xs uppercase tracking-[0.14em] font-medium text-[#2a1c12] border-b border-[#e2d5c1] pb-3">
                      What We Handle
                    </div>
                    <ul className="space-y-3 text-xs sm:text-sm text-[#5b4a3b]">
                      {(practice.whatWeHandle || []).map((item, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="mr-2.5 text-[#9a6a35] font-bold">—</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Column 2: When Clients Call */}
                  <div className="border border-[#e2d5c1] bg-[#fffaf2] p-6 space-y-4">
                    <div className="text-xs uppercase tracking-[0.14em] font-medium text-[#2a1c12] border-b border-[#e2d5c1] pb-3">
                      When Clients Call Us
                    </div>
                    <ul className="space-y-3 text-xs sm:text-sm text-[#5b4a3b]">
                      {(practice.whenClientsCall || []).map((item, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="mr-2.5 text-[#9a6a35] font-bold">→</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Column 3: Lead Partners & Forums */}
                  <div className="border border-[#e2d5c1] bg-[#ebe1d1]/50 p-6 space-y-4">
                    <div className="text-xs uppercase tracking-[0.14em] font-medium text-[#2a1c12] border-b border-[#e2d5c1] pb-3">
                      Practice Leadership
                    </div>
                    <div className="space-y-4">
                      {leadPartners.map((lp) => (
                        <div key={lp.id} className="flex items-center space-x-3">
                          <div className="relative h-12 w-12 shrink-0 overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1]">
                            <Image
                              src={lp.image}
                              alt={lp.name}
                              fill
                              className="object-cover object-top"
                            />
                          </div>
                          <div>
                            <div className="font-serif text-base font-normal text-[#2a1c12]">
                              {lp.name}
                            </div>
                            <div className="text-xs text-[#85725f]">
                              {lp.role} · {lp.inPracticeYears} yrs
                            </div>
                            <div className="text-[11px] font-mono text-[#5b4a3b]">
                              {lp.phone}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    {practice.whereWeArgue && (
                      <div className="pt-4 border-t border-[#e2d5c1] space-y-1 text-xs">
                        <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                          Primary Forums:
                        </div>
                        <ul className="space-y-1 text-xs text-[#5b4a3b]">
                          {practice.whereWeArgue.map((forum, fi) => (
                            <li key={fi} className="truncate">• {forum}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>

                {/* Notable Track Record Metrics */}
                {practice.results && (
                  <div className="mt-8 border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-8">
                    <div className="text-xs uppercase tracking-[0.14em] font-medium text-[#85725f] mb-4">
                      Representative Track Record:
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {practice.results.map((res, ri) => (
                        <div key={ri} className="border-l-2 border-[#9a6a35] pl-4 space-y-1">
                          <div className="font-serif text-3xl font-normal text-[#2a1c12]">
                            {res.metric}
                          </div>
                          <div className="text-xs font-medium text-[#2a1c12]">
                            {res.description}
                          </div>
                          <div className="text-[11px] font-mono text-[#85725f]">
                            {res.forum}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </Container>
            </section>
          );
        })}
      </div>

      {/* 3. Bottom Consultation Callout */}
      <section className="py-16 sm:py-24 bg-[#24180f] text-[#f3ece1] border-t border-[#3f2c1f]">
        <Container size="xl">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <Badge variant="dark">CONFLICT CLEARANCE</Badge>
            <h2 className="font-serif text-[36px] sm:text-[48px] font-normal leading-[1.0] text-[#f3ece1]">
              Initiate a conflict check for your matter.
            </h2>
            <p className="text-sm sm:text-base text-[#b8a695] leading-relaxed max-w-xl mx-auto">
              Our conflicts committee reviews adverse parties against our active client registry within hours. Call directly or start online.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
              <Link href="/contact">
                <Button variant="darkOutline" size="lg">
                  Start Online Conflict Check
                </Button>
              </Link>
              <a
                href="tel:3125550147"
                className="inline-flex items-center px-6 py-3 border border-[#3f2c1f] text-sm text-[#f3ece1] hover:bg-[#3f2c1f] transition-colors"
              >
                <Phone className="mr-2 h-4 w-4 text-[#d1a46a]" />
                <span>Call (312) 555-0147</span>
              </a>
            </div>
          </div>
        </Container>
      </section>

      {/* Quick Consultation Modal */}
      <QuickConsultationModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        defaultPractice={selectedPractice}
      />
    </div>
  );
}
