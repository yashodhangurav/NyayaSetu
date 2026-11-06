import * as React from "react";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";

export const metadata = {
  title: "Privacy Notice · Ellery Kowal LLP",
  description:
    "Privacy notice of Ellery Kowal LLP governing client intake, adverse conflict screening data, retention under Illinois ethics rules, and web communications.",
};

export default function PrivacyPage() {
  const sections = [
    {
      num: "01",
      title: "Identity of the Data Controller & Scope",
      content:
        "This Privacy Notice governs the collection, use, and retention of personal and corporate information by Ellery Kowal LLP, an Illinois limited liability partnership located at 224 S. LaSalle Street, 31st Floor, Chicago, IL 60604 ('the Firm', 'we', 'our'). This notice applies to information collected through this website, our conflict clearance portal, electronic mail, and preliminary intake consultations.",
    },
    {
      num: "02",
      title: "Information Collected via Preliminary Intake",
      content:
        "When prospective clients, in-house counsel, or corporate officers submit inquiries or initiate conflict checks, we collect: full names, business titles, corporate entity affiliations, business email addresses, direct telephone numbers, matter practice descriptions, and disclosed adverse individuals or corporate entities necessary to perform conflicts clearance.",
    },
    {
      num: "03",
      title: "Purpose of Processing: Conflict Screening",
      content:
        "Information submitted via our intake portal is processed exclusively to: (i) identify whether representation would create a concurrent or successive conflict of interest under the Illinois Rules of Professional Conduct (Rules 1.7, 1.8, 1.9, and 1.10); (ii) evaluate whether the Firm possesses the requisite expertise; and (iii) communicate the results of our conflict clearance to prospective clients.",
    },
    {
      num: "04",
      title: "Non-Privilege of Preliminary Submissions",
      content:
        "Submitting preliminary information through this website or by electronic mail does not create an attorney-client relationship. Until a formal engagement letter is signed by an Ellery Kowal partner, preliminary transmissions are not protected by attorney-client privilege. Prospective clients are advised not to disclose trade secrets, trial strategy, or highly sensitive corporate communications in early online forms.",
    },
    {
      num: "05",
      title: "Retention Schedules under Illinois Supreme Court Rules",
      content:
        "We retain conflict check search logs and adverse party lists in accordance with Illinois Supreme Court Rule 769 and professional liability obligations for a minimum of seven (7) years following the inquiry date. If formal representation is declined or a conflict exists, adverse data is sequestered in an internal conflicts database to prevent future conflicting representations.",
    },
    {
      num: "06",
      title: "Confidentiality & Information Security Standards",
      content:
        "The Firm implements physical, electronic, and procedural safeguards in compliance with federal and state cybersecurity frameworks. All online intake submissions are encrypted in transit using Transport Layer Security (TLS 1.3) and stored in access-restricted data repositories accessible only by our conflicts committee, general counsel, and intake partners.",
    },
    {
      num: "07",
      title: "Third-Party Disclosures & No-Sale Commitment",
      content:
        "Ellery Kowal LLP does not sell, lease, monetize, or commercialize personal or corporate information. Information is disclosed to third parties only where: (i) required by court subpoena or valid law enforcement order; (ii) necessary for vetted cloud hosting and e-discovery infrastructure bound by strict confidentiality; or (iii) with express client authorization.",
    },
    {
      num: "08",
      title: "Cookies, Server Logs & Web Analytics",
      content:
        "Our web server automatically logs routine technical diagnostic telemetry, including IP addresses, browser types, referring pages, and access timestamps. We use strictly necessary session cookies to maintain navigation state and preserve responsive UI preferences. We do not deploy third-party advertising tracking pixels or commercial ad retargeting networks.",
    },
    {
      num: "09",
      title: "CCPA / CPRA & European Data Rights",
      content:
        "To the extent applicable under the California Consumer Privacy Act (CCPA/CPRA), the General Data Protection Regulation (GDPR), or state privacy legislation, individuals have the right to request access to, correction of, or deletion of their personal information, subject to statutory exemptions for legal records retained pursuant to judicial or professional responsibility obligations.",
    },
    {
      num: "10",
      title: "Communications & Newsletter Opt-Out",
      content:
        "Prospective clients and colleagues who subscribe to our quarterly LaSalle Street legal briefing may unsubscribe at any time by clicking the unsubscribe link in any bulletin or by emailing intake@ellerykowal.com with the subject line 'Unsubscribe'.",
    },
    {
      num: "11",
      title: "Children's Online Privacy Protection",
      content:
        "This website is designed for corporate executives, legal professionals, and commercial enterprises. We do not knowingly solicit, collect, or maintain information from individuals under eighteen (18) years of age.",
    },
    {
      num: "12",
      title: "Data Protection Inquiries & Office Contact",
      content:
        "Inquiries regarding this Privacy Notice or our conflict data handling practices should be directed to our Administrative Partner: Ellery Kowal LLP, Attn: Conflicts & Privacy Committee, 224 S. LaSalle Street, 31st Floor, Chicago, IL 60604. Email: privacy@ellerykowal.com. Telephone: (312) 555-0147.",
    },
  ];

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* Header */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="lg">
          <div className="max-w-3xl space-y-4">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">PRIVACY NOTICE</Badge>
              <span className="text-xs font-mono text-[#85725f]">Last Updated: February 2026</span>
            </div>
            <h1 className="font-serif text-[40px] sm:text-[56px] lg:text-[68px] leading-[1.0] tracking-[-0.04em] font-normal text-[#2a1c12]">
              Privacy & Conflict Data Notice
            </h1>
            <p className="text-sm sm:text-base text-[#5b4a3b] leading-relaxed">
              Governing information collection, adverse conflicts screening, and data retention standards at Ellery Kowal LLP under Illinois and federal rules.
            </p>
          </div>
        </Container>
      </section>

      {/* 12 Sections */}
      <section className="py-16 sm:py-20 lg:py-24">
        <Container size="lg">
          <div className="space-y-12">
            {sections.map((sec) => (
              <div
                key={sec.num}
                className="border border-[#e2d5c1] bg-[#fffaf2] p-8 sm:p-10 shadow-[0_4px_20px_rgba(42,28,18,0.03)] space-y-3"
              >
                <div className="flex items-center space-x-3 border-b border-[#e2d5c1] pb-3">
                  <span className="font-serif text-2xl text-[#9a6a35] font-normal">
                    {sec.num}
                  </span>
                  <h2 className="font-serif text-xl sm:text-2xl font-normal text-[#2a1c12]">
                    {sec.title}
                  </h2>
                </div>
                <p className="text-xs sm:text-sm text-[#5b4a3b] leading-[1.75] pt-1">
                  {sec.content}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-16 pt-8 border-t border-[#e2d5c1] flex items-center justify-between text-xs text-[#85725f]">
            <span>Ellery Kowal LLP · 224 S. LaSalle Street, Chicago, IL 60604</span>
            <Link href="/disclaimer" className="hover:text-[#2a1c12] hover:underline">
              Legal Notice & Disclaimers →
            </Link>
          </div>
        </Container>
      </section>
    </div>
  );
}

