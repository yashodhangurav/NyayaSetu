export interface ClientInstitution {
  id: string;
  name: string;
  logo: string;
  description: string;
  category: string;
}

export const clientInstitutions: ClientInstitution[] = [
  {
    id: "apex-capital",
    name: "Apex Capital Partners",
    logo: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&q=80&w=240",
    description: "Midwest private equity fund managing over $1.2B in assets.",
    category: "Financial Institutions",
  },
  {
    id: "strata-ventures",
    name: "Strata Ventures",
    logo: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&q=80&w=240",
    description: "Chicago early and growth-stage B2B enterprise investor.",
    category: "Venture Capital",
  },
  {
    id: "meridian-holdings",
    name: "Meridian Logistics Group",
    logo: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&q=80&w=240",
    description: "Regional transportation and warehousing conglomerate.",
    category: "Corporate Enterprise",
  },
];
