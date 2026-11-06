import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { BackToTop } from "@/components/layout/back-to-top";

export const metadata: Metadata = {
  title: {
    default: "NyayaSetu (न्यायसेतु) · AI Legal Advisor & Advocate Matching Platform · India",
    template: "%s · NyayaSetu India",
  },
  description:
    "AI-Powered Legal Advisor and Advocate Matching Platform for India. Helping citizens understand legal problems in simple language, assess their legal situation, discover verified advocates, and manage court cases across 6 Indian languages.",
  authors: [{ name: "NyayaSetu Technologies (India) Pvt. Ltd." }],
  creator: "NyayaSetu India",
  publisher: "NyayaSetu India",
  formatDetection: {
    email: true,
    address: true,
    telephone: true,
  },
  openGraph: {
    title: "NyayaSetu · AI Legal Advisor & Advocate Matching Platform · India",
    description:
      "Understand your legal situation, explore your options, and connect with verified advocates across District Courts, High Courts, and the Supreme Court of India.",
    url: "https://nyayasetu.in",
    siteName: "NyayaSetu India",
    locale: "en_IN",
    type: "website",
    images: [
      {
        url: "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=1200",
        width: 1200,
        height: 630,
        alt: "NyayaSetu · AI-Powered Legal Advisor & Advocate Matching Platform for India",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "NyayaSetu · AI Legal Advisor & Advocate Matching Platform · India",
    description: "Legal Help Should Be Clear. Justice Should Be Accessible. Connecting citizens with verified counsel across India.",
    images: ["https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=1200"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased scroll-smooth">
      <head>
        <link rel="preconnect" href="https://api.fontshare.com" />
        <link
          rel="stylesheet"
          href="https://api.fontshare.com/v2/css?f[]=gambetta@400,500,600,700,401,501,601,701&f[]=general-sans@400,500,600,700&display=swap"
        />
      </head>
      <body className="min-h-full flex flex-col bg-[#f3ece1] text-[#2a1c12] font-sans antialiased selection:bg-[#2a1c12] selection:text-[#fffaf2]" suppressHydrationWarning>
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
        <BackToTop />
      </body>
    </html>
  );
}
