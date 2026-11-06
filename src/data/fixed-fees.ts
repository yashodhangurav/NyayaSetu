import { FixedFee } from "@/types";

export const fixedFees: FixedFee[] = [
  {
    id: "growth-advisory",
    title: "Fractional Corporate Counsel",
    description: "Ongoing executive legal governance, commercial contract review, and board advisory for scaling enterprises.",
    price: "$7,500",
    period: "per month",
    features: [
      "Dedicated Partner-level point of contact",
      "Up to 20 hours of monthly corporate & commercial advisory",
      "Priority review turnaround within 24 hours",
      "Board meeting preparation and attendance",
      "Standard contract templates & repository access",
    ],
    popular: false,
    ctaText: "Engage Advisory",
  },
  {
    id: "transaction-readiness",
    title: "M&A & Deal Readiness Audit",
    description: "Comprehensive due diligence and structural clean-up package preparing firms for investment or acquisition.",
    price: "$18,500",
    period: "fixed engagement",
    features: [
      "Corporate charter, cap table & capitalization review",
      "Key commercial contracts & IP assignment audits",
      "Regulatory & data compliance risk assessment",
      "Definitive Red-Flag Due Diligence Memorandum",
      "Virtual Data Room (VDR) curation and structuring",
      "Direct investor presentation consultation",
    ],
    popular: true,
    ctaText: "Schedule Audit",
  },
  {
    id: "private-wealth-structuring",
    title: "Estate & Family Office Governance",
    description: "Comprehensive multi-jurisdictional asset protection, family charter, and generational trust structuring.",
    price: "$24,000",
    period: "fixed foundation",
    features: [
      "Bespoke revocable & irrevocable trust documentation",
      "Family constitution & governance framework",
      "Cross-border tax & estate strategy alignment",
      "Asset transfer deeds & entity restructuring",
      "Fiduciary appointments & succession protocol",
    ],
    popular: false,
    ctaText: "Request Consultation",
  },
];

