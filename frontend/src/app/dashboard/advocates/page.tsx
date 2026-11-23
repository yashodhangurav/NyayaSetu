"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import {
  BadgeCheck,
  ChevronDown,
  Filter,
  IndianRupee,
  Languages,
  MapPin,
  Video,
} from "lucide-react";
import {
  Badge,
  Button,
  Chip,
  Field,
  Input,
  Select,
  SkeletonCard,
  Tabs,
} from "@/components/dashboard/ui";
import {
  AdvocateCard,
  Disclaimer,
  PageHeader,
  ServiceError,
} from "@/components/dashboard/shared";
import { matchAdvocates, practiceAreas, sortMatches, type MatchPreferences } from "@/services/dashboard/advocates";
import { loadCaseProfile } from "@/services/dashboard/intake";
import { cases, languageLabels } from "@/data/dashboard-mock-data";
import type { AdvocateMatch, Language } from "@/types/dashboard";
import { cn } from "@/lib/utils";
import { dh } from "@/lib/dashboard-utils";

type Sort = "recommended" | "nearest" | "fee" | "experience";

export default function AdvocatesPage() {
  const router = useRouter();
  const profile = typeof window !== "undefined" ? loadCaseProfile() ?? cases[0] : cases[0];
  const [prefs, setPrefs] = useState<MatchPreferences>({
    practiceArea: profile.category,
    budgetMax: 3000,
    language: "en",
    mode: "any",
    gender: "any",
  });
  const [draft, setDraft] = useState<MatchPreferences>(prefs);
  const [matches, setMatches] = useState<AdvocateMatch[]>([]);
  const [noLocal, setNoLocal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sort, setSort] = useState<Sort>("recommended");
  const [showHow, setShowHow] = useState(false);

  const search = async (p: MatchPreferences) => {
    setLoading(true);
    setError("");
    try {
      const res = await matchAdvocates(p, p.practiceArea ?? profile.category);
      setMatches(res.matches);
      setNoLocal(res.noLocalMatch);
      setPrefs(p);
      setSort("recommended");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load advocate matches.");
    } finally {
      setLoading(false);
    }
  };

  const [initialPrefs] = useState(prefs);
  const [initialCategory] = useState(profile.category);

  useEffect(() => {
    let cancelled = false;
    void matchAdvocates(initialPrefs, initialPrefs.practiceArea ?? initialCategory)
      .then((res) => {
        if (cancelled) return;
        setMatches(res.matches);
        setNoLocal(res.noLocalMatch);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Could not load advocate matches.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [initialPrefs, initialCategory]);

  const sorted = useMemo(() => sortMatches(matches, sort), [matches, sort]);

  return (
    <div className="space-y-6 animate-fade">
      <PageHeader
        title="Find an Advocate"
        subtitle="Matched by practice area, court, language, and budget. No paid placements."
        actions={
          <Badge tone="mint">
            {matches.length} matches
          </Badge>
        }
      />

      {error && <ServiceError message={error} onRetry={() => void search(prefs)} className="mb-4" />}

      {noLocal && (
        <div className="rounded-[2px] border border-[#b54708]/30 bg-[#fff8e7] p-4 text-xs flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-2.5">
            <Video className="mt-0.5 size-4.5 shrink-0 text-[#b54708]" aria-hidden />
            <div>
              <p className="font-semibold text-[#b54708]">No direct local bench advocate matched every constraint</p>
              <p className="text-[11.5px] leading-relaxed text-[#5b4a3b]">
                These verified High Court and Appellate advocates offer hybrid/remote consultation and formal appearance.
              </p>
            </div>
          </div>
          <Button size="sm" variant="secondary" onClick={() => void search({ ...prefs, mode: "video" })}>
            Show Remote Consultation Only
          </Button>
        </div>
      )}

      {/* Filter Preferences Panel */}
      <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 sm:p-6 shadow-[0_1px_2px_rgba(42,28,18,0.04)]">
        <div className="mb-4 flex items-center justify-between pb-3 border-b border-[#e2d5c1]/60">
          <h2 className="flex items-center gap-2 font-serif text-[18px] sm:text-[20px] font-normal text-[#2a1c12]">
            <Filter className="size-4 text-[#9a6a35]" aria-hidden /> Matching Filters
          </h2>

        </div>
        <div className="grid gap-3.5 sm:grid-cols-2 lg:grid-cols-5 text-xs">
          <Field label="Practice Area" htmlFor="area">
            <Select id="area" value={draft.practiceArea} onChange={(e) => setDraft({ ...draft, practiceArea: e.target.value })}>
              {practiceAreas.map((a) => (
                <option key={a}>{a}</option>
              ))}
            </Select>
          </Field>
          <Field label="Budget Ceiling (₹)" htmlFor="budget">
            <Input
              id="budget"
              inputMode="numeric"
              value={draft.budgetMax}
              onChange={(e) => setDraft({ ...draft, budgetMax: Number(e.target.value.replace(/[^\d]/g, "")) || 0 })}
            />
          </Field>
          <Field label="Language" htmlFor="lang">
            <Select id="lang" value={draft.language} onChange={(e) => setDraft({ ...draft, language: e.target.value as Language | "any" })}>
              <option value="any">Any Language</option>
              {(Object.keys(languageLabels) as Language[]).map((l) => (
                <option key={l} value={l}>
                  {languageLabels[l]}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Consultation Format" htmlFor="mode">
            <Select id="mode" value={draft.mode} onChange={(e) => setDraft({ ...draft, mode: e.target.value as MatchPreferences["mode"] })}>
              <option value="any">Any Format</option>
              <option value="video">Video</option>
              <option value="phone">Phone</option>
              <option value="in-person">In-person</option>
            </Select>
          </Field>
          <Field label="Gender Preference" htmlFor="gender">
            <Select id="gender" value={draft.gender} onChange={(e) => setDraft({ ...draft, gender: e.target.value as MatchPreferences["gender"] })}>
              <option value="any">No Preference</option>
              <option value="female">Woman Advocate</option>
              <option value="male">Male Advocate</option>
            </Select>
          </Field>
        </div>
        <div className="mt-4 pt-3 border-t border-[#e2d5c1]/60 flex flex-wrap items-center justify-between gap-3 text-xs">
          <p className="flex items-center gap-1.5 text-[#85725f]">
            <MapPin className="size-3.5 text-[#9a6a35]" aria-hidden /> Showing counsel with active vakalat standing in {profile.probableForum}
          </p>
          <Button size="sm" variant="compound" loading={loading} onClick={() => void search(draft)}>
            Find advocates
          </Button>
        </div>
      </div>

      {/* Results Header Strip */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-baseline sm:justify-between">
        <div>
          <h2 className="font-serif text-[20px] sm:text-[22px] font-normal text-[#2a1c12]">
            {loading ? "Finding advocates…" : `${sorted.length} verified advocates`}
            <span className="ml-2 text-xs font-sans text-[#85725f]">for {prefs.practiceArea}</span>
          </h2>

        </div>
        <Tabs
          size="sm"
          value={sort}
          onChange={(v) => setSort(v as Sort)}
          options={[
            { value: "recommended", label: "Recommended" },
            { value: "nearest", label: "Proximity" },
            { value: "fee", label: "Fee" },
            { value: "experience", label: "Experience" },
          ]}
        />
      </div>

      {/* Practice Category Quick Chips */}
      <div className="flex flex-wrap gap-1.5">
        {["Tenancy", "Property", "Consumer", "Cheque bounce", "Family", "Employment"].map((area) => (
          <Chip
            key={area}
            active={prefs.practiceArea === area}
            onClick={() => {
              const next = { ...prefs, practiceArea: area };
              setDraft(next);
              void search(next);
            }}
          >
            {area}
          </Chip>
        ))}
        <Chip onClick={() => setShowHow((v) => !v)}>
          How scoring works <ChevronDown className={cn("size-3 ml-0.5 transition", showHow && "rotate-180")} />
        </Chip>
      </div>

      {showHow && (
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 p-4 text-xs animate-in-up">
          <div className="grid gap-2 sm:grid-cols-3">
            {[
              ["Practice Fit", 30],
              ["Court Proximity", 20],
              ["Bar Experience", 15],
              ["Language Compatibility", 10],
              ["Verified Client Rating", 15],
              ["Budget & Availability", 10],
            ].map(([label, pct]) => (
              <div key={String(label)} className="flex items-center justify-between rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 py-2">
                <span className="text-[#5b4a3b]">{label}</span>
                <span className="font-mono font-semibold text-[#2a1c12]">{pct}%</span>
              </div>
            ))}
          </div>
          <p className="mt-3 flex items-start gap-1.5 text-[11px] text-[#85725f]">
            <BadgeCheck className="size-3.5 text-[#2e7d32] shrink-0 mt-0.5" aria-hidden />
            Ranked by practice fit, court proximity, language, experience, and budget. No paid placements.
          </p>
        </div>
      )}

      {/* Advocates Cards Grid */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {loading
          ? [0, 1, 2].map((i) => <SkeletonCard key={i} />)
          : sorted.map((m, i) => (
            <AdvocateCard
              key={m.advocate.id}
              match={m}
              rank={i + 1}
              onBook={() => router.push(dh(`/booking/${m.advocate.id}`))}
            />
          ))}
      </div>

      {!loading && (
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-6 shadow-[0_1px_2px_rgba(42,28,18,0.04)] flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
          <div className="space-y-1">
            <p className="flex items-center gap-1.5 font-serif text-[18px] font-normal text-[#2a1c12]">
              <IndianRupee className="size-4 text-[#9a6a35]" aria-hidden /> Standardize Your Case Brief First
            </p>
            <p className="text-xs text-[#5b4a3b] leading-relaxed max-w-xl">
              Compile facts, dates, and evidence into an organized matter brief before booking consultations.
            </p>
          </div>
          <div className="flex gap-2 shrink-0">
            <Button size="sm" variant="secondary" onClick={() => router.push(dh("/brief"))}>
              Prepare Brief
            </Button>
            <Button size="sm" variant="primary" onClick={() => router.push(dh("/triage"))}>
              Review Triage
            </Button>
          </div>
        </div>
      )}

      <div className="pt-2 flex flex-wrap items-center justify-between gap-2 text-xs text-[#85725f]">
        <Disclaimer />
        <p className="flex items-center gap-1.5">
          <Languages className="size-3.5 text-[#9a6a35]" aria-hidden />
          Credentials verified against Bar Council of India rolls.
        </p>
      </div>
    </div>
  );
}
