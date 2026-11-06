import { HeroSection } from "@/components/sections/hero-section";
import { AboutStrip } from "@/components/sections/about-strip";
import { PracticesSlider } from "@/components/sections/practices-slider";
import { TransparencyPreview } from "@/components/sections/transparency-preview";
import { ContractAnnotator } from "@/components/sections/contract-annotator";
import { MattersPreview } from "@/components/sections/matters-preview";
import { PartnerShowcase } from "@/components/sections/partner-showcase";
import { ClientQuotes } from "@/components/sections/client-quotes";
import { LatestInsights } from "@/components/sections/latest-insights";
import { FaqSection } from "@/components/sections/faq-section";
import { ConflictIntakeSection } from "@/components/sections/conflict-intake-section";

export const metadata = {
  title: "NyayaSetu (न्यायसेतु) · AI Legal Advisor & Advocate Matching Platform · India",
  description:
    "Legal Help Should Be Clear. Justice Should Be Accessible. Preliminary AI statutory assessment, Bar Council-verified advocate matching, court tracking, and multilingual legal support for Indian citizens and MSMEs.",
};

export default function HomePage() {
  return (
    <div className="flex flex-col bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Hero Section */}
      <HeroSection />

      {/* 2. About Firm Overview & Metrics */}
      <AboutStrip />

      {/* 3. Practices Carousel */}
      <PracticesSlider />

      {/* 4. Transparency & Fee Models */}
      <TransparencyPreview />

      {/* 5. Interactive Contract Annotator */}
      <ContractAnnotator />

      {/* 6. Representative Matters Ledger Preview */}
      <MattersPreview />

      {/* 7. Partner Showcase */}
      <PartnerShowcase />

      {/* 8. Client Testimonials */}
      <ClientQuotes />

      {/* 9. Latest Insights */}
      <LatestInsights />

      {/* 10. Frequently Asked Questions */}
      <FaqSection />

      {/* 11. Conflict Check Intake */}
      <ConflictIntakeSection />
    </div>
  );
}
