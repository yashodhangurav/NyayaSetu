"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { partners, teamRoster } from "@/data/lawyers";
import { Phone, Mail, Award, GraduationCap, ArrowRight, ShieldCheck, Check, Search, X, FileCheck, Copy } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { QuickConsultationModal } from "@/components/ui/quick-consultation-modal";

export default function PeoplePage() {
  const [selectedPracticeFilter, setSelectedPracticeFilter] = React.useState("all");
  const [searchQuery, setSearchQuery] = React.useState("");
  const [consultModalOpen, setConsultModalOpen] = React.useState(false);
  const [selectedPartner, setSelectedPartner] = React.useState<string | undefined>(undefined);
  const [selectedPractice, setSelectedPractice] = React.useState<string>("Trials & Disputes");
  const [copiedVCard, setCopiedVCard] = React.useState<string | null>(null);

  const practicesList = [
    { id: "all", label: "All Lawyers (41)" },
    { id: "Trials & Disputes", label: "Trials & Disputes" },
    { id: "Corporate & M&A", label: "Corporate & M&A" },
    { id: "Employment", label: "Employment" },
    { id: "Investigations", label: "Investigations" },
    { id: "Real Estate", label: "Real Estate" },
    { id: "IP & Technology", label: "IP & Technology" },
  ];

  const query = searchQuery.toLowerCase().trim();

  const filteredPartners = partners.filter((p) => {
    const matchesPractice =
      selectedPracticeFilter === "all" || p.practice === selectedPracticeFilter;
    const matchesSearch =
      query === "" ||
      p.name.toLowerCase().includes(query) ||
      p.role.toLowerCase().includes(query) ||
      p.practice.toLowerCase().includes(query) ||
      p.bio.toLowerCase().includes(query) ||
      p.admissions.some((a) => a.toLowerCase().includes(query)) ||
      p.education.some((e) => e.toLowerCase().includes(query));

    return matchesPractice && matchesSearch;
  });

  const filteredRoster = teamRoster.filter((r) => {
    const matchesPractice =
      selectedPracticeFilter === "all" || r.practice === selectedPracticeFilter;
    const matchesSearch =
      query === "" ||
      r.practice.toLowerCase().includes(query) ||
      r.counsel.some((c) => c.toLowerCase().includes(query)) ||
      r.associates.some((a) => a.toLowerCase().includes(query));

    return matchesPractice && matchesSearch;
  });

  const handleCopyVCard = (partnerName: string, email: string, phone: string) => {
    const vCardText = `BEGIN:VCARD\nVERSION:3.0\nFN:${partnerName}\nORG:Ellery Kowal LLP\nTITLE:Partner\nEMAIL:${email}\nTEL:${phone}\nADR:;;224 S. LaSalle St, 31st Fl;Chicago;IL;60604;USA\nEND:VCARD`;
    if (typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard.writeText(vCardText);
    }
    setCopiedVCard(partnerName);
    setTimeout(() => {
      setCopiedVCard(null);
    }, 2200);
  };

  const handleOpenConsult = (partnerName: string, practice: string) => {
    setSelectedPartner(partnerName);
    setSelectedPractice(practice);
    setConsultModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Hero / Header */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="max-w-3xl space-y-6">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">THE TEAM</Badge>
              <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
                224 S. LaSalle Street · 31st Floor
              </span>
            </div>

            <h1 className="font-serif text-[42px] sm:text-[64px] lg:text-[84px] leading-[0.95] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Seven partners, one floor of 224 S. LaSalle.
            </h1>

            <p className="font-serif text-[22px] sm:text-[28px] leading-[1.2] text-[#5b4a3b]">
              The lawyer you hire is the one who reads the contract, takes the deposition, and stands before the bench.
            </p>

            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
              Ellery Kowal operates on one foundational staffing rule: zero associate leverage pyramids. Our 41 lawyers include seven named equity partners, eight counsel, and twenty-six associates—ensuring that senior legal judgement directs every active client matter.
            </p>

            {/* Practice Filter Pills & Search */}
            <div className="pt-6 border-t border-[#e2d5c1] space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex flex-wrap gap-2">
                  {practicesList.map((pf) => (
                    <button
                      key={pf.id}
                      type="button"
                      onClick={() => setSelectedPracticeFilter(pf.id)}
                      className={`px-3.5 py-1.5 text-xs font-sans uppercase tracking-[0.1em] font-medium border transition-colors cursor-pointer ${
                        selectedPracticeFilter === pf.id
                          ? "border-[#2a1c12] bg-[#2a1c12] text-[#fffaf2]"
                          : "border-[#e2d5c1] bg-[#fffaf2] text-[#5b4a3b] hover:bg-[#ebe1d1]"
                      }`}
                    >
                      {pf.label}
                    </button>
                  ))}
                </div>

                <div className="relative w-full sm:w-64">
                  <Search className="absolute left-3 top-2.5 h-4 w-4 text-[#85725f]" />
                  <input
                    type="text"
                    placeholder="Search by name, school, admission..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-9 pr-8 py-1.5 border border-[#e2d5c1] bg-[#fffaf2] text-xs text-[#2a1c12] placeholder:text-[#85725f] focus:outline-none focus:border-[#9a6a35] focus:ring-1 focus:ring-[#9a6a35]"
                  />
                  {searchQuery && (
                    <button
                      type="button"
                      onClick={() => setSearchQuery("")}
                      className="absolute right-2.5 top-2.5 text-[#85725f] hover:text-[#2a1c12]"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. Equity Partners Detailed Showcase */}
      <section className="py-16 sm:py-20 lg:py-28">
        <Container size="xl">
          <div className="border-b border-[#e2d5c1] pb-6 mb-12 flex items-center justify-between">
            <div>
              <h2 className="font-serif text-3xl sm:text-4xl font-normal text-[#2a1c12]">
                Equity Partners
              </h2>
              <p className="text-xs text-[#85725f] mt-1">
                Named partners leading trials, transactions, covenants, and investigations
              </p>
            </div>
            <span className="text-xs font-mono text-[#85725f]">
              {filteredPartners.length} of {partners.length} Partners
            </span>
          </div>

          {filteredPartners.length === 0 ? (
            <div className="border border-[#e2d5c1] bg-[#fffaf2] p-12 text-center space-y-4">
              <div className="font-serif text-2xl text-[#2a1c12]">No partners match your criteria</div>
              <p className="text-sm text-[#5b4a3b] max-w-md mx-auto">
                No equity partners found matching &ldquo;{searchQuery}&rdquo;. Try clearing your search term.
              </p>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setSearchQuery("");
                  setSelectedPracticeFilter("all");
                }}
              >
                Reset search
              </Button>
            </div>
          ) : (
            <div className="space-y-12">
              {filteredPartners.map((partner) => (
                <div
                  key={partner.id}
                  id={partner.id}
                  className="border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-10 shadow-[0_4px_24px_rgba(42,28,18,0.04)] scroll-mt-24"
                >
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
                    {/* Photo & Quick Info (4 cols) */}
                    <div className="lg:col-span-4 space-y-4">
                      <div className="relative aspect-[4/5] w-full overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1]">
                        <Image
                          src={partner.image}
                          alt={partner.name}
                          fill
                          sizes="(max-width: 1024px) 100vw, 380px"
                          className="object-cover object-top filter contrast-[1.02]"
                        />
                      </div>

                      <div className="p-4 border border-[#e2d5c1] bg-[#ebe1d1]/30 space-y-2 text-xs font-mono">
                        <div className="flex items-center justify-between">
                          <span className="text-[#85725f]">Experience:</span>
                          <span className="font-semibold text-[#2a1c12]">{partner.inPracticeYears} Years</span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-[#85725f]">Direct Line:</span>
                          <a href={`tel:${partner.phone}`} className="text-[#9a6a35] hover:underline font-medium">
                            {partner.phone}
                          </a>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-[#85725f]">Email:</span>
                          <a href={`mailto:${partner.email}`} className="text-[#2a1c12] hover:underline">
                            {partner.email}
                          </a>
                        </div>
                      </div>

                      <div className="space-y-2 pt-1">
                        <Button
                          variant="primary"
                          size="md"
                          onClick={() => handleOpenConsult(partner.name, partner.practice)}
                          className="w-full bg-[#2a1c12] text-[#fffaf2] hover:bg-[#9a6a35]"
                        >
                          Consult with {partner.name.split(" ")[0]}
                        </Button>

                        <button
                          type="button"
                          onClick={() => handleCopyVCard(partner.name, partner.email, partner.phone)}
                          className="w-full py-2 border border-[#e2d5c1] bg-[#fffaf2] text-xs font-mono uppercase tracking-wider text-[#5b4a3b] hover:text-[#2a1c12] hover:bg-[#ebe1d1] transition-colors flex items-center justify-center cursor-pointer"
                        >
                          {copiedVCard === partner.name ? (
                            <span className="inline-flex items-center text-[#9a6a35] font-semibold">
                              <Check className="h-3.5 w-3.5 mr-1" />
                              vCard Copied!
                            </span>
                          ) : (
                            <span className="inline-flex items-center">
                              <Copy className="h-3.5 w-3.5 mr-1" />
                              Download / Copy vCard
                            </span>
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Bio, Credentials & Results (8 cols) */}
                    <div className="lg:col-span-8 space-y-6">
                      <div>
                        <div className="flex items-center space-x-3 mb-2">
                          <Badge variant="stamp">{partner.practice}</Badge>
                          <span className="text-xs font-mono text-[#85725f]">
                            {partner.role}
                          </span>
                        </div>
                        <h3 className="font-serif text-[32px] sm:text-[40px] font-normal leading-[1.08] text-[#2a1c12]">
                          {partner.name}
                        </h3>
                      </div>

                      <p className="text-[15px] sm:text-[16px] leading-[1.65] text-[#5b4a3b]">
                        {partner.bio}
                      </p>

                      {/* Prior Experience */}
                      {partner.priorExperience && (
                        <div className="border-t border-[#e2d5c1] pt-4 text-xs sm:text-sm">
                          <span className="font-mono text-[#85725f] uppercase tracking-wider text-xs">
                            Prior Experience:{" "}
                          </span>
                          <span className="text-[#2a1c12] font-medium">
                            {partner.priorExperience}
                          </span>
                        </div>
                      )}

                      {/* Key Trial & Deal Results */}
                      <div className="border-t border-[#e2d5c1] pt-4 space-y-3">
                        <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                          Representative Results & Matters:
                        </div>
                        <ul className="space-y-2 text-xs sm:text-sm text-[#5b4a3b]">
                          {partner.keyResults.map((result, idx) => (
                            <li key={idx} className="flex items-start">
                              <span className="mr-3 text-[#9a6a35] font-bold shrink-0">—</span>
                              <span className="leading-relaxed">{result}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Education & Admissions */}
                      <div className="border-t border-[#e2d5c1] pt-4 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                        <div className="space-y-1.5">
                          <div className="flex items-center space-x-1.5 font-mono text-[#85725f] uppercase tracking-wider text-[11px]">
                            <GraduationCap className="h-3.5 w-3.5" />
                            <span>Education</span>
                          </div>
                          <ul className="space-y-1 text-xs text-[#2a1c12]">
                            {partner.education.map((edu, ei) => (
                              <li key={ei}>• {edu}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="space-y-1.5">
                          <div className="flex items-center space-x-1.5 font-mono text-[#85725f] uppercase tracking-wider text-[11px]">
                            <ShieldCheck className="h-3.5 w-3.5" />
                            <span>Bar Admissions</span>
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {partner.admissions.map((adm, ai) => (
                              <span
                                key={ai}
                                className="border border-[#e2d5c1] bg-[#ebe1d1]/40 px-2 py-0.5 text-[11px] font-mono text-[#2a1c12]"
                              >
                                {adm}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Container>
      </section>

      {/* 3. Counsel & Associates Roster Directory */}
      <section className="border-t border-[#e2d5c1] bg-[#ebe1d1]/30 py-16 sm:py-20 lg:py-28">
        <Container size="xl">
          <div className="max-w-3xl space-y-4 mb-12">
            <Badge variant="stamp">DIRECTORY</Badge>
            <h2 className="font-serif text-[32px] sm:text-[44px] font-normal leading-[1.0] text-[#2a1c12]">
              Counsel & Associates Roster
            </h2>
            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6]">
              Our counsel and associates provide targeted research, factual investigation, discovery administration, and transaction documentation across each of our six core practices.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredRoster.map((group) => (
              <div
                key={group.practice}
                className="border border-[#e2d5c1] bg-[#fffaf2] p-6 space-y-6 shadow-[0_4px_20px_rgba(42,28,18,0.03)]"
              >
                <div className="border-b border-[#e2d5c1] pb-3 flex items-center justify-between">
                  <h3 className="font-serif text-xl font-normal text-[#2a1c12]">
                    {group.practice}
                  </h3>
                  <Badge variant="stamp">
                    {group.counsel.length + group.associates.length} Lawyers
                  </Badge>
                </div>

                {/* Counsel */}
                <div className="space-y-2">
                  <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                    Senior Counsel:
                  </div>
                  <ul className="space-y-1.5 text-xs font-medium text-[#2a1c12]">
                    {group.counsel.map((c, ci) => (
                      <li key={ci} className="flex items-center space-x-2">
                        <span className="h-1.5 w-1.5 bg-[#9a6a35] rounded-full" />
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Associates */}
                <div className="space-y-2 pt-3 border-t border-[#e2d5c1]/60">
                  <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                    Associates:
                  </div>
                  <ul className="space-y-1.5 text-xs text-[#5b4a3b]">
                    {group.associates.map((a, ai) => (
                      <li key={ai} className="flex items-center space-x-2">
                        <span className="h-1 w-1 bg-[#85725f] rounded-full" />
                        <span>{a}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </Container>
      </section>

      {/* 4. Bottom Conflict Intake Banner */}
      <section className="py-16 sm:py-24 bg-[#24180f] text-[#f3ece1] border-t border-[#3f2c1f]">
        <Container size="xl">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <Badge variant="dark">STAFFING COMMITMENT</Badge>
            <h2 className="font-serif text-[36px] sm:text-[48px] font-normal leading-[1.0] text-[#f3ece1]">
              Work directly with our partners.
            </h2>
            <p className="text-sm sm:text-base text-[#b8a695] leading-relaxed max-w-xl mx-auto">
              Schedule an introductory conference with the partner in charge of your practice area once adverse conflicts are cleared.
            </p>
            <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
              <Link href="/contact">
                <Button variant="darkOutline" size="lg">
                  Start Conflict Check Online
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
        isOpen={consultModalOpen}
        onClose={() => setConsultModalOpen(false)}
        defaultPartner={selectedPartner}
        defaultPractice={selectedPractice}
      />
    </div>
  );
}
