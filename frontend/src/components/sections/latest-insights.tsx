"use client";

import * as React from "react";
import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/container";

interface InsightPost {
  slug: string;
  category: string;
  author: string;
  date: string;
  readTime: string;
  title: string;
  image: string;
}

const homepageInsights: InsightPost[] = [
  {
    slug: "non-compete-clauses-section-27-indian-contract-act",
    category: "Contracts & Labor",
    author: "Adv. Rajeshwari Sen",
    date: "Sep 18, 2026",
    readTime: "4 min read",
    title: "Why post-employment non-compete clauses are void in India under Section 27",
    image: "https://framerusercontent.com/images/1P4ZiDmUViRZSPDF7pkkL0gc.webp?width=1200&height=900",
  },
  {
    slug: "bns-2023-procedural-changes-bail-guidelines",
    category: "Criminal Law & BNSS",
    author: "Adv. Harshvardhan Kapoor",
    date: "Aug 27, 2026",
    readTime: "5 min read",
    title: "Bharatiya Nyaya Sanhita 2023 vs IPC: 5 procedural bail changes citizens must know",
    image: "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=900",
  },
  {
    slug: "cyber-banking-fraud-1930-golden-window",
    category: "Consumer & Cyber",
    author: "Adv. Ananya Sundaram",
    date: "Aug 4, 2026",
    readTime: "4 min read",
    title: "The 48-hour golden window: how to report cyber banking fraud on National Portal 1930",
    image: "https://framerusercontent.com/images/CZFM2PYLPboBXfjd97sEto88.webp?width=1200&height=900",
  },
];

export function LatestInsights() {
  return (
    <section className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-12 sm:mb-16 gap-6">
          <h2 className="font-serif text-[40px] sm:text-[52px] lg:text-[62px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
            Kanoon Gyaan. <span className="text-[#a89682]">Plain language.</span>
          </h2>

          <Link
            href="/insights"
            className="inline-flex items-center px-5 py-2.5 border border-[#2a1c12] text-[#2a1c12] hover:bg-[#2a1c12] hover:text-[#fffaf2] transition-colors text-[13.5px] font-medium rounded-[2px]"
          >
            All legal guides
          </Link>
        </div>

        {/* 3-Column Editorial Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {homepageInsights.map((post) => (
            <Link
              key={post.slug}
              href={`/insights/${post.slug}`}
              className="group space-y-4"
            >
              {/* Image with Tag Badge */}
              <div className="relative aspect-[16/10] w-full rounded-md overflow-hidden border border-[#e2d5c1] bg-[#ebe1d1]">
                <Image
                  src={post.image}
                  alt={post.title}
                  fill
                  sizes="(max-width: 768px) 100vw, 33vw"
                  className="object-cover object-center filter contrast-[1.02] transition-transform duration-500 group-hover:scale-105"
                />
                <div className="absolute top-3 left-3 z-10">
                  <span className="px-2.5 py-1 bg-[#fffaf2]/90 backdrop-blur-xs border border-[#e2d5c1] text-[11px] font-medium text-[#2a1c12] rounded-[2px]">
                    {post.category}
                  </span>
                </div>
              </div>

              {/* Author & Date/Read Time */}
              <div className="flex items-center justify-between text-[12.5px] text-[#85725f] pt-1">
                <span>{post.author}</span>
                <span>
                  {post.date} · {post.readTime}
                </span>
              </div>

              {/* Headline */}
              <h3 className="font-serif text-[21px] sm:text-[23px] font-normal leading-[1.25] text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors">
                {post.title}
              </h3>
            </Link>
          ))}
        </div>
      </Container>
    </section>
  );
}
