import { TimelineMilestone, WrittenCommitment, ClientProfile } from "@/types";

export const firmTimeline: TimelineMilestone[] = [
  {
    year: "2011",
    title: "Founding on LaSalle Street",
    description: "Margaret Ellery (former federal prosecutor) and Tomasz Kowal (national corporate partner) open Ellery Kowal LLP at 224 S. LaSalle Street with four lawyers, focusing on trials and private company M&A.",
    keyMatters: ["Founding charter with zero associate leverage ratio", "First commercial trial verdict in Cook County"],
  },
  {
    year: "2014",
    title: "Expansion into White-Collar Defense",
    description: "Marcus Leland joins as investigations partner after eleven years at the U.S. Attorney's Office, establishing the government investigations and grand jury response practice.",
    keyMatters: ["Representation in multi-state healthcare fraud probe", "Secured complete SEC regulatory declination"],
  },
  {
    year: "2017",
    title: "Trial Record Milestones & Real Estate",
    description: "Owen Pryce joins commercial trials from a national litigation firm, and Helen Brandt arrives to lead commercial real estate during Chicago's West Loop development surge.",
    keyMatters: ["$18.4M jury trial verdict in federal court", "$47M Fulton Market headquarters acquisition"],
  },
  {
    year: "2020",
    title: "Employment & Restrictive Covenants",
    description: "Danielle Okafor joins as employment partner, advising boards on executive separations and non-compete enforcement following Illinois Freedom to Work Act reforms.",
    keyMatters: ["Emergency TRO halting defecting sales team", "Independent board investigation for regional healthcare system"],
  },
  {
    year: "2023",
    title: "IP, Privacy & Technology Practice",
    description: "Arjun Sethi arrives to lead IP, software licensing, and privacy defense, defending Midwest employers against Illinois Biometric Information Privacy Act (BIPA) claims.",
    keyMatters: ["Complete defense dismissal of 60-location BIPA class action", "Remediation of OSS code risk in $140M acquisition"],
  },
  {
    year: "2026",
    title: "Fifteen Years at 224 S. LaSalle",
    description: "Seven partners and thirty-four counsel and associates now occupy the entire 31st floor of 224 S. LaSalle, maintaining the firm's foundational partner-led operational model.",
    keyMatters: ["Over sixty company sales completed", "Thirty-four commercial cases tried to verdict"],
  },
];

export const writtenCommitments: WrittenCommitment[] = [
  {
    id: "commitment-1",
    number: "01",
    title: "No Surprise Invoices",
    summary: "Every commercial trial, transaction, and investigation includes an agreed written 90-day phase budget or fixed fee. We never invoice beyond our written estimate without prior written consent.",
    fullPolicy: "Before any work commences, the lead partner delivers a written engagement letter with a phased budget schedule. Each month, the client receives a single-page reconciliation report detailing actual hours, fees, and remaining budget capacity. If an unforeseen procedural development arises in court, we notify the client in writing before incurring additional costs.",
    artifactTitle: "Schedule B · Phased Budget Agreement & Reconciliation Protocol",
  },
  {
    id: "commitment-2",
    number: "02",
    title: "The Partner on the Call",
    summary: "When you retain Ellery Kowal, the partner you interviewed is the one who reads your contract, takes your key depositions, and appears before the judge. We do not use client work to train junior associates.",
    fullPolicy: "Traditional law firms maintain leverage ratios of five to seven associates per partner. At Ellery Kowal, all seven named partners personally conduct substantive case analysis. Associating counsel and senior associates perform targeted research and document management, but every strategic decision and court appearance is executed directly by the partner on the door.",
    artifactTitle: "Operational Policy 4 · Senior Partner Staffing Guarantee",
  },
  {
    id: "commitment-3",
    number: "03",
    title: "Real Deadlines",
    summary: "We treat legal deadlines with the urgency of trial dates. If an intake inquiry is received before noon, conflict clearances are completed the same business day.",
    fullPolicy: "Legal matters stall when law firms prioritize internal billable quotas over client velocity. Our firm operates on strict operational turnaround SLAs: same-day conflict checks, 48-hour turnarounds for commercial contract markups, and immediate 24-hour mobilization for emergency restraining orders.",
    artifactTitle: "Service Standard 1 · Client Turnaround & Availability SLA",
  },
  {
    id: "commitment-4",
    number: "04",
    title: "Plain English Writing",
    summary: "Our briefs, contracts, and advice memos are drafted for judges, juries, and business owners—not for law review editors. We write with brevity, precision, and zero Latin fillers.",
    fullPolicy: "Dense, archaic legal boilerplate is a sign of insecure drafting that obscures commercial risk. Our attorneys draft contracts that can be understood across boardroom tables and trial briefs that federal judges can read in fifteen minutes. Every sentence must serve as clear, persuasive evidence.",
    artifactTitle: "Drafting Standard 7 · Clarity, Brevity & Trial-Ready Language",
  },
];

export const clientProfiles: ClientProfile[] = [
  {
    id: "founders-family",
    title: "Founders & Family-Owned Companies",
    description: "Second- and third-generation private businesses navigating company sales, private equity recapitalizations, executive departures, and commercial contract negotiations.",
    typicalMatters: [
      "Sell-side representation in $15M–$300M transactions",
      "Rollover equity structuring & tax planning",
      "Key executive non-compete agreements",
      "Outside general counsel governance maintenance",
    ],
  },
  {
    id: "mid-market",
    title: "Regional & Middle-Market Corporations",
    description: "Midwest manufacturers, logistics carriers, real estate developers, and software companies requiring trial-ready defense and high-stakes commercial counsel.",
    typicalMatters: [
      "Commercial contract breach litigation before federal & state courts",
      "Commercial arbitration before AAA and JAMS",
      "West Loop and suburban commercial lease negotiations",
      "BIPA privacy audits and software licensing agreements",
    ],
  },
  {
    id: "general-counsel",
    title: "General Counsel & Board Special Committees",
    description: "Corporate legal departments seeking specialized conflict counsel, trial co-counsel, or independent investigators for sensitive internal inquiries.",
    typicalMatters: [
      "Grand jury subpoena responses & DOJ inquiries",
      "Audit committee whistleblower investigations",
      "Emergency temporary restraining orders & trade secrets",
      "Adverse party conflict overflow counsel",
    ],
  },
];

export const proBonoDetails = {
  title: "LaSalle Street Small Business Legal Clinic",
  founded: "2014",
  hoursAnnually: "1,200+ hours",
  mission: "Every attorney at Ellery Kowal devotes at least 50 hours annually to pro bono representation. On the second Friday of each month, our partners open the 31st floor conference rooms to provide free legal advice to Chicago minority- and female-owned small businesses, non-profit community organizations, and military veterans navigating commercial leases, corporate formation, and municipal licensing.",
  partnerInCharge: "Margaret Ellery & Danielle Okafor",
  contactEmail: "probono@ellerykowal.com",
};

