import * as React from "react";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";

export const metadata = {
  title: "Legal Notice & Disclaimers · Ellery Kowal LLP",
  description:
    "Regulatory disclosures, attorney advertising notice, and professional conduct limitations of Ellery Kowal LLP under Illinois and federal rules.",
};

export default function DisclaimerPage() {
  const notices = [
    {
      title: "Attorney Advertising Notice",
      content:
        "This website and its associated publications, articles, case summaries, and marketing materials may be considered Attorney Advertising under the Illinois Rules of Professional Conduct (Rules 7.1 through 7.5) and the disciplinary rules of other jurisdictions in which our attorneys are admitted to practice.",
    },
    {
      title: "No Attorney-Client Relationship Formed",
      content:
        "The transmission of an inquiry, completion of our online conflict intake check, or exchange of electronic mail with Ellery Kowal LLP or any of its partners, counsel, or associates does not create an attorney-client relationship. An attorney-client relationship is formed only upon the execution of a written engagement letter countersigned by an authorized partner of the Firm following formal conflict clearance.",
    },
    {
      title: "Prior Results Do Not Guarantee Future Outcomes",
      content:
        "Case summaries, representative matters, trial verdict amounts, arbitration awards, and transaction values presented on this website reflect historical outcomes. Every legal dispute and commercial transaction turns upon unique statutory, evidentiary, jurisdictional, and factual circumstances. Prior results do not guarantee, promise, or predict a similar outcome in any future legal matter.",
    },
    {
      title: "No Legal Advice or Formal Legal Opinion",
      content:
        "The content provided on this website, including partner-authored insights, checklists, contract commentary, and statutory analyses, is provided solely for general informational and educational purposes. It does not constitute legal advice, nor should it be relied upon as a substitute for competent legal counsel tailored to your specific situation.",
    },
    {
      title: "Jurisdictional Practice & Bar Admissions",
      content:
        "Attorneys at Ellery Kowal LLP are licensed to practice law in the state courts of Illinois, New York, and specific federal district and appellate courts as identified on their individual attorney profile biographies. The Firm does not seek to represent clients in jurisdictions where our attorneys are not authorized to practice law or where this website fails to comply with all applicable legal or ethical rules.",
    },
    {
      title: "Electronic Communications & Confidentiality Warning",
      content:
        "Do not send confidential, proprietary, or privileged information to the Firm through this website or via email until you have received written confirmation of conflict clearance and executed a formal retention letter. Unsolicited information sent to the Firm cannot be treated as confidential and will not prevent us from representing an adverse party in related or unrelated matters.",
    },
    {
      title: "Designated Responsible Attorney",
      content:
        "In compliance with the Illinois Rules of Professional Conduct, the attorney responsible for the content and management of this website is Margaret Ellery, Managing Partner, Ellery Kowal LLP, 224 S. LaSalle Street, 31st Floor, Chicago, IL 60604. Direct telephone: (312) 555-0152.",
    },
  ];

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* Header */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="lg">
          <div className="max-w-3xl space-y-4">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">LEGAL NOTICE</Badge>
              <span className="text-xs font-mono text-[#85725f]">Regulatory Disclosures</span>
            </div>
            <h1 className="font-serif text-[40px] sm:text-[56px] lg:text-[68px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
              Legal Notice & Disclaimers
            </h1>
            <p className="text-sm sm:text-base text-[#5b4a3b] leading-relaxed">
              Disclosures, attorney advertising regulations, and ethical guidelines governing communications with Ellery Kowal LLP.
            </p>
          </div>
        </Container>
      </section>

      {/* Notices */}
      <section className="py-16 sm:py-20 lg:py-24">
        <Container size="lg">
          <div className="space-y-8">
            {notices.map((n, idx) => (
              <div
                key={idx}
                className="border border-[#e2d5c1] bg-[#fffaf2] p-8 sm:p-10 shadow-[0_4px_20px_rgba(42,28,18,0.03)] space-y-3"
              >
                <div className="flex items-center space-x-3 border-b border-[#e2d5c1] pb-3">
                  <span className="font-serif text-2xl text-[#9a6a35] font-normal">
                    0{idx + 1}
                  </span>
                  <h2 className="font-serif text-xl sm:text-2xl font-normal text-[#2a1c12]">
                    {n.title}
                  </h2>
                </div>
                <p className="text-xs sm:text-sm text-[#5b4a3b] leading-[1.75] pt-1">
                  {n.content}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-16 pt-8 border-t border-[#e2d5c1] flex items-center justify-between text-xs text-[#85725f]">
            <span>Ellery Kowal LLP · 224 S. LaSalle Street, Chicago, IL 60604</span>
            <Link href="/privacy" className="hover:text-[#2a1c12] hover:underline">
              Privacy Notice →
            </Link>
          </div>
        </Container>
      </section>
    </div>
  );
}

