"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  CheckCircle2,
  Download,
  FileText,
  Info,
  MapPin,
  Receipt,
  ShieldCheck,
  Sparkles,
  Stamp,
} from "lucide-react";
import { templates } from "@/data/dashboard-mock-data";
import { loadCaseProfile } from "@/services/dashboard/intake";
import { printHtml } from "@/lib/dashboard-print";
import { Badge, Button, Field, Input, Textarea } from "@/components/dashboard/ui";
import { Disclaimer, PageHeader } from "@/components/dashboard/shared";
import { cn } from "@/lib/utils";
import { dh } from "@/lib/dashboard-utils";
import { DASHBOARD_TODAY_PLACEHOLDER } from "@/lib/dashboard-time";

const prefill: Record<string, string> = {
  recipient: "Mr. S. Rao, 402 Lake View Apartments, HSR Layout, Bengaluru 560102",
  sender: "Rahul Kumar, 12th Main, Indiranagar, Bengaluru 560038",
  facts:
    "I vacated the premises on 15 September 2026 upon lease expiry and returned all keys. The tenancy premises were surrendered in tenable condition subject to ordinary wear and tear. Security deposit of ₹60,000 remains unpaid despite written reminders.",
  demand: "refund the security deposit of ₹60,000 along with statutory interest at 18% p.a.",
  deadline: "15 days from receipt of this notice",
  authority: "The Public Information Officer, BBMP, Bengaluru",
  applicant: "Rahul Kumar, 12th Main, Indiranagar, Bengaluru 560038",
  information: "Certified copies of all sanctioned road repair tenders and completion certificates for 12th Main, Indiranagar, executed between January and September 2026.",
  period: "1 January 2026 to 30 September 2026",
  complainant: "Rahul Kumar, 12th Main, Indiranagar, Bengaluru 560038",
  opposite: "M/s TechnoMart Retail Pvt. Ltd., Koramangala, Bengaluru",
  product: "a laptop computer (Tax Invoice INV-8842) amounting to ₹72,999",
  defect: "the keyboard and logic board failed during the statutory warranty period, and the retailer denied replacement or refund.",
  relief: "a full refund of ₹72,999 along with damages for mental harassment and litigation costs.",
  advocate: "M/s Rao & Associates, Advocates, Bengaluru",
  points:
    "The premises were inspected on the date of vacating in the presence of the building manager. No structural damage was recorded. Date-stamped inspection photographs are enclosed.",
  request: "withdraw the impugned notice and remit the security deposit forthwith.",
};

