import { NavItem } from "@/types";

export const navigationLinks: NavItem[] = [
  {
    label: "Legal Areas",
    href: "/practices",
    children: [
      {
        label: "Civil & Property",
        href: "/practices#civil",
        description: "Partition suits, title deeds, injunctions & RERA builder disputes",
      },
      {
        label: "Criminal & Bail",
        href: "/practices#criminal",
        description: "Bharatiya Nyaya Sanhita (BNS), Anticipatory Bail under BNSS & FIR quashing",
      },
      {
        label: "Corporate & Startups",
        href: "/practices#corporate",
        description: "Founder agreements, Companies Act 2013 compliance & equity financing",
      },
      {
        label: "Cheque Bounce (138 NI)",
        href: "/practices#cheque-bounce",
        description: "Statutory 15-day notices, summary recovery suits & commercial courts",
      },
      {
        label: "Family & Matrimonial",
        href: "/practices#family",
        description: "Mutual consent divorce, child custody, maintenance & family settlements",
      },
      {
        label: "Consumer & Cyber",
        href: "/practices#consumer",
        description: "Consumer Protection Act 2019, cyber fraud portal 1930 & IT Act claims",
      },
    ],
  },
  { label: "Find Advocates", href: "/people" },
  { label: "Precedents", href: "/matters" },
  { label: "Legal Guides", href: "/insights" },
  { label: "About Us", href: "/firm" },
];
