export interface Lawyer {
  id: string;
  name: string;
  role: string;
  practice: string;
  bio: string;
  inPracticeYears: number;
  admissions: string[];
  education: string[];
  priorExperience?: string;
  keyResults: string[];
  phone: string;
  email: string;
  image: string;
  isPartner: boolean;
}

export type Partner = Lawyer;

export interface Practice {
  id: string;
  slug: string;
  num?: string;
  title: string;
  tagline?: string;
  description: string;
  shortDescription?: string;
  fullDescription?: string;
  startingFee?: string;
  feeType?: string;
  feeBasis?: string;
  feeDetail?: string;
  partnerNames?: string;
  partnerIds?: string[];
  image?: string;
  iconName?: string;
  whatWeHandle?: string[];
  keyServices?: string[];
  whenClientsCall?: string[];
  whereWeArgue?: string[];
  mattersCount?: number;
  results?: { metric: string; description: string; forum: string }[];
}

export type PracticeArea = Practice;

export interface Matter {
  id: string;
  slug?: string;
  result?: string;
  resultUnit?: string;
  title: string;
  summary: string;
  whatHappened?: string;
  outcome?: string;
  leadPartner?: string;
  leadLawyerId?: string;
  practice?: string;
  clientType?: string;
  forum?: string;
  year: string;
  category: string;
}

export interface Article {
  id: string;
  slug: string;
  title: string;
  subtitle?: string;
  excerpt?: string;
  content?: string;
  category: string;
  date?: string;
  publishedDate?: string;
  readTime: string;
  author: string;
  authorRole?: string;
  authorPractice?: string;
  authorImage?: string;
  pullQuote?: string;
  paragraphs?: string[];
  takeaways?: string[];
  image: string;
}

export interface Testimonial {
  id: string;
  quote: string;
  role: string;
  author?: string;
  company: string;
  clientSince?: string;
  avatar?: string;
  rating?: number;
}

export interface FAQ {
  id: string;
  question: string;
  answer: string;
  category?: string;
}

export interface TimelineMilestone {
  year: string;
  title: string;
  description: string;
  keyMatters?: string[];
}

export interface WrittenCommitment {
  id: string;
  number: string;
  title: string;
  summary: string;
  fullPolicy: string;
  artifactTitle: string;
}

export interface ClientProfile {
  id: string;
  title: string;
  description: string;
  typicalMatters: string[];
}

export interface FixedFee {
  id: string;
  service?: string;
  title?: string;
  fee?: string;
  price?: string;
  period?: string;
  timeline?: string;
  description: string;
  included?: string[];
  features?: string[];
  popular?: boolean;
  ctaText?: string;
}

export interface NavChild {
  label: string;
  href: string;
  description?: string;
}

export interface NavItem {
  label: string;
  href: string;
  children?: NavChild[];
}

export interface ConflictCheckFormData {
  fullName: string;
  companyName: string;
  email: string;
  phone: string;
  matterType: string;
  adverseParties: string;
  urgency: "urgent-48h" | "upcoming-30d" | "none-yet";
  preferredDate?: string;
  preferredTime?: string;
  nonConfidentialAcknowledged: boolean;
}

export interface FormErrors {
  fullName?: string;
  companyName?: string;
  email?: string;
  phone?: string;
  matterType?: string;
  adverseParties?: string;
  nonConfidentialAcknowledged?: string;
}