function BeforeYouSend({ className }: { className?: string }) {
  return (
    <div className={cn('rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 p-5', className)}>
      <p className="flex items-center gap-2 font-serif text-[14px] font-normal text-[#2a1c12]">
        <Info className="size-4 text-[#9a6a35]" aria-hidden /> Procedural Notice Requirements
      </p>
      <ul className="mt-3 space-y-2">
        {[
          'Verify counterparty’s full legal name and registered jurisdictional address.',
          'Dispatch via Registered Post with Acknowledgment Due (RPAD) or Speed Post and preserve tracking receipt.',
          'Maintain an identical attested duplicate copy along with all annexures.',
        ].map((x) => (
          <li key={x} className="flex gap-2 text-[12px] leading-relaxed text-[#5b4a3b]">
            <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-[#9a6a35]" /> {x}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function SelfHelpPage() {
  const router = useRouter();
  const profile = loadCaseProfile();
  const [templateId, setTemplateId] = useState(templates[0].id);
  const template = templates.find((t) => t.id === templateId)!;
  const [values, setValues] = useState<Record<string, string>>(prefill);
  const [reviewed, setReviewed] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [draftDate] = useState(() =>
    DASHBOARD_TODAY_PLACEHOLDER.toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }),
  );

  const rendered = useMemo(
    () =>
      template.body.replace(/\{\{(\w+)\}\}/g, (_, key: string) =>
        key === 'date' ? draftDate : values[key] || `[${key}]`,
      ),
    [template, values, draftDate],
  );

  const download = () => {
    printHtml(template.name, rendered.replaceAll('&', '&amp;').replaceAll('<', '&lt;'));
    setGenerated(true);
  };

  return (
    <div className="animate-fade space-y-6">
      <PageHeader
        title="Self-Help Guides"
        subtitle="Statutory notice templates. Have an advocate review before sending."
        actions={<Badge tone="mint"><ShieldCheck className="size-3" /> Reviewed templates</Badge>}
      />

      <div className="grid gap-6 lg:grid-cols-[300px_1fr]">
        {/* List */}
        <aside className="min-w-0 space-y-4">
          <div className="grid gap-2.5 sm:grid-cols-3 lg:grid-cols-1">
            {templates.map((t) => (
              <button
                key={t.id}
                type="button"
                onClick={() => setTemplateId(t.id)}
                className={cn(
                  'flex flex-col rounded-[2px] border p-4 text-left transition-colors',
                  templateId === t.id
                    ? 'border-[#2a1c12] bg-[#f4efe6] ring-1 ring-[#2a1c12]'
                    : 'border-[#e2d5c1] bg-[#fffaf2] hover:border-[#9a6a35]',
                )}
              >
                <span className="flex items-center gap-2">
                  <FileText className={cn('size-4', templateId === t.id ? 'text-[#9a6a35]' : 'text-[#85725f]')} aria-hidden />
                  <span className="font-serif text-[14px] font-normal text-[#2a1c12]">{t.name}</span>
                </span>
                <span className="mt-1 line-clamp-2 text-[11.5px] leading-relaxed text-[#5b4a3b]">{t.description}</span>
              </button>
            ))}
          </div>

          <BeforeYouSend className="hidden lg:block" />
        </aside>

        {/* Editor + preview */}
        <div className="min-w-0 space-y-6">
          <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] overflow-hidden">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#e2d5c1] bg-[#ebe1d1]/20 px-5 py-4">
              <div className="min-w-0 flex-1">
                <h2 className="font-serif text-[18px] font-normal text-[#2a1c12]">{template.name}</h2>
                <p className="font-mono text-[11px] text-[#85725f]">Prefilled from your case · {profile ? profile.title : "Active case"}</p>
              </div>
              <Badge tone="neutral">Template</Badge>
            </div>

            <div className="grid divide-y divide-[#e2d5c1] lg:grid-cols-2 lg:divide-x lg:divide-y-0">
              {/* Form */}
              <div className="space-y-4 p-5 sm:p-6">
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Fill in details</p>
                {template.fields.map((f) => (
                  <Field key={f.key} label={f.label} htmlFor={`f-${f.key}`}>
                    {f.multiline ? (
                      <Textarea
                        id={`f-${f.key}`}
                        rows={4}
                        value={values[f.key] ?? ''}
                        onChange={(e) => setValues((v) => ({ ...v, [f.key]: e.target.value }))}
                      />
                    ) : (
                      <Input
                        id={`f-${f.key}`}
                        value={values[f.key] ?? ''}
                        onChange={(e) => setValues((v) => ({ ...v, [f.key]: e.target.value }))}
                      />
                    )}
                  </Field>
                ))}
              </div>

              {/* Preview */}
              <div className="bg-[#f4efe6]/50 p-5 sm:p-6">
                <div className="mb-3 flex items-center justify-between">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Preview</p>
                  <button type="button" onClick={download} className="inline-flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-[#9a6a35] hover:underline">
                    <Download className="size-3.5" aria-hidden /> Export PDF
                  </button>
                </div>
                <div className="max-h-[460px] overflow-y-auto rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 shadow-xs">
                  <pre className="font-serif text-[12.5px] leading-relaxed whitespace-pre-wrap text-[#2a1c12]">{rendered}</pre>
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-3 border-t border-[#e2d5c1] px-5 py-4 sm:flex-row sm:items-center sm:justify-between bg-[#ebe1d1]/10">
              <p className="font-mono text-[10.5px] text-[#85725f]">
                Statutory Draft · Legal notice issued in personal capacity or via advocate.
              </p>
              <div className="flex gap-2.5">
                <Button variant="secondary" size="sm" onClick={() => setReviewed(true)}>
                  <Sparkles className="size-3.5" aria-hidden /> Request review
                </Button>
                <Button size="sm" onClick={download}>
                  <Download className="size-3.5" aria-hidden /> Download PDF
                </Button>
              </div>
            </div>
          </div>

          {reviewed && (
            <div className="rounded-[2px] border border-[#2a6b3b]/30 bg-[#2a6b3b]/10 px-5 py-3.5 text-[13px] font-medium text-[#2a6b3b]">
              Review requested from Adv. Ananya Rao. You&apos;ll be notified when done.
              <button type="button" onClick={() => router.push(dh('/messages'))} className="ml-2 inline-flex items-center gap-1 underline">
                Open messages <ArrowRight className="size-3.5" aria-hidden />
              </button>
            </div>
          )}
          {generated && (
            <p className="flex items-center gap-2 font-mono text-[11px] text-[#2a6b3b]">
              <CheckCircle2 className="size-4" aria-hidden /> Downloaded. Save a copy to your vault.
            </p>
          )}

          <BeforeYouSend className="lg:hidden" />

          {/* Checklist */}
          <div className="grid gap-4 sm:grid-cols-3">
            {[
              { icon: MapPin, title: 'Prescribed Forum', body: template.forum },
              { icon: Receipt, title: 'Statutory Fee / Stamp', body: template.fee },
              { icon: Stamp, title: 'Mandatory Annexures', body: template.documents.join(' · ') },
            ].map((item) => (
              <div key={item.title} className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5">
                <span className="grid size-9 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] text-[#9a6a35]">
                  <item.icon className="size-4.5" aria-hidden />
                </span>
                <p className="mt-3 font-mono text-[10px] uppercase tracking-[0.14em] text-[#85725f]">{item.title}</p>
                <p className="mt-1 text-[12.5px] leading-relaxed text-[#5b4a3b]">{item.body}</p>
              </div>
            ))}
          </div>

          <Disclaimer variant="banner" text="Templates are for reference only. Court filings must be verified by an advocate." />
        </div>
      </div>
    </div>
  );
}
