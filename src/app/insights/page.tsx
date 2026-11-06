"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs } from "@/components/ui/tabs";
import { articles } from "@/data/articles";
import { Clock, ArrowRight, CheckCircle2, Mail, Search } from "lucide-react";

export default function InsightsPage() {
  const [selectedCategory, setSelectedCategory] = React.useState("all");
  const [searchQuery, setSearchQuery] = React.useState("");
  const [newsletterEmail, setNewsletterEmail] = React.useState("");
  const [newsletterSubscribed, setNewsletterSubscribed] = React.useState(false);

  const categories = [
    { id: "all", label: "All Insights", count: articles.length },
    { id: "Trials & Disputes", label: "Disputes" },
    { id: "Corporate & M&A", label: "Deals & LOIs" },
    { id: "Employment", label: "Employment" },
    { id: "Investigations", label: "Investigations" },
    { id: "Real Estate", label: "Real Estate" },
    { id: "IP & Technology", label: "Privacy & Tech" },
  ];

  const filteredArticles = articles.filter((article) => {
    const matchesCategory =
      selectedCategory === "all" || article.category === selectedCategory || article.authorPractice === selectedCategory;

    const matchesSearch =
      searchQuery.trim() === "" ||
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.subtitle?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.author.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (newsletterEmail.trim() && newsletterEmail.includes("@")) {
      setNewsletterSubscribed(true);
    }
  };

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Header Hero */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="max-w-3xl space-y-6">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">PUBLICATIONS & NOTES</Badge>
              <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
                LaSalle Street Treatises
              </span>
            </div>

            <h1 className="font-serif text-[42px] sm:text-[64px] lg:text-[84px] leading-[0.95] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Notes from the floor.
            </h1>

            <p className="font-serif text-[22px] sm:text-[28px] leading-[1.2] text-[#5b4a3b]">
              Practical legal analysis written by trial lawyers and corporate partners—not junior marketing teams.
            </p>

            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
              We write about problems we encounter in Illinois courtrooms, deal closings, and government inquiries. From biometric timeclocks under BIPA to non-compete enforceability and office lease audit rights, each note offers actionable guidance for corporate officers.
            </p>

            {/* Filter Pills & Search */}
            <div className="pt-6 border-t border-[#e2d5c1] space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <Tabs
                  tabs={categories}
                  activeTab={selectedCategory}
                  onChange={setSelectedCategory}
                />
                <div className="relative w-full sm:w-64">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-[#85725f]" />
                  <input
                    type="text"
                    placeholder="Search articles..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-9 pr-4 py-2 border border-[#e2d5c1] bg-[#fffaf2] text-xs text-[#2a1c12] placeholder:text-[#85725f] focus:outline-none focus:border-[#9a6a35] focus:ring-1 focus:ring-[#9a6a35]"
                  />
                </div>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. Articles Grid */}
      <section className="py-16 sm:py-20 lg:py-28">
        <Container size="xl">
          {filteredArticles.length === 0 ? (
            <div className="border border-[#e2d5c1] bg-[#fffaf2] p-12 text-center space-y-4">
              <h3 className="font-serif text-2xl text-[#2a1c12]">No publications match your criteria</h3>
              <p className="text-sm text-[#5b4a3b]">Try clearing your search query or choosing another category filter.</p>
              <Button variant="outline" size="sm" onClick={() => { setSearchQuery(""); setSelectedCategory("all"); }}>
                Reset Filters
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredArticles.map((article) => (
                <Link
                  key={article.id}
                  href={`/insights/${article.slug}`}
                  className="group border border-[#e2d5c1] bg-[#fffaf2] flex flex-col justify-between overflow-hidden shadow-[0_4px_20px_rgba(42,28,18,0.03)] hover:border-[#cfbe9e] transition-all hover:-translate-y-1"
                >
                  <div>
                    {/* Thumbnail Image */}
                    <div className="relative aspect-[16/10] w-full overflow-hidden bg-[#ebe1d1] border-b border-[#e2d5c1]">
                      <Image
                        src={article.image}
                        alt={article.title}
                        fill
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        className="object-cover object-center filter contrast-[1.02] transition-transform duration-500 group-hover:scale-105"
                      />
                      <div className="absolute top-3 left-3">
                        <Badge variant="stamp">{article.category}</Badge>
                      </div>
                    </div>

                    <div className="p-6 sm:p-8 space-y-4">
                      <div className="flex items-center space-x-2 text-xs font-mono text-[#85725f]">
                        <Clock className="h-3.5 w-3.5" />
                        <span>{article.readTime}</span>
                        <span>·</span>
                        <span>{article.date}</span>
                      </div>

                      <h3 className="font-serif text-[22px] sm:text-[24px] font-normal leading-[1.2] tracking-[-0.025em] text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors">
                        {article.title}
                      </h3>

                      <p className="text-xs text-[#5b4a3b] leading-[1.65] line-clamp-3">
                        {article.excerpt || article.subtitle}
                      </p>
                    </div>
                  </div>

                  {/* Author Strip */}
                  <div className="p-6 sm:px-8 sm:py-5 border-t border-[#e2d5c1] bg-[#ebe1d1]/20 flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {article.authorImage && (
                        <div className="relative h-9 w-9 overflow-hidden rounded-full border border-[#e2d5c1] shrink-0">
                          <Image
                            src={article.authorImage}
                            alt={article.author}
                            fill
                            className="object-cover"
                          />
                        </div>
                      )}
                      <div>
                        <div className="text-xs font-sans font-medium text-[#2a1c12]">
                          {article.author}
                        </div>
                        <div className="text-[11px] text-[#85725f]">
                          {article.authorRole} · {article.authorPractice}
                        </div>
                      </div>
                    </div>
                    <ArrowRight className="h-4 w-4 text-[#9a6a35] transition-transform group-hover:translate-x-1 shrink-0" />
                  </div>
                </Link>
              ))}
            </div>
          )}
        </Container>
      </section>

      {/* 3. Quarterly Briefing Subscription Section */}
      <section className="py-16 sm:py-20 border-t border-[#e2d5c1] bg-[#ebe1d1]/40">
        <Container size="xl">
          <div className="max-w-2xl mx-auto border border-[#e2d5c1] bg-[#fffaf2] p-8 sm:p-12 shadow-[0_4px_24px_rgba(42,28,18,0.04)] space-y-6">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">QUARTERLY BRIEFING</Badge>
              <span className="text-xs font-mono text-[#85725f]">Zero Marketing Spam</span>
            </div>

            <h3 className="font-serif text-[28px] sm:text-[34px] font-normal leading-[1.1] text-[#2a1c12]">
              Receive our quarterly LaSalle Street legal briefing.
            </h3>

            <p className="text-xs sm:text-sm text-[#5b4a3b] leading-[1.6]">
              A concise quarterly digest of Seventh Circuit commercial precedents, Cook County commercial calendar developments, Illinois non-compete updates, and M&A negotiating shifts. Delivered four times per year.
            </p>

            {newsletterSubscribed ? (
              <div className="p-4 border border-[#9a6a35] bg-[#ebe1d1]/50 flex items-center space-x-3 text-xs text-[#2a1c12]">
                <CheckCircle2 className="h-5 w-5 text-[#9a6a35] shrink-0" />
                <span>
                  Thank you. Your email <span className="font-mono font-medium">{newsletterEmail}</span> has been added to our quarterly partner distribution list.
                </span>
              </div>
            ) : (
              <form onSubmit={handleSubscribe} className="space-y-3">
                <div className="flex flex-col sm:flex-row gap-3">
                  <input
                    type="email"
                    required
                    placeholder="Enter corporate email address..."
                    value={newsletterEmail}
                    onChange={(e) => setNewsletterEmail(e.target.value)}
                    className="flex-1 px-4 py-2.5 border border-[#e2d5c1] bg-[#fffaf2] text-sm text-[#2a1c12] placeholder:text-[#85725f] focus:outline-none focus:border-[#9a6a35] focus:ring-1 focus:ring-[#9a6a35]"
                  />
                  <Button type="submit" variant="primary" size="md" className="shrink-0">
                    Subscribe
                  </Button>
                </div>
                <p className="text-[11px] text-[#85725f] font-mono">
                  You can unsubscribe at any time. We never sell or share client subscriber information.
                </p>
              </form>
            )}
          </div>
        </Container>
      </section>

      {/* 4. Bottom Conflict Intake CTA */}
      <section className="py-16 sm:py-24 bg-[#24180f] text-[#f3ece1] border-t border-[#3f2c1f]">
        <Container size="xl">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <Badge variant="dark">PRACTICE INQUIRIES</Badge>
            <h2 className="font-serif text-[36px] sm:text-[48px] font-normal leading-[1.0] text-[#f3ece1]">
              Consult with the author of an article.
            </h2>
            <p className="text-sm sm:text-base text-[#b8a695] leading-relaxed max-w-xl mx-auto">
              Our authors personally lead client matters in the areas they write about. Clear conflicts online to schedule an introductory conference.
            </p>
            <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
              <Link href="/contact">
                <Button variant="darkOutline" size="lg">
                  Start Online Conflict Check
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </section>
    </div>
  );
}
