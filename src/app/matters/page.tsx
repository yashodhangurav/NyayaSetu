"use client";

import * as React from "react";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Tabs } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { matters } from "@/data/matters";
import { ChevronDown, ArrowRight, ShieldCheck, Scale, Phone, Search, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { QuickConsultationModal } from "@/components/ui/quick-consultation-modal";

export default function MattersPage() {
  const [selectedCategory, setSelectedCategory] = React.useState("all");
  const [searchQuery, setSearchQuery] = React.useState("");
  const [expandedIds, setExpandedIds] = React.useState<string[]>(["matter-1", "matter-2"]);
  const [consultModalOpen, setConsultModalOpen] = React.useState(false);
  const [selectedPractice, setSelectedPractice] = React.useState("Trials & Disputes");
  const [selectedPartner, setSelectedPartner] = React.useState("");

  const tabs = [
    { id: "all", label: "All Matters", count: 16 },
    { id: "Disputes", label: "Disputes", count: 7 },
    { id: "Transactions", label: "Transactions", count: 5 },
    { id: "Investigations", label: "Investigations", count: 4 },
  ];

  const filteredMatters = matters.filter((m) => {
    const matchesCategory = selectedCategory === "all" || m.category === selectedCategory;
    const query = searchQuery.toLowerCase().trim();
    const matchesSearch =
      query === "" ||
      m.title.toLowerCase().includes(query) ||
      m.summary.toLowerCase().includes(query) ||
      (m.leadPartner && m.leadPartner.toLowerCase().includes(query)) ||
      (m.practice && m.practice.toLowerCase().includes(query)) ||
      (m.forum && m.forum.toLowerCase().includes(query)) ||
      (m.result && m.result.toLowerCase().includes(query)) ||
      (m.year && m.year.includes(query));

    return matchesCategory && matchesSearch;
  });

  const toggleMatter = (id: string) => {
    setExpandedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const expandAll = () => {
    setExpandedIds(filteredMatters.map((m) => m.id));
  };

  const collapseAll = () => {
    setExpandedIds([]);
  };

  const handleInquireMatter = (practice: string, partner: string) => {
    setSelectedPractice(practice);
    setSelectedPartner(partner);
    setConsultModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Header Hero */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="max-w-3xl space-y-6">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">REPRESENTATIVE MATTERS</Badge>
              <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
                Public Record 2023–2026
              </span>
            </div>

            <h1 className="font-serif text-[42px] sm:text-[64px] lg:text-[84px] leading-[0.95] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Prepared for trial. That’s why most settle.
            </h1>

            <p className="font-serif text-[22px] sm:text-[28px] leading-[1.2] text-[#5b4a3b]">
              A public ledger of 16 commercial jury verdicts, business sales, emergency injunctions, and regulatory closures.
            </p>

            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
              Every matter listed below was led by an Ellery Kowal partner. We do not litigate to bill hours; we litigate to achieve courtroom trial leverage, regulatory declinations, and definitive commercial transaction closings.
            </p>

            {/* Filter Pills & Search */}
            <div className="pt-6 border-t border-[#e2d5c1] space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <Tabs
                  tabs={tabs}
                  activeTab={selectedCategory}
                  onChange={setSelectedCategory}
                />
                <div className="relative w-full sm:w-72">
                  <Search className="absolute left-3 top-2.5 h-4 w-4 text-[#85725f]" />
                  <input
                    type="text"
                    placeholder="Search by client, partner, forum..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-9 pr-8 py-2 border border-[#e2d5c1] bg-[#fffaf2] text-xs text-[#2a1c12] placeholder:text-[#85725f] focus:outline-none focus:border-[#9a6a35] focus:ring-1 focus:ring-[#9a6a35]"
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

              <div className="flex items-center justify-between text-xs font-mono text-[#85725f]">
                <div>
                  Showing {filteredMatters.length} of {matters.length} case records
                </div>
                <div className="flex items-center space-x-3">
                  <button
                    type="button"
                    onClick={expandAll}
                    className="hover:text-[#2a1c12] hover:underline cursor-pointer"
                  >
                    Expand All
                  </button>
                  <span>·</span>
                  <button
                    type="button"
                    onClick={collapseAll}
                    className="hover:text-[#2a1c12] hover:underline cursor-pointer"
                  >
                    Collapse All
                  </button>
                </div>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. Top Metric Highlights Bar */}
      <section className="border-b border-[#e2d5c1] bg-[#fffaf2] py-8">
        <Container size="xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 divide-x divide-[#e2d5c1]/60">
            <div className="pl-4 sm:pl-6 space-y-1">
              <div className="font-serif text-3xl sm:text-4xl text-[#2a1c12] font-normal">$18.4M</div>
              <div className="text-xs text-[#85725f] font-mono">Federal Jury Verdict (N.D. Ill.)</div>
            </div>
            <div className="pl-4 sm:pl-6 space-y-1">
              <div className="font-serif text-3xl sm:text-4xl text-[#2a1c12] font-normal">$212M</div>
              <div className="text-xs text-[#85725f] font-mono">Company Sale to Private Equity</div>
            </div>
            <div className="pl-4 sm:pl-6 space-y-1">
              <div className="font-serif text-3xl sm:text-4xl text-[#2a1c12] font-normal">36 Hours</div>
              <div className="text-xs text-[#85725f] font-mono">Emergency Chancery Injunction</div>
            </div>
            <div className="pl-4 sm:pl-6 space-y-1">
              <div className="font-serif text-3xl sm:text-4xl text-[#2a1c12] font-normal">0 Charges</div>
              <div className="text-xs text-[#85725f] font-mono">DOJ Grand Jury Declination</div>
            </div>
          </div>
        </Container>
      </section>

      {/* 3. Full 16 Matters Ledger Table */}
      <section className="py-16 sm:py-20 lg:py-28">
        <Container size="xl">
          {filteredMatters.length === 0 ? (
            <div className="border border-[#e2d5c1] bg-[#fffaf2] p-12 text-center space-y-4">
              <div className="font-serif text-2xl text-[#2a1c12]">No matching matters found</div>
              <p className="text-sm text-[#5b4a3b] max-w-md mx-auto">
                No matters in our public ledger match &ldquo;{searchQuery}&rdquo;. Try adjusting your search term or category filter.
              </p>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategory("all");
                }}
              >
                Clear all filters
              </Button>
            </div>
          ) : (
            <div className="border border-[#e2d5c1] bg-[#fffaf2] shadow-[0_4px_24px_rgba(42,28,18,0.04)]">
              {/* Table Header Row */}
              <div className="hidden sm:grid sm:grid-cols-12 border-b border-[#e2d5c1] bg-[#ebe1d1]/50 px-6 py-4 text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                <div className="col-span-3">Result / Magnitude</div>
                <div className="col-span-5">Matter Title & Scope</div>
                <div className="col-span-2">Lead Partner</div>
                <div className="col-span-2 text-right">Forum / Year</div>
              </div>

              {/* Table Rows */}
              <div className="divide-y divide-[#e2d5c1]">
                {filteredMatters.map((matter) => {
                  const isExpanded = expandedIds.includes(matter.id);

                  return (
                    <div key={matter.id} className="transition-colors hover:bg-[#ebe1d1]/20">
                      {/* Row Summary Bar */}
                      <div
                        onClick={() => toggleMatter(matter.id)}
                        className="p-6 cursor-pointer flex flex-col sm:grid sm:grid-cols-12 gap-4 items-start sm:items-center"
                      >
                        {/* Result */}
                        <div className="sm:col-span-3 flex items-center space-x-3">
                          <ChevronDown
                            className={`h-4 w-4 shrink-0 text-[#85725f] transition-transform duration-200 ${
                              isExpanded ? "rotate-180 text-[#9a6a35]" : ""
                            }`}
                          />
                          <div>
                            <div className="font-serif text-2xl sm:text-[26px] font-normal text-[#2a1c12] leading-none">
                              {matter.result}
                            </div>
                            <div className="text-[11px] font-mono uppercase tracking-wider text-[#9a6a35] mt-1">
                              {matter.resultUnit}
                            </div>
                          </div>
                        </div>

                        {/* Title */}
                        <div className="sm:col-span-5 pr-4">
                          <h3 className="font-serif text-[17px] sm:text-[18px] font-normal leading-[1.3] text-[#2a1c12]">
                            {matter.title}
                          </h3>
                          <div className="sm:hidden text-xs text-[#85725f] mt-1">
                            Lead: {matter.leadPartner} · {matter.year}
                          </div>
                        </div>

                        {/* Lead Partner */}
                        <div className="hidden sm:block sm:col-span-2 text-xs font-sans text-[#5b4a3b]">
                          <span className="font-medium text-[#2a1c12]">{matter.leadPartner}</span>
                          <div className="text-[11px] text-[#85725f] font-mono">{matter.practice}</div>
                        </div>

                        {/* Forum & Year */}
                        <div className="hidden sm:block sm:col-span-2 text-right text-xs font-mono text-[#85725f]">
                          <div>{matter.year}</div>
                          <div className="text-[11px] truncate max-w-[140px] ml-auto">{matter.forum}</div>
                        </div>
                      </div>

                      {/* Expandable Matter Dossier */}
                      <AnimatePresence initial={false}>
                        {isExpanded && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{
                              height: "auto",
                              opacity: 1,
                              transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
                            }}
                            exit={{
                              height: 0,
                              opacity: 0,
                              transition: { duration: 0.2, ease: [0.16, 1, 0.3, 1] },
                            }}
                            className="overflow-hidden bg-[#ebe1d1]/30 border-t border-[#e2d5c1]"
                          >
                            <div className="p-6 sm:p-8 space-y-6">
                              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                                <div className="lg:col-span-7 space-y-4">
                                  <div>
                                    <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f] mb-1">
                                      Matter Background & Retention
                                    </div>
                                    <p className="text-sm text-[#5b4a3b] leading-[1.65]">
                                      {matter.summary}
                                    </p>
                                  </div>

                                  <div>
                                    <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f] mb-1">
                                      What Happened / Strategic Outcome
                                    </div>
                                    <p className="text-sm text-[#2a1c12] font-serif leading-[1.6]">
                                      {matter.whatHappened}
                                    </p>
                                  </div>
                                </div>

                                <div className="lg:col-span-5 border-l border-[#e2d5c1] lg:pl-6 space-y-3 text-xs font-mono">
                                  <div className="border-b border-[#e2d5c1] pb-2">
                                    <span className="text-[#85725f] block">FORUM / VENUE:</span>
                                    <span className="text-[#2a1c12] font-sans font-medium">{matter.forum}</span>
                                  </div>
                                  <div className="border-b border-[#e2d5c1] pb-2">
                                    <span className="text-[#85725f] block">LEAD TRIAL / TRANSACTION COUNSEL:</span>
                                    <span className="text-[#2a1c12] font-sans font-medium">{matter.leadPartner}</span>
                                  </div>
                                  <div className="border-b border-[#e2d5c1] pb-2">
                                    <span className="text-[#85725f] block">PRACTICE CLASSIFICATION:</span>
                                    <span className="text-[#9a6a35]">{matter.practice}</span>
                                  </div>
                                  <div className="pt-2">
                                    <button
                                      type="button"
                                      onClick={() => handleInquireMatter(matter.practice || "Trials & Disputes", matter.leadPartner || "")}
                                      className="inline-flex items-center text-xs font-medium text-[#2a1c12] hover:text-[#9a6a35] transition-colors cursor-pointer"
                                    >
                                      <span>Inquire regarding similar matter</span>
                                      <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                                    </button>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </Container>
      </section>

      {/* 4. Conflict Check CTA Strip */}
      <section className="border-t border-[#e2d5c1] bg-[#ebe1d1]/30 py-16">
        <Container size="xl">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
            <div className="max-w-2xl space-y-2">
              <h3 className="font-serif text-2xl sm:text-3xl font-normal text-[#2a1c12]">
                Have an adverse party or commercial dispute?
              </h3>
              <p className="text-sm text-[#5b4a3b]">
                All matter intakes begin with same-day conflict clearance across Illinois court registers.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-4">
              <button
                type="button"
                onClick={() => setConsultModalOpen(true)}
                className="px-5 py-3 border border-[#e2d5c1] bg-[#fffaf2] text-xs font-mono uppercase tracking-wider text-[#2a1c12] hover:bg-[#ebe1d1] transition-colors cursor-pointer"
              >
                Quick Consultation
              </button>
              <Link href="/contact">
                <Button variant="primary" size="lg" className="bg-[#2a1c12] text-[#fffaf2]">
                  Start a conflict check
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </section>

      {/* Consultation Modal */}
      <QuickConsultationModal
        isOpen={consultModalOpen}
        onClose={() => setConsultModalOpen(false)}
        defaultPractice={selectedPractice}
        defaultPartner={selectedPartner}
      />
    </div>
  );
}
