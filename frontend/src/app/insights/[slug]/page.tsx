import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { articles } from "@/data/articles";
import { partners } from "@/data/lawyers";
import { Clock, ArrowRight, ArrowLeft, ChevronRight } from "lucide-react";
import type { Metadata } from "next";

type Props = {
  params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
  return articles.map((article) => ({
    slug: article.slug,
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const article = articles.find((a) => a.slug === slug);

  if (!article) {
    return {
      title: "Article Not Found · Ellery Kowal LLP",
    };
  }

  return {
    title: `${article.title} · Ellery Kowal LLP`,
    description: article.excerpt || article.subtitle,
  };
}

export default async function ArticleDetailPage({ params }: Props) {
  const { slug } = await params;
  const article = articles.find((a) => a.slug === slug);

  if (!article) {
    notFound();
  }

  // Find partner details if matches author name
  const authorPartner = partners.find((p) => p.name === article.author);

  // 2 Related articles (excluding current)
  const relatedArticles = articles
    .filter((a) => a.slug !== article.slug)
    .slice(0, 2);

  return (
    <article className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Article Header & Breadcrumbs */}
      <section className="border-b border-[#e2d5c1] py-12 md:py-16 bg-[#ebe1d1]/30">
        <Container size="lg">
          <div className="space-y-6">
            {/* Breadcrumb Trail */}
            <nav className="flex items-center space-x-2 text-xs font-mono text-[#85725f]">
              <Link href="/" className="hover:text-[#2a1c12] transition-colors">
                Home
              </Link>
              <ChevronRight className="h-3 w-3" />
              <Link href="/insights" className="hover:text-[#2a1c12] transition-colors">
                Insights
              </Link>
              <ChevronRight className="h-3 w-3" />
              <span className="text-[#2a1c12] font-medium truncate max-w-[200px] sm:max-w-md">
                {article.category}
              </span>
            </nav>

            {/* Metadata Badges */}
            <div className="flex flex-wrap items-center gap-3">
              <Badge variant="stamp">{article.category}</Badge>
              <div className="flex items-center space-x-2 text-xs font-mono text-[#85725f]">
                <Clock className="h-3.5 w-3.5" />
                <span>{article.readTime}</span>
                <span>·</span>
                <span>{article.date}</span>
              </div>
            </div>

            {/* Headline H1 */}
            <h1 className="font-serif text-[36px] sm:text-[48px] lg:text-[60px] leading-[1.02] tracking-[-0.04em] font-normal text-[#2a1c12]">
              {article.title}
            </h1>

            {/* Subhead / Lead Summary */}
            {article.subtitle && (
              <p className="font-serif italic text-[20px] sm:text-[24px] leading-[1.25] text-[#5b4a3b]">
                {article.subtitle}
              </p>
            )}

            {/* Author Byline Strip */}
            <div className="pt-6 border-t border-[#e2d5c1] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                {article.authorImage && (
                  <div className="relative h-14 w-14 overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1] shrink-0">
                    <Image
                      src={article.authorImage}
                      alt={article.author}
                      fill
                      className="object-cover object-top"
                    />
                  </div>
                )}
                <div>
                  <div className="font-serif text-lg font-normal text-[#2a1c12]">
                    {article.author}
                  </div>
                  <div className="text-xs text-[#85725f]">
                    {article.authorRole} · {article.authorPractice}
                  </div>
                  {authorPartner && (
                    <div className="text-[11px] font-mono text-[#5b4a3b] mt-0.5">
                      {authorPartner.phone} · {authorPartner.email}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Link href={`/contact?partner=${encodeURIComponent(article.author)}`}>
                  <Button variant="primary" size="sm">
                    Consult with Author
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. Article Featured Image */}
      <section className="py-8 sm:py-12 border-b border-[#e2d5c1]">
        <Container size="lg">
          <div className="relative aspect-[16/10] sm:aspect-[16/9] w-full overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1] shadow-[0_4px_24px_rgba(42,28,18,0.04)]">
            <Image
              src={article.image}
              alt={article.title}
              fill
              priority
              sizes="(max-width: 1024px) 100vw, 1100px"
              className="object-cover object-center filter contrast-[1.02]"
            />
          </div>
        </Container>
      </section>

      {/* 3. Article Editorial Body */}
      <section className="py-12 sm:py-16 lg:py-20">
        <Container size="md">
          <div className="space-y-8 font-sans text-[16px] sm:text-[17px] leading-[1.75] text-[#2a1c12]/90">
            {/* Pull Quote Box */}
            {article.pullQuote && (
              <div className="border-l-2 border-[#9a6a35] bg-[#fffaf2] p-6 sm:p-8 my-8 shadow-[0_4px_20px_rgba(42,28,18,0.03)] border-y border-r border-[#e2d5c1]">
                <span className="font-serif text-3xl text-[#9a6a35] leading-none">“</span>
                <p className="font-serif italic text-[20px] sm:text-[23px] leading-[1.35] text-[#2a1c12] mt-1">
                  {article.pullQuote}
                </p>
                <div className="mt-4 text-xs font-mono uppercase tracking-wider text-[#85725f]">
                  — {article.author}, {article.authorRole}
                </div>
              </div>
            )}

            {/* Paragraphs */}
            {article.paragraphs?.map((para, idx) => (
              <p
                key={idx}
                className={idx === 0 ? "first-letter:font-serif first-letter:text-5xl first-letter:font-normal first-letter:float-left first-letter:mr-3 first-letter:text-[#2a1c12] first-letter:leading-none" : ""}
              >
                {para}
              </p>
            ))}

            {/* Key Takeaways Architectural Box */}
            {article.takeaways && article.takeaways.length > 0 && (
              <div className="mt-12 border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-10 shadow-[0_4px_24px_rgba(42,28,18,0.04)] space-y-4">
                <div className="flex items-center space-x-3 border-b border-[#e2d5c1] pb-3">
                  <Badge variant="gold">KEY COUNSEL TAKEAWAYS</Badge>
                  <span className="text-xs font-mono text-[#85725f]">Action Protocol</span>
                </div>

                <ul className="space-y-3 pt-2 text-sm text-[#2a1c12]">
                  {article.takeaways.map((takeaway, ti) => (
                    <li key={ti} className="flex items-start">
                      <span className="font-serif text-base text-[#9a6a35] mr-3 font-normal">
                        0{ti + 1}.
                      </span>
                      <span className="leading-relaxed font-sans">{takeaway}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Author Detailed Dossier Card */}
          {authorPartner && (
            <div className="mt-16 border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-8 shadow-[0_4px_20px_rgba(42,28,18,0.03)] space-y-4">
              <div className="text-[11px] uppercase tracking-wider font-mono text-[#85725f]">
                About the Author
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center gap-6">
                <div className="relative h-20 w-20 overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1] shrink-0">
                  <Image
                    src={authorPartner.image}
                    alt={authorPartner.name}
                    fill
                    className="object-cover object-top"
                  />
                </div>

                <div className="space-y-1">
                  <h4 className="font-serif text-2xl font-normal text-[#2a1c12]">
                    {authorPartner.name}
                  </h4>
                  <div className="text-xs text-[#9a6a35] font-medium font-sans">
                    {authorPartner.role} · {authorPartner.practice} · {authorPartner.inPracticeYears} Years in Practice
                  </div>
                  <p className="text-xs text-[#5b4a3b] leading-relaxed pt-1">
                    {authorPartner.bio}
                  </p>
                </div>
              </div>

              <div className="pt-4 border-t border-[#e2d5c1] flex flex-wrap items-center justify-between text-xs font-mono text-[#85725f] gap-4">
                <div>
                  <span>Direct: {authorPartner.phone}</span>
                  <span className="mx-2">·</span>
                  <span>{authorPartner.email}</span>
                </div>
                <Link href={`/contact?partner=${authorPartner.id}`}>
                  <Button variant="outline" size="sm">
                    Inquire Directly
                  </Button>
                </Link>
              </div>
            </div>
          )}

          {/* Back to Insights Navigation */}
          <div className="mt-12 pt-8 border-t border-[#e2d5c1] flex items-center justify-between">
            <Link
              href="/insights"
              className="inline-flex items-center text-xs font-semibold uppercase tracking-wider text-[#2a1c12] hover:text-[#9a6a35] transition-colors"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              <span>Back to all publications</span>
            </Link>
          </div>
        </Container>
      </section>

      {/* 4. Related Publications Strip */}
      <section className="py-16 sm:py-20 border-t border-[#e2d5c1] bg-[#ebe1d1]/30">
        <Container size="lg">
          <div className="space-y-2 mb-10">
            <Badge variant="stamp">RELATED NOTES</Badge>
            <h3 className="font-serif text-2xl sm:text-3xl font-normal text-[#2a1c12]">
              More publications from LaSalle Street
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {relatedArticles.map((rel) => (
              <Link
                key={rel.id}
                href={`/insights/${rel.slug}`}
                className="group border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-8 flex flex-col justify-between shadow-[0_4px_20px_rgba(42,28,18,0.03)] hover:border-[#cfbe9e] transition-all hover:-translate-y-1"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs font-mono text-[#85725f]">
                    <Badge variant="stamp">{rel.category}</Badge>
                    <span>{rel.readTime}</span>
                  </div>

                  <h4 className="font-serif text-xl sm:text-2xl font-normal text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors">
                    {rel.title}
                  </h4>

                  <p className="text-xs text-[#5b4a3b] leading-[1.6] line-clamp-2">
                    {rel.excerpt || rel.subtitle}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-[#e2d5c1] flex items-center justify-between text-xs text-[#85725f]">
                  <span className="font-sans font-medium text-[#2a1c12]">{rel.author}</span>
                  <ArrowRight className="h-4 w-4 text-[#9a6a35] transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </section>

      {/* 5. Bottom Conflict Intake Banner */}
      <section className="py-16 sm:py-24 bg-[#24180f] text-[#f3ece1] border-t border-[#3f2c1f]">
        <Container size="xl">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <Badge variant="dark">LEGAL INQUIRIES</Badge>
            <h2 className="font-serif text-[36px] sm:text-[48px] font-normal leading-[1.0] text-[#f3ece1]">
              Discuss your matter with our partners.
            </h2>
            <p className="text-sm sm:text-base text-[#b8a695] leading-relaxed max-w-xl mx-auto">
              We clear conflicts the same business day. Consult directly with the partner who authoritatively handles your legal challenge.
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
    </article>
  );
}
