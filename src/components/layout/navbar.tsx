"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { navigationLinks } from "@/data/navigation";
import { ChevronDown, ArrowRight, Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { NavChild } from "@/types";
import { QuickConsultationModal } from "@/components/ui/quick-consultation-modal";

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const [isConsultModalOpen, setIsConsultModalOpen] = useState(false);
  const pathname = usePathname();
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpenDropdown(null);
        setIsOpen(false);
      }
    };

    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setOpenDropdown(null);
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <>
      <header className="sticky top-0 z-40 w-full bg-[#f4efe6]/95 backdrop-blur-md transition-all">
        <div className="mx-auto flex max-w-[1424px] items-center justify-between px-6 lg:px-12 h-20">
          {/* Brand Logo with Justice Scale Monogram */}
          <Link href="/" className="flex items-center space-x-3 group">
            {/* Monogram SVG */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="-242 -690 975 700"
              className="h-6 w-auto shrink-0 transition-transform group-hover:scale-105"
            >
              <path
                fill="#9a6a35"
                d="M179.56-333.16v-39.8H41.6q-36.04 0-55.94-4.28t-30.32-14.56-16.02-28.78-12.6-46.5h-29.04v228.04h29.04q7-27.44 12.6-45.72t16.02-29.06 30.32-15.06 55.94-4.28ZM-128.6-38.48l-73.04-155.28h-30.16L-212.36 0h515.24v-28.48q-33.2-4.44-49.54-9.5t-22.9-16.74q-7.56-12.56-9.06-36.06t-1.5-64.58v-369.28q0-44.44 1.78-68.22t11.02-36.34q7.12-10.44 23.18-14.94t47.02-6.82V-680h-499.12l-10 176.92h30.16l63.04-138.44h235v603.04Z"
              />
              <path
                fill="#2a1c12"
                d="m204-275-52-2.4 314.72-292.68q20.44-19 30.94-28.72t10.5-21.72q0-14-14.48-21t-41.28-10V-680q31 2 59.04 3t56.68 1q27.4 0 56.8-1t75.04-3v28.48q-32.56 4-56.38 11.32t-45.98 21.76-51.52 40.36Zm79.96-107.72 76.56-56.88 204.56 299.4q27.12 36.36 45.96 57.7t34.64 31.8 33.92 15.12 43.36 7.66V.44q-40.48-2-61.84-2.66t-39.08-.66q-17.68 0-36.16.72T547.96 0Zm-63-163.2v411.84q0 30.36 1.5 49.32t6.94 29.28q7.56 13 24.8 17.78t50.68 9.22V0q-32.04-2-52.12-2.5t-37.84-1-44.4-.5q-24.88 0-42.26.5t-36.96 1T39.12 0v-28.48q32.12-4.44 49.8-9t25.24-17.24q6.32-10.32 7.82-29.28t1.5-51.08v-409.84q0-32.12-1.72-51.08t-7.6-29.28q-7.56-12.68-25.24-17.46t-49.8-8.78V-680q32.6 1 52.18 2t36.96 1.5 42.26.5q26.64 0 44.4-.5t37.84-1.5 52.12-2v28.48q-33.44 4-50.46 8.5t-25.02 18.5q-5.88 10.32-7.16 29t-1.28 49.6"
              />
            </svg>

            {/* Typography */}
            <div className="flex items-baseline space-x-1.5">
              <span className="font-serif text-[21px] tracking-tight text-[#2a1c12] font-normal">
                NyayaSetu
              </span>
              <span className="text-[10px] uppercase tracking-[0.2em] font-sans text-[#85725f] font-semibold">
                BHARAT
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center space-x-7" aria-label="Main navigation">
            {/* Home with dot */}
            <Link
              href="/"
              className={cn(
                "text-[14px] font-medium transition-colors hover:text-[#2a1c12] flex items-center space-x-1.5",
                pathname === "/" ? "text-[#2a1c12] font-semibold" : "text-[#5b4a3b]"
              )}
            >
              <span className="text-[16px] text-[#2a1c12]">•</span>
              <span>Home</span>
            </Link>

            {navigationLinks.map((item) => {
              const hasChildren = item.children && item.children.length > 0;
              const dropdownOpen = openDropdown === item.label;

              if (hasChildren) {
                return (
                  <div
                    key={item.label}
                    ref={dropdownRef}
                    className="relative"
                    onMouseEnter={() => setOpenDropdown(item.label)}
                    onMouseLeave={() => setOpenDropdown(null)}
                  >
                    <button
                      type="button"
                      onClick={() => setOpenDropdown(dropdownOpen ? null : item.label)}
                      aria-expanded={dropdownOpen}
                      aria-haspopup="true"
                      className="flex items-center space-x-1 text-[14px] font-medium text-[#5b4a3b] hover:text-[#2a1c12] transition-colors py-2 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#9a6a35]"
                    >
                      <span>{item.label}</span>
                      <ChevronDown
                        className={cn(
                          "h-3.5 w-3.5 text-[#85725f] transition-transform duration-200",
                          dropdownOpen && "rotate-180"
                        )}
                      />
                    </button>

                    {dropdownOpen && (
                      <div className="absolute top-full left-0 z-50 mt-1 w-80 border border-[#e2d5c1] bg-[#fffaf2] p-2 shadow-lg animate-in fade-in slide-in-from-top-1 duration-150">
                        {item.children?.map((child: NavChild) => (
                          <Link
                            key={child.href}
                            href={child.href}
                            onClick={() => setOpenDropdown(null)}
                            className="block p-2.5 transition-colors hover:bg-[#ebe1d1]/50 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35]"
                          >
                            <div className="text-sm font-medium text-[#2a1c12]">
                              {child.label}
                            </div>
                            {child.description && (
                              <div className="text-xs text-[#85725f] mt-0.5 leading-snug">
                                {child.description}
                              </div>
                            )}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                );
              }

              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "text-[14px] font-medium transition-colors hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#9a6a35]",
                    isActive ? "text-[#2a1c12] font-semibold" : "text-[#5b4a3b]"
                  )}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          {/* Action CTA Compound Button */}
          <div className="hidden sm:flex items-center space-x-3">
            <Link
              href="/contact"
              className="group inline-flex items-center bg-[#2a1c12] text-[#fffaf2] hover:bg-[#9a6a35] transition-colors rounded-[2px] overflow-hidden shadow-xs cursor-pointer"
            >
              <span className="px-4 py-2.5 text-[14px] font-semibold tracking-tight">
                Get Legal Help
              </span>
              <span className="flex items-center justify-center w-9 h-full py-2.5 border-l border-white/20 bg-[#fffaf2]/10 group-hover:bg-[#fffaf2]/20 transition-colors">
                <ArrowRight className="h-3.5 w-3.5" />
              </span>
            </Link>
          </div>

          {/* Mobile / Tablet Menu Button */}
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="lg:hidden flex items-center space-x-1.5 p-2 text-[#2a1c12] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#9a6a35] cursor-pointer"
            aria-label="Toggle navigation menu"
            aria-expanded={isOpen}
          >
            <span className="text-xs uppercase tracking-wider font-semibold font-mono">Menu</span>
            {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>

        {/* Mobile Navigation Dropdown Drawer */}
        {isOpen && (
          <div className="lg:hidden border-t border-[#e2d5c1] bg-[#fffaf2] py-5 px-6 space-y-4 shadow-xl animate-in fade-in duration-200">
            <Link
              href="/"
              onClick={() => setIsOpen(false)}
              className="block py-2 text-base font-serif text-[#2a1c12]"
            >
              • Home
            </Link>
            {navigationLinks.map((item) => (
              <div key={item.label}>
                <Link
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="block py-2 text-base font-serif text-[#2a1c12]"
                >
                  {item.label}
                </Link>
                {item.children && (
                  <div className="pl-4 space-y-2.5 border-l border-[#e2d5c1] mt-1">
                    {item.children.map((child: NavChild) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        onClick={() => setIsOpen(false)}
                        className="block text-sm text-[#5b4a3b] hover:text-[#2a1c12]"
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
            <div className="pt-4 border-t border-[#e2d5c1] space-y-2.5">
              <Link
                href="/contact"
                onClick={() => setIsOpen(false)}
                className="group flex items-center justify-between bg-[#2a1c12] text-[#fffaf2] rounded-[2px] overflow-hidden"
              >
                <span className="px-4 py-3 text-sm font-semibold">
                  Get Legal Help
                </span>
                <span className="flex items-center justify-center w-10 py-3 border-l border-white/20 bg-[#fffaf2]/10">
                  <ArrowRight className="h-4 w-4" />
                </span>
              </Link>
            </div>
          </div>
        )}
      </header>

      {/* Global Quick Consultation Modal */}
      <QuickConsultationModal
        isOpen={isConsultModalOpen}
        onClose={() => setIsConsultModalOpen(false)}
      />
    </>
  );
}
