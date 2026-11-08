import Link from "next/link";
import { Container } from "./container";
import { practices } from "@/data/practices";

export function Footer() {
  return (
    <footer className="border-t border-[#3f2c1f] bg-[#24180f] text-[#f3ece1]">
      <Container size="xl" className="py-16 lg:py-24">
        <div className="grid grid-cols-1 gap-12 md:grid-cols-2 lg:grid-cols-5">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <Link href="/" className="inline-block">
              <span className="font-serif text-2xl lg:text-3xl font-normal text-[#f3ece1] tracking-tight">
                NyayaSetu Bharat
              </span>
            </Link>
            <p className="max-w-sm text-sm text-[#b8a695] leading-relaxed">
              AI-Powered Legal Advisor and Advocate Matching Platform for India. Helping citizens understand legal problems in simple language, assess their legal situation, discover verified advocates, and manage court cases across 6 Indian languages.
            </p>
            <div className="pt-2 text-xs text-[#85725f] space-y-1 font-sans">
              <div>New Delhi · Mumbai · Bengaluru · Kolkata · Chennai · Hyderabad</div>
              <div>Toll-Free Legal Helpline: 1800-NYAYA-SETU (1800-692-9273)</div>
              <div>Direct: support@nyayasetu.in · advocates@nyayasetu.in</div>
            </div>
          </div>

          {/* Legal Topics & Practice Areas */}
          <div>
            <h4 className="text-xs uppercase tracking-[0.14em] font-medium text-[#d1a46a]">
              Legal Areas
            </h4>
            <ul className="mt-4 space-y-2.5 text-sm">
              {practices.map((practice) => (
                <li key={practice.id}>
                  <Link
                    href={`/practices#${practice.slug}`}
                    className="text-[#b8a695] hover:text-[#f3ece1] transition-colors"
                  >
                    {practice.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Platform Navigation */}
          <div>
            <h4 className="text-xs uppercase tracking-[0.14em] font-medium text-[#d1a46a]">
              Platform
            </h4>
            <ul className="mt-4 space-y-2.5 text-sm">
              <li>
                <Link href="/firm" className="text-[#b8a695] hover:text-[#f3ece1] transition-colors">
                  About NyayaSetu
                </Link>
              </li>
              <li>
                <Link href="/people" className="text-[#b8a695] hover:text-[#f3ece1] transition-colors">
                  Find Advocates
                </Link>
              </li>
              <li>
                <Link href="/matters" className="text-[#b8a695] hover:text-[#f3ece1] transition-colors">
                  Precedents & Verdicts
                </Link>
              </li>
              <li>
                <Link href="/insights" className="text-[#b8a695] hover:text-[#f3ece1] transition-colors">
                  Legal Guides (Kanoon Gyaan)
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-[#b8a695] hover:text-[#f3ece1] transition-colors">
                  For Advocates
                </Link>
              </li>
            </ul>
          </div>

          {/* AI Intake & Help CTA */}
          <div>
            <h4 className="text-xs uppercase tracking-[0.14em] font-medium text-[#d1a46a]">
              Get Legal Help
            </h4>
            <p className="mt-4 text-xs text-[#b8a695] leading-relaxed">
              Instant preliminary legal evaluation under Indian statutory codes with Bar Council-verified advocate matching in your state.
            </p>
            <div className="pt-4">
              <Link
                href="/#conflict-check"
                className="inline-block border border-[#d1a46a]/60 bg-[#2f2116] px-4 py-2.5 text-xs uppercase tracking-wider text-[#f3ece1] hover:bg-[#9a6a35] hover:border-[#9a6a35] transition-colors"
              >
                Get Legal Help
              </Link>
            </div>
          </div>
        </div>

        {/* Bar Council of India Regulatory Notice & Copyright */}
        <div className="mt-16 border-t border-[#3f2c1f] pt-8 flex flex-col md:flex-row items-start md:items-center justify-between text-xs text-[#85725f] gap-4">
          <div className="space-y-1">
            <div>© 2026 NyayaSetu Technologies (India) Pvt. Ltd. All rights reserved.</div>
            <div className="text-[11px] text-[#85725f]/80 max-w-2xl">
              Bar Council of India Disclaimer: In accordance with Rule 36 of the Bar Council of India Rules, advocates do not advertise or solicit work through this website. NyayaSetu is an informational technology platform. AI evaluations are for preliminary legal education and do not constitute formal legal counsel or replace a licensed advocate under the Advocates Act, 1961.
            </div>
          </div>
          <div className="flex items-center space-x-6 text-xs text-[#b8a695]">
            <Link href="/privacy" className="hover:text-[#f3ece1] transition-colors">
              Privacy Policy
            </Link>
            <Link href="/disclaimer" className="hover:text-[#f3ece1] transition-colors">
              Terms & BCI Notice
            </Link>
          </div>
        </div>
      </Container>
    </footer>
  );
}
