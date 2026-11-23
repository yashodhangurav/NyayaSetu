"use client";

import * as React from "react";
import Link from "next/link";
import {
  ArrowLeft,
  BadgeCheck,
  BookOpen,
  Briefcase,
  ExternalLink,
  Info,
  Languages,
  MapPin,
  ShieldCheck,
  Star,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { formatDate, formatInr } from "@/lib/dashboard-utils";
import { spokenLanguageLabels } from "@/data/dashboard-mock-data";
import type { AdvocateMatch, Citation } from "@/types/dashboard";
import { Avatar, Badge, Button, Dot, Modal } from "@/components/dashboard/ui";
import { Logo } from "@/components/ui/logo";

/* -------------------------------------------------------------------------- */
/* Brand                                                                      */
/* -------------------------------------------------------------------------- */

export function BrandLogo({
  compact = false,
  className,
  onClick,
}: {
  compact?: boolean;
  className?: string;
  onClick?: () => void;
}) {
  return (
    <div className={cn("inline-flex items-center", className)} onClick={onClick}>
      <Logo size={compact ? "sm" : "md"} href="/dashboard" showSubtitle={!compact} />
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Stat card (Homepage Editorial Metric Style)                                 */
/* -------------------------------------------------------------------------- */

export function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  tone = "brand",
  onClick,
}: {
  icon: LucideIcon;
  label: string;
  value: string | number;
  hint?: string;
  tone?: "brand" | "mint" | "neutral" | "danger";
  onClick?: () => void;
}) {
  const Comp = onClick ? "button" : "div";
  return (
    <Comp
      onClick={onClick}
      className={cn(
        "rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 text-left transition-all duration-200 hover:border-[#cfbe9e] shadow-[0_1px_2px_rgba(42,28,18,0.04)]",
        onClick && "cursor-pointer hover:shadow-[0_4px_20px_rgba(42,28,18,0.06)]"
      )}
    >
      <div className="flex items-center justify-between gap-2 mb-3">
        <span className="text-[11px] font-sans uppercase tracking-[0.14em] font-medium text-[#85725f]">
          {label}
        </span>
        <span className="grid size-7 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
          <Icon className="size-3.5" aria-hidden="true" />
        </span>
      </div>

      <div className={cn(
        "border-l-2 pl-3 py-0.5",
        tone === "mint" && "border-[#2a6b3b]",
        tone === "danger" && "border-[#9a3424]",
        tone === "neutral" && "border-[#85725f]",
        (!tone || tone === "brand") && "border-[#9a6a35]"
      )}>
        <p className="font-serif text-[28px] sm:text-[32px] font-normal leading-none tracking-tight text-[#2a1c12]">
          {value}
        </p>
      </div>

      {hint && (
        <p className="mt-3 pt-2.5 border-t border-[#e2d5c1]/60 truncate text-xs text-[#5b4a3b] leading-relaxed">
          {hint}
        </p>
      )}
    </Comp>
  );
}

/* -------------------------------------------------------------------------- */
/* Page header                                                                */
/* -------------------------------------------------------------------------- */

export function PageHeader({
  title,
  subtitle,
  backTo,
  actions,
  eyebrow,
  className,
}: {
  title: string;
  subtitle?: string;
  backTo?: string;
  actions?: React.ReactNode;
  eyebrow?: string;
  className?: string;
}) {
  return (
    <div className={cn("mb-6 pb-6 border-b border-[#e2d5c1] flex flex-col gap-4 sm:mb-8 sm:flex-row sm:items-end sm:justify-between", className)}>
      <div className="min-w-0 space-y-1.5 max-w-3xl">
        {backTo && (
          <Link
            href={backTo}
            className="mb-2 inline-flex items-center gap-1.5 text-xs font-sans uppercase tracking-[0.12em] font-medium text-[#5b4a3b] transition hover:text-[#2a1c12]"
          >
            <ArrowLeft className="size-3.5" aria-hidden="true" />
            Back
          </Link>
        )}
        {eyebrow && (
          <div>
            <span className="inline-flex items-center px-2 py-0.5 text-[10.5px] font-sans uppercase tracking-[0.14em] font-medium border border-[#e2d5c1] bg-[#ebe1d1]/60 text-[#85725f] rounded-[2px]">
              {eyebrow}
            </span>
          </div>
        )}
        <h1 className="font-serif text-[28px] sm:text-[36px] font-normal leading-[1.08] tracking-[-0.03em] text-[#2a1c12]">
          {title}
        </h1>
        {subtitle && (
          <p className="text-xs sm:text-[14px] leading-relaxed text-[#5b4a3b] max-w-2xl">
            {subtitle}
          </p>
        )}
      </div>
      {actions && <div className="flex shrink-0 flex-wrap items-center gap-2.5">{actions}</div>}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Disclaimer + error                                                         */
/* -------------------------------------------------------------------------- */

export function Disclaimer({
  className,
  variant = "inline",
  text = "Legal information only. Not legal advice.",
  suppressHydrationWarning,
}: {
  className?: string;
  variant?: "inline" | "banner";
  text?: string;
  suppressHydrationWarning?: boolean;
}) {
  if (variant === "banner") {
    return (
      <div className={cn("flex items-start gap-2.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-4 py-3 text-xs leading-relaxed text-[#5b4a3b]", className)}>
        <ShieldCheck className="mt-0.5 size-4 shrink-0 text-[#9a6a35]" aria-hidden="true" />
        <p suppressHydrationWarning={suppressHydrationWarning} className="text-xs leading-5 text-[#5b4a3b]">{text}</p>
      </div>
    );
  }
  return (
    <p suppressHydrationWarning={suppressHydrationWarning} className={cn("flex items-start gap-1.5 text-xs leading-5 text-[#85725f]", className)}>
      <Info className="mt-0.5 size-3.5 shrink-0 text-[#9a6a35]" aria-hidden="true" />
      <span suppressHydrationWarning={suppressHydrationWarning}>{text}</span>
    </p>
  );
}

export function ServiceError({
  title = "Could not load this screen",
  message = "The service did not respond. Check your connection and try again.",
  onRetry,
  className,
}: {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}) {
  return (
    <div
      role="alert"
      className={cn("rounded-[2px] border border-[#c0392b]/30 bg-[#fdf2f0] px-4 py-4 sm:px-5", className)}
    >
      <div className="flex items-start gap-3">
        <Info className="mt-0.5 size-5 shrink-0 text-[#c0392b]" aria-hidden="true" />
        <div className="min-w-0 flex-1">
          <p className="text-xs uppercase tracking-[0.08em] font-semibold text-[#c0392b]">{title}</p>
          <p className="mt-1 text-xs sm:text-[13px] leading-5 text-[#78261f]">{message}</p>
          {onRetry && (
            <Button size="sm" variant="secondary" className="mt-3" onClick={onRetry}>
              Try again
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Advocate card                                                              */
/* -------------------------------------------------------------------------- */

export function AdvocateCard({
  match,
  rank,
  onBook,
}: {
  match: AdvocateMatch;
  rank?: number;
  onBook?: () => void;
}) {
  const { advocate: a, score, reason } = match;
  return (
    <article className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] flex h-full flex-col p-5 sm:p-6 transition-all duration-200 hover:border-[#cfbe9e] shadow-[0_1px_2px_rgba(42,28,18,0.04)] hover:shadow-[0_4px_24px_rgba(42,28,18,0.06)]">
      <div className="flex items-start justify-between gap-3 pb-4 border-b border-[#e2d5c1]/60">
        <div className="flex min-w-0 items-start gap-3.5">
          <Avatar initials={a.initials} size="lg" tone={rank === 1 ? "mint" : "brand"} />
          <div className="min-w-0 space-y-0.5">
            <h3 className="font-serif text-[18px] sm:text-[20px] font-normal leading-snug text-[#2a1c12]">
              Adv. {a.name}
            </h3>
            <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
              <span className="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-sans uppercase tracking-[0.1em] font-medium border border-[#e2d5c1] bg-[#dceada]/60 text-[#2e7d32] rounded-[2px]">
                <BadgeCheck className="size-3" aria-hidden="true" /> Verified Roll
              </span>
              {rank === 1 && <Badge tone="brand">Recommended</Badge>}
            </div>
          </div>
        </div>
        <div className="shrink-0 text-right border-l border-[#e2d5c1] pl-3">
          <p className="font-serif text-[22px] leading-none font-normal text-[#2a1c12]">{Math.round(score.total * 100)}%</p>
          <p className="mt-1 text-[9.5px] font-sans uppercase tracking-[0.12em] font-medium text-[#85725f]">Match</p>
        </div>
      </div>

      <div className="py-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-[#5b4a3b]">
        <span className="inline-flex items-center gap-1">
          <Briefcase className="size-3.5 text-[#9a6a35]" aria-hidden="true" /> {a.experienceYears} Years Exp
        </span>
        <span className="inline-flex items-center gap-1">
          <MapPin className="size-3.5 text-[#9a6a35]" aria-hidden="true" /> {a.distanceKm} km
        </span>
        <span className="inline-flex items-center gap-1">
          <Star className="size-3.5 fill-[#d1a46a] text-[#d1a46a]" aria-hidden="true" /> {a.rating} ({a.reviewCount})
        </span>
      </div>

      <div className="py-1 flex flex-wrap gap-1.5">
        {a.practiceAreas.slice(0, 3).map((area) => (
          <Badge key={area} tone="neutral">
            {area}
          </Badge>
        ))}
      </div>

      <p className="mt-2.5 flex items-center gap-1.5 text-xs text-[#85725f]">
        <Languages className="size-3.5 shrink-0 text-[#9a6a35]" aria-hidden="true" />
        {a.languages.map((l) => spokenLanguageLabels[l]).join(", ")}
      </p>

      <div className="my-3.5 flex-1 rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 p-3">
        <p className="line-clamp-3 text-xs leading-relaxed text-[#5b4a3b]">
          <span className="font-semibold text-[#2a1c12]">Grounds for Match: </span>
          {reason}
        </p>
      </div>

      <div className="pt-3 border-t border-[#e2d5c1]/60 flex items-end justify-between gap-2">
        <div>
          <p className="font-mono text-sm font-semibold text-[#2a1c12]">
            {formatInr(a.feeMin)}–{formatInr(a.feeMax)}
          </p>
          <p className="mt-0.5 flex items-center gap-1 text-[11px] text-[#85725f]">
            <Dot /> {a.responseRate}% response rate
          </p>
        </div>
        <p className="shrink-0 text-right text-[11px] text-[#85725f]">
          Earliest Slot
          <span className="block text-xs font-semibold text-[#2a1c12] font-mono">
            {a.nextAvailable ? formatDate(a.nextAvailable, { day: "numeric", month: "short" }) : "Available"}
          </span>
        </p>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2">
        <Link
          href={`/dashboard/advocates/${a.id}`}
          className="inline-flex h-10 items-center justify-center rounded-[2px] border border-[#2a1c12] bg-transparent px-3 text-xs uppercase tracking-[0.08em] font-semibold text-[#2a1c12] transition hover:bg-[#2a1c12] hover:text-[#fffaf2]"
        >
          View Record
        </Link>
        <Button size="sm" variant="primary" onClick={onBook} fullWidth>
          Request Consult
        </Button>
      </div>
    </article>
  );
}

/* -------------------------------------------------------------------------- */
/* Citation chip                                                              */
/* -------------------------------------------------------------------------- */

export function CitationChip({ citation }: { citation: Citation }) {
  const [open, setOpen] = React.useState(false);
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        title={`${citation.act} — ${citation.section}`}
        className="inline-flex cursor-pointer items-center gap-1.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-2.5 py-1 text-xs font-mono text-[#2a1c12] transition hover:border-[#9a6a35] hover:bg-[#ebe1d1]/40"
      >
        <BookOpen className="size-3 text-[#9a6a35]" aria-hidden="true" />
        {citation.act.split(",")[0]} · {citation.section}
      </button>

      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title={citation.act}
        description={citation.section}
        footer={
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" onClick={() => setOpen(false)}>
              Close
            </Button>
            {citation.url && (
              <Button variant="secondary" size="sm" onClick={() => window.open(citation.url, "_blank", "noopener")}>
                Open official source
                <ExternalLink className="size-3.5 ml-1" />
              </Button>
            )}
          </div>
        }
      >
        <div className="space-y-3">
          <p className="text-sm font-semibold text-[#2a1c12]">{citation.title}</p>
          <blockquote className="rounded-[2px] border-l-2 border-[#9a6a35] bg-[#ebe1d1]/40 px-4 py-3 text-xs leading-relaxed text-[#5b4a3b]">
            {citation.snippet}
          </blockquote>
          <p className="text-xs text-[#85725f]">
            Statutory sources are verified against official gazette Bare Acts.
          </p>
        </div>
      </Modal>
    </>
  );
}
