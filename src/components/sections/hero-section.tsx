"use client";

import Image from "next/image";
import Link from "next/link";
import dynamic from "next/dynamic";
import { Container } from "@/components/layout/container";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import { LadyJusticeLoader } from "@/components/3d/lady-justice-canvas";

const LadyJustice3D = dynamic(
  () =>
    import("@/components/3d/lady-justice-canvas").then(
      (mod) => mod.LadyJusticeCanvas
    ),
  {
    ssr: false,
    loading: () => <LadyJusticeLoader />,
  }
);

export function HeroSection() {
  const practiceChips = [
    { label: "Find an Advocate", href: "/people" },
    { label: "Explore Legal Topics", href: "/practices" },
    { label: "For Advocates", href: "/contact?type=advocate" },
  ];

  return (
    <section className="relative overflow-hidden bg-[#f4efe6] py-6 sm:py-8 lg:py-0 lg:h-[calc(100vh-5rem)] min-h-[calc(100vh-5rem)] flex flex-col justify-center">
      {/* 1. Giant Background Watermark "NYAYA" */}
      <div
        className="pointer-events-none absolute bottom-[-15px] sm:bottom-0 left-0 right-0 overflow-hidden select-none z-0 flex justify-center"
        aria-hidden="true"
      >
        <span
          className="font-sans font-medium text-[130px] sm:text-[180px] md:text-[210px] lg:text-[240px] leading-[0.8] tracking-[-0.055em] text-transparent select-none"
          style={{
            backgroundImage:
              "linear-gradient(0deg, rgba(244, 239, 230, 0) 0%, rgb(233, 221, 202) 59%, rgb(227, 212, 189) 100%)",
            WebkitBackgroundClip: "text",
            backgroundClip: "text",
          }}
        >
          NYAYA
        </span>
      </div>

      <Container size="xl" className="relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-10 items-center">
          {/* Left Column: Heading, Avatars, Verdict, Actions (Cols 1-7) */}
          <div className="lg:col-span-7 space-y-3.5 sm:space-y-4 lg:space-y-3.5 xl:space-y-4">
            {/* Main Headline (Compact & Authoritative) */}
            <motion.h1
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className="font-serif text-[32px] sm:text-[42px] md:text-[48px] lg:text-[50px] xl:text-[56px] leading-[1.04] tracking-[-0.035em] font-normal text-[#2a1c12]"
            >
              Legal Help Should Be Clear.
              <br />
              Justice <span className="text-[#9a6a35]">Should Be Accessible.</span>
            </motion.h1>

            {/* Separator, Avatars & Language Support Details */}
            <motion.div
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.08, ease: [0.16, 1, 0.3, 1] }}
              className="pt-2.5 sm:pt-3 border-t border-[#e2d5c1]/60 flex items-center space-x-3.5"
            >
              <div className="flex -space-x-2 overflow-hidden">
                <div className="relative h-8 w-8 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
                  <Image
                    src="https://framerusercontent.com/images/0LArNLIabDDiZZoFMZhtVP1Dudc.webp?width=720&height=900"
                    alt="Senior Advocate"
                    fill
                    className="object-cover object-[50%_18%]"
                  />
                </div>
                <div className="relative h-8 w-8 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
                  <Image
                    src="https://framerusercontent.com/images/aduozO96ZbkNp24VgIVFxOelF4.webp?width=720&height=900"
                    alt="Advocate"
                    fill
                    className="object-cover object-[50%_18%]"
                  />
                </div>
                <div className="relative h-8 w-8 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
                  <Image
                    src="https://framerusercontent.com/images/aP4i3MQtE6NvStb54fOi7D2gxG8.webp?width=720&height=900"
                    alt="Advocate"
                    fill
                    className="object-cover object-[50%_18%]"
                  />
                </div>
                <div className="relative h-8 w-8 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
                  <Image
                    src="https://framerusercontent.com/images/9wg0juCfo5rrwm9BHnLZFuKX3g.webp?width=720&height=900"
                    alt="Advocate"
                    fill
                    className="object-cover object-[50%_18%]"
                  />
                </div>
              </div>
              <div className="text-[12.5px] leading-snug font-sans text-[#705c49]">
                Support in English & regional languages:
                <br />
                <span className="font-medium text-[#2a1c12]">Hindi, Kannada, Marathi, Tamil & Telugu</span>
              </div>
            </motion.div>

            {/* Verdict Statement / Suggested Tagline */}
            <motion.p
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.12, ease: [0.16, 1, 0.3, 1] }}
              className="text-[14px] sm:text-[15px] leading-[1.48] text-[#5b4a3b] max-w-xl"
            >
              <strong className="font-semibold text-[#2a1c12]">Understand your legal situation</strong>, explore your options, and connect with the right legal professional across District Courts, High Courts, and the Supreme Court.
            </motion.p>

            {/* Bottom Lede & Action Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.16, ease: [0.16, 1, 0.3, 1] }}
              className="pt-1 space-y-3"
            >
              <p className="text-[13.5px] sm:text-[14px] leading-[1.48] text-[#5b4a3b] max-w-lg">
                AI-assisted preliminary case assessment and Bar Council-verified advocates. We simplify complex Indian acts into clear steps, document checklists, and transparent consultations.
              </p>

              <div className="flex flex-wrap items-center gap-3 pt-1">
                {/* Compound Primary Button: Get Legal Help */}
                <Link
                  href="/contact"
                  className="group inline-flex items-center bg-[#2a1c12] text-[#fffaf2] hover:bg-[#9a6a35] transition-colors rounded-[2px] overflow-hidden shadow-xs"
                >
                  <span className="px-4.5 py-2.5 sm:px-5 sm:py-3 text-[14px] font-semibold tracking-tight">
                    Get Legal Help
                  </span>
                  <span className="flex items-center justify-center w-9 sm:w-10 h-full py-2.5 sm:py-3 border-l border-white/20 bg-[#fffaf2]/10 group-hover:bg-[#fffaf2]/20 transition-colors">
                    <ArrowRight className="h-4 w-4" />
                  </span>
                </Link>

                {/* Ghost Secondary Button: Explore Legal Topics */}
                <Link
                  href="/practices"
                  className="inline-flex items-center px-5 py-2.5 sm:px-5.5 sm:py-3 border-[1.5px] border-[#2a1c12] text-[#2a1c12] hover:bg-[#2a1c12] hover:text-[#fffaf2] transition-colors text-[14px] font-semibold rounded-[2px]"
                >
                  Explore Legal Topics
                </Link>
              </div>
            </motion.div>
          </div>

          {/* Right Column: Lady Justice with Concentric Seal Ring (Cols 8-12) */}
          <div className="lg:col-span-5 relative flex items-center justify-center h-full min-h-[380px] sm:min-h-[440px] lg:min-h-[480px] xl:min-h-[520px]">
            {/* Concentric Rotating / Static Circular Seal Ring */}
            <div
              className="absolute inset-0 flex items-center justify-center pointer-events-none select-none z-0"
              aria-hidden="true"
            >
              <svg
                viewBox="0 0 400 400"
                className="w-[320px] h-[320px] sm:w-[400px] sm:h-[400px] lg:w-[440px] lg:h-[440px] xl:w-[480px] xl:h-[480px] overflow-visible"
              >
                <defs>
                  <path
                    id="hero-seal-path"
                    d="M200,200 m-168,0 a168,168 0 1,1 336,0 a168,168 0 1,1 -336,0"
                  />
                </defs>
                <circle
                  cx="200"
                  cy="200"
                  r="196"
                  fill="none"
                  stroke="rgb(154, 106, 53)"
                  strokeWidth="1"
                  opacity="0.38"
                />
                <circle
                  cx="200"
                  cy="200"
                  r="142"
                  fill="none"
                  stroke="rgb(154, 106, 53)"
                  strokeWidth="1"
                  strokeDasharray="2 6"
                  opacity="0.45"
                />
                <g style={{ transformOrigin: "200px 200px" }}>
                  <text
                    style={{
                      fontFamily: "General Sans, sans-serif",
                      fontWeight: 500,
                      fontSize: "13px",
                      letterSpacing: "0.34em",
                      fill: "rgb(124, 82, 38)",
                    }}
                    opacity="0.5"
                  >
                    <textPath href="#hero-seal-path" textLength="1040">
                      NYAYASETU · AI LEGAL ADVISOR & ADVOCATE NETWORK · BHARAT · ESTABLISHED 2026 ·
                    </textPath>
                  </text>
                </g>
              </svg>
            </div>

            {/* Bronze 3D Statue */}
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.97 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
              className="relative z-10 w-[220px] sm:w-[280px] lg:w-[310px] xl:w-[335px] aspect-[1200/2406] drop-shadow-[0_12px_24px_rgba(42,28,18,0.12)] max-h-[calc(100vh-10rem)]"
            >
              <LadyJustice3D />
            </motion.div>

            {/* Floating Practice Chips on the Bottom Right */}
            <div className="hidden xl:flex flex-col space-y-2 absolute right-[-6px] bottom-1 z-20">
              {practiceChips.map((chip) => (
                <Link
                  key={chip.label}
                  href={chip.href}
                  className="group flex items-center justify-between border border-[#e2d5c1] bg-[#fffaf2]/90 backdrop-blur-md rounded-[2px] overflow-hidden hover:border-[#9a6a35] transition-all shadow-xs"
                >
                  <span className="px-3.5 py-2 text-[13px] font-semibold text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors whitespace-nowrap">
                    {chip.label}
                  </span>
                  <span className="flex items-center justify-center w-7 py-2 bg-[#2a1c12] text-[#fffaf2] group-hover:bg-[#9a6a35] transition-colors">
                    <span className="text-[14px] font-medium leading-none">+</span>
                  </span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
