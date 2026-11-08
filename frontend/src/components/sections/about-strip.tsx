"use client";

import Image from "next/image";
import { Container } from "@/components/layout/container";

export function AboutStrip() {
  const metrics = [
    { value: "6", label: "Languages: EN, HI, KN, MR, TA, TE" },
    { value: "2,800+", label: "Verified advocates enrolled" },
    { value: "28", label: "High Courts & tribunals covered" },
    { value: "100%", label: "Transparent consultation models" },
  ];

  return (
    <section aria-label="About the platform" className="border-b border-[#e2d5c1] bg-[#f4efe6] py-20 lg:py-28">
      <Container size="xl">
        {/* Top: Header Pill with Avatars */}
        <div className="flex items-center space-x-3 mb-8">
          <div className="flex -space-x-1.5 overflow-hidden">
            <div className="relative h-7 w-7 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
              <Image
                src="https://framerusercontent.com/images/0LArNLIabDDiZZoFMZhtVP1Dudc.webp?width=720&height=900"
                alt="Advocate portrait"
                fill
                className="object-cover object-[50%_15%]"
              />
            </div>
            <div className="relative h-7 w-7 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
              <Image
                src="https://framerusercontent.com/images/aduozO96ZbkNp24VgIVFxOelF4.webp?width=720&height=900"
                alt="Advocate portrait"
                fill
                className="object-cover object-[50%_15%]"
              />
            </div>
            <div className="relative h-7 w-7 rounded-full ring-2 ring-[#f4efe6] overflow-hidden bg-[#ebe1d1]">
              <Image
                src="https://framerusercontent.com/images/aP4i3MQtE6NvStb54fOi7D2gxG8.webp?width=720&height=900"
                alt="Advocate portrait"
                fill
                className="object-cover object-[50%_15%]"
              />
            </div>
          </div>
          <span className="text-[14px] font-sans font-semibold text-[#2a1c12] tracking-tight">
            About the platform
          </span>
        </div>

        {/* Large Editorial Lead Statement */}
        <div className="max-w-5xl mb-14 lg:mb-16">
          <h2 className="font-serif text-[28px] sm:text-[38px] lg:text-[46px] leading-[1.14] tracking-[-0.035em] font-normal text-[#2a1c12]">
            NyayaSetu simplifies complex legal problems into clear steps, document guidance, and advocate connections,{" "}
            <span className="text-[#85725f]">
              so every citizen can understand their legal position before making critical decisions.
            </span>
          </h2>
        </div>

        {/* 2 Photos & Narrative Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-8 lg:gap-12 items-start mb-16 lg:mb-20">
          {/* Photo 1: Judicial Heritage Entrance (4 cols) */}
          <div className="lg:col-span-4 relative aspect-[4/5] overflow-hidden rounded-[2px] bg-[#ebe1d1]">
            <Image
              src="https://framerusercontent.com/images/bhhAOZcQmJaXBnbcUcjp1ROF948.webp?width=960&height=1200"
              alt="Judicial court entrance in morning light"
              fill
              sizes="(max-width: 600px) 100vw, (max-width: 1024px) 50vw, 380px"
              className="object-cover object-center"
            />
          </div>

          {/* Center: Two Narrative Paragraphs (4 cols) */}
          <div className="lg:col-span-4 space-y-6 text-[15.5px] leading-[1.65] text-[#5b4a3b]">
            <p>
              Navigating the legal system in India can feel intimidating. Complex statutory language, uncertain procedural timelines, and opaque fees often leave citizens and entrepreneurs unsure of their first step.
            </p>
            <p>
              NyayaSetu provides an accessible, human-friendly bridge: preliminary AI-assisted case assessment, document checklists, and transparent discovery of verified Bar Council advocates across District Courts, High Courts, and the Supreme Court.
            </p>
          </div>

          {/* Photo 2: Advocate Chamber / Consultation Area (4 cols) */}
          <div className="lg:col-span-4 relative aspect-[4/3] lg:aspect-[4/5] overflow-hidden rounded-[2px] bg-[#ebe1d1]">
            <Image
              src="https://framerusercontent.com/images/REfcmzt4mPpUJT1GGSseLryjp1g.webp?width=1200&height=900"
              alt="Advocate consultation chamber"
              fill
              sizes="(max-width: 600px) 100vw, (max-width: 1024px) 50vw, 380px"
              className="object-cover object-center"
            />
          </div>
        </div>

        {/* Bottom: 4 Stats Bar */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 border-t border-[#e2d5c1] pt-10">
          {metrics.map((metric) => (
            <div key={metric.label} className="border-l-2 border-[#9a6a35] pl-5 space-y-1">
              <div className="font-serif text-[42px] sm:text-[54px] leading-none font-normal text-[#2a1c12]">
                {metric.value}
              </div>
              <div className="text-sm font-sans font-medium text-[#705c49] pt-1">
                {metric.label}
              </div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
