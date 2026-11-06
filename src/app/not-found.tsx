import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight, ShieldAlert, FileText, Users, Scale, Search } from "lucide-react";

export default function NotFound() {
  const quickLinks = [
    {
      title: "Our Practices",
      desc: "Commercial litigation, corporate M&A, employment covenants, and investigations.",
      href: "/practices",
      icon: Scale,
    },
    {
      title: "Partners & Counsel",
      desc: "The 41 lawyers of Ellery Kowal LLP on the 31st floor of 224 S. LaSalle.",
      href: "/people",
      icon: Users,
    },
    {
      title: "Representative Matters",
      desc: "Public ledger of 16 commercial jury trials, business sales, and TRO injunctions.",
      href: "/matters",
      icon: FileText,
    },
    {
      title: "Start a Conflict Check",
      desc: "Same-day adverse party clearance for time-sensitive commercial matters.",
      href: "/contact",
      icon: ShieldAlert,
    },
  ];

  return (
    <div className="min-h-[80vh] bg-[#f3ece1] text-[#2a1c12] py-20 lg:py-32 flex items-center">
      <Container size="lg">
        <div className="max-w-3xl mx-auto space-y-10 text-center">
          {/* Badge & Code */}
          <div className="flex items-center justify-center space-x-3">
            <Badge variant="stamp">ERROR 404</Badge>
            <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
              RECORD NOT FOUND · LASALLE STREET
            </span>
          </div>

          {/* Heading */}
          <div className="space-y-4">
            <h1 className="font-serif text-[48px] sm:text-[72px] lg:text-[88px] leading-[0.95] tracking-[-0.04em] font-normal text-[#2a1c12]">
              Docket entry does not exist.
            </h1>
            <p className="font-serif text-[20px] sm:text-[24px] text-[#5b4a3b] leading-[1.3] max-w-2xl mx-auto">
              The page or document you requested has been relocated, unfiled, or does not exist in our online firm records.
            </p>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <Link href="/">
              <Button variant="primary" size="lg" className="bg-[#2a1c12] text-[#fffaf2]">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Return to LaSalle Floor
              </Button>
            </Link>
            <Link href="/contact">
              <Button variant="outline" size="lg">
                Direct Intake Inquiry
              </Button>
            </Link>
          </div>

          {/* Directory Shortcuts Grid */}
          <div className="pt-12 border-t border-[#e2d5c1] text-left">
            <div className="text-xs font-mono uppercase tracking-[0.14em] text-[#85725f] mb-6 text-center">
              Available Case Files & Directories
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {quickLinks.map((link) => {
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="border border-[#e2d5c1] bg-[#fffaf2] p-6 hover:border-[#cfbe9e] hover:shadow-[0_8px_30px_rgba(42,28,18,0.06)] transition-all group flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <Icon className="h-5 w-5 text-[#9a6a35]" />
                        <span className="text-xs font-mono text-[#85725f] group-hover:text-[#2a1c12] transition-colors">
                          Filed →
                        </span>
                      </div>
                      <h3 className="font-serif text-lg font-medium text-[#2a1c12] group-hover:text-[#9a6a35] transition-colors">
                        {link.title}
                      </h3>
                      <p className="mt-1.5 text-xs text-[#5b4a3b] leading-relaxed">
                        {link.desc}
                      </p>
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Contact Details Footer Note */}
          <div className="pt-6 text-xs text-[#85725f] font-mono">
            Ellery Kowal LLP · 224 S. LaSalle Street, 31st Floor, Chicago, IL 60604 · (312) 555-0147
          </div>
        </div>
      </Container>
    </div>
  );
}

