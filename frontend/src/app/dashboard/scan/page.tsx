"use client";

import { useRef, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import {
  AlertTriangle,
  ArrowRight,
  CalendarPlus,
  Camera,
  Check,
  FileImage,
  FileText,
  Loader2,
  Pencil,
  RotateCcw,
  ScanLine,
  Upload,
} from "lucide-react";
import { explainDocument, runOcr } from "@/services/dashboard/documents";
import type { DocumentExplanation, OcrResult } from "@/types/dashboard";
import { Badge, Button, Input } from "@/components/dashboard/ui";
import { Disclaimer, PageHeader } from "@/components/dashboard/shared";
import { cn } from "@/lib/utils";
import { dh } from "@/lib/dashboard-utils";
import { useDashboardUI } from "@/lib/dashboard-ui-context";

type Stage = 'idle' | 'ocr' | 'explain' | 'done';

export default function ScanPage() {
  const router = useRouter();
  const { pushNotification } = useDashboardUI();
  const fileRef = useRef<HTMLInputElement>(null);

  const [stage, setStage] = useState<Stage>('idle');
  const [ocr, setOcr] = useState<OcrResult | null>(null);
  const [explanation, setExplanation] = useState<DocumentExplanation | null>(null);
  const [fileName, setFileName] = useState('');
  const [preview, setPreview] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [dates, setDates] = useState<Array<{ label: string; value: string }>>([]);
  const [amounts, setAmounts] = useState<Array<{ label: string; value: string }>>([]);
  const [saved, setSaved] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const process = async (fileOrName: File | string, imageUrl?: string) => {
    const displayName = fileOrName instanceof File ? fileOrName.name : fileOrName;
    setFileName(displayName);
    if (imageUrl) setPreview(imageUrl);
    setStage('ocr');
    setOcr(null);
    setExplanation(null);
    setErrorMsg(null);
    setSaved(false);

    try {
      const result = await runOcr(fileOrName);
      setOcr(result);

      if (result.status === 'failed' || !result.text || result.text.trim().length === 0) {
        setErrorMsg(result.processingError || "Optical extraction failed: The document contains no readable text or is corrupted.");
        setStage('idle');
        return;
      }

      setStage('explain');
      const explained = await explainDocument(result.text, result.documentId);
      setExplanation(explained);
      setDates(explained.dates || []);
      setAmounts(explained.amounts || []);
      setStage('done');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Document analysis failed. Please try again.";
      setErrorMsg(msg);
      setStage('idle');
    }
  };

  const onFile = (file?: File) => {
    if (!file) return;
    const url = file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined;
    void process(file, url);
  };

  const addDates = () => {
    setSaved(true);
    pushNotification({
      title: 'Dates added to your deadlines',
      body: `${dates.length} dates from ${fileName} were added. Confirm each trigger date.`,
      href: '/deadlines',
    });
  };

  const reset = () => {
    setStage('idle');
    setOcr(null);
    setExplanation(null);
    setPreview(null);
    setFileName('');
    setSaved(false);
    setEditing(false);
  };

  return (
    <div className="animate-fade space-y-6">
      <PageHeader
        title="Scan & Explain"
        subtitle="Upload or photograph a notice, agreement, or summons. We extract key dates, amounts, and what it means in plain language."

      />

      {errorMsg && (
        <div className="rounded-[2px] border border-[#9a3424]/40 bg-[#fbf2ef] p-4 flex items-start gap-3">
          <AlertTriangle className="size-5 text-[#9a3424] mt-0.5 shrink-0" />
          <div className="flex-1">
            <h4 className="text-[13px] font-semibold text-[#7a2517]">Could not read document</h4>
            <p className="mt-1 text-[12px] leading-relaxed text-[#7a2517]">{errorMsg}</p>
          </div>
          <Button size="sm" variant="secondary" onClick={() => setErrorMsg(null)}>
            Dismiss
          </Button>
        </div>
      )}

      {stage === 'idle' && (
        <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              onFile(e.dataTransfer.files?.[0]);
            }}
            className="flex flex-col items-center justify-center rounded-[2px] border-2 border-dashed border-[#e2d5c1] bg-[#fffaf2] px-6 py-16 text-center transition hover:border-[#9a6a35] hover:bg-[#ebe1d1]/20"
          >
            <span className="grid size-14 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] text-[#9a6a35] shadow-xs">
              <Upload className="size-6" aria-hidden />
            </span>
            <h2 className="mt-4 font-serif text-[22px] font-normal text-[#2a1c12]">Upload or photograph a document</h2>
            <p className="mt-1.5 max-w-sm text-[13px] leading-relaxed text-[#5b4a3b]">
              JPG, PNG or PDF up to 10 MB. Files are stored with client-side encryption and shared only with your explicit consent.
            </p>

            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Button onClick={() => fileRef.current?.click()}>
                <Upload className="size-4" aria-hidden /> Choose a file
              </Button>
              <Button variant="secondary" onClick={() => fileRef.current?.click()}>
                <Camera className="size-4" aria-hidden /> Use camera
              </Button>
            </div>
            <input
              ref={fileRef}
              type="file"
              accept="image/*,application/pdf"
              className="hidden"
              onChange={(e) => onFile(e.target.files?.[0])}
            />

            <div className="mt-8 w-full max-w-sm border-t border-[#e2d5c1] pt-4">
              <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-[#85725f]">No document handy?</p>
              <div className="mt-3 flex flex-col gap-2 sm:flex-row">
                <button
                  type="button"
                  onClick={() => void process('sample-legal-notice.jpg')}
                  className="flex flex-1 items-center justify-center gap-1.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 py-2 text-[12px] font-medium text-[#2a1c12] hover:border-[#9a6a35] hover:bg-[#ebe1d1]/30 transition-colors"
                >
                  <FileText className="size-3.5 text-[#9a6a35]" aria-hidden /> Sample notice
                </button>
                <button
                  type="button"
                  onClick={() => void process('blurry-photo-scan.jpg')}
                  className="flex flex-1 items-center justify-center gap-1.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-3 py-2 text-[12px] font-medium text-[#2a1c12] hover:border-[#9a6a35] hover:bg-[#ebe1d1]/30 transition-colors"
                >
                  <FileImage className="size-3.5 text-[#b97a29]" aria-hidden /> Low-quality sample
                </button>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-6">
              <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-[#85725f]">What you&apos;ll get</p>
              <ul className="mt-4 space-y-3">
                {[
                  ['Document type', 'Notice, FIR, commercial agreement, or court summons'],
                  ['Plain summary', 'Factual breakdown stripped of confusing legalese'],
                  ['Parties & dates', 'Issuing authority/counterparty and response deadlines'],
                  ['Amounts & liabilities', 'Demanded sums, fees, or performance obligations'],
                  ['Statutory risks', 'Procedural consequences of non-compliance'],
                ].map(([t, d]) => (
                  <li key={t} className="flex gap-2.5">
                    <Check className="mt-0.5 size-4 shrink-0 text-[#2a6b3b]" aria-hidden />
                    <span className="text-[12.5px] leading-relaxed text-[#5b4a3b]">
                      <span className="font-medium text-[#2a1c12]">{t}: </span>
                      {d}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/30 p-4">
              <p className="text-[12px] leading-relaxed text-[#5b4a3b]">Your document is processed privately. You choose whether to save it to your vault or share it.</p>
            </div>
          </div>
        </div>
      )}

      {stage === 'ocr' && (
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] flex flex-col items-center px-6 py-20 text-center">
          <div className="grid size-16 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6]">
            <Loader2 className="size-7 animate-spin text-[#9a6a35]" />
          </div>
          <h2 className="mt-5 font-serif text-[24px] font-normal text-[#2a1c12]">Scanning document text</h2>
          <p className="mt-2 max-w-sm text-[13px] leading-relaxed text-[#5b4a3b]">
            Extracting text characters and validating OCR confidence. Complex legal stamps may take a few seconds.
          </p>
          <p className="mt-4 flex items-center gap-1.5 rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] px-3.5 py-1.5 text-[11px] font-mono text-[#5b4a3b]">
            <FileText className="size-3.5 text-[#9a6a35]" aria-hidden /> {fileName}
          </p>
          <div className="mt-6 h-1 w-full max-w-xs overflow-hidden rounded-[2px] bg-[#ebe1d1]">
            <div className="h-full w-2/3 animate-pulse rounded-[2px] bg-[#2a1c12]" />
          </div>
        </div>
      )}

      {stage === 'explain' && (
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] flex flex-col items-center px-6 py-20 text-center">
          <div className="grid size-16 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/40">
            <ScanLine className="size-7 text-[#2a6b3b]" />
          </div>
          <h2 className="mt-5 font-serif text-[24px] font-normal text-[#2a1c12]">Explaining in plain language</h2>
          <p className="mt-2 max-w-sm text-[13px] leading-relaxed text-[#5b4a3b]">Finding parties, dates, and your obligations.</p>
        </div>
      )}

      {stage === 'done' && ocr && explanation && (
        <div className="space-y-6">
          {ocr.lowConfidence && (
            <div className="flex items-start gap-3 rounded-[2px] border border-[#b97a29]/40 bg-[#fdf5eb] px-5 py-4">
              <AlertTriangle className="mt-0.5 size-5 shrink-0 text-[#b97a29]" aria-hidden />
              <div className="flex-1">
                <p className="text-[13px] font-semibold text-[#8a5b1c]">Low quality — results may not be accurate</p>
                <p className="mt-1 text-[12px] leading-relaxed text-[#5b4a3b]">
                  Only {Math.round(ocr.confidence * 100)}% of text was read clearly. Try retaking the photo in good lighting.
                </p>
              </div>
              <Button size="sm" variant="secondary" onClick={() => fileRef.current?.click()}>
                <RotateCcw className="size-3.5" aria-hidden /> Retake
              </Button>
            </div>
          )}

          <div className="grid gap-6 lg:grid-cols-[1fr_1.15fr]">
            {/* Original */}
            <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] flex flex-col overflow-hidden">
              <div className="flex items-center justify-between border-b border-[#e2d5c1] px-5 py-3.5 bg-[#ebe1d1]/20">
                <div className="flex items-center gap-2">
                  <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-[#85725f]">Source Document</p>

                </div>
                <Badge tone={ocr.lowConfidence ? 'warn' : 'mint'}>
                  {Math.round(ocr.confidence * 100)}% Confidence
                </Badge>
              </div>
              <div className="flex flex-1 items-center justify-center bg-[#f4efe6]/50 p-6">
                {preview ? (
                  <Image
                    src={preview}
                    alt="Uploaded document preview"
                    unoptimized
                    width={720}
                    height={960}
                    className="h-auto max-h-[460px] w-auto rounded-[2px] border border-[#e2d5c1] shadow-xs"
                  />
                ) : (
                  <div className="w-full max-w-sm rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-6 shadow-xs">
                    <div className="mb-4 h-2 w-1/2 rounded-[1px] bg-[#9a6a35]/40" />
                    <div className="space-y-2">
                      {Array.from({ length: 16 }).map((_, i) => (
                        <div key={i} className={cn('h-1.5 rounded-[1px] bg-[#ebe1d1]', i % 4 === 0 ? 'w-3/4' : 'w-full')} />
                      ))}
                    </div>
                    <p className="mt-5 text-center font-mono text-[10px] uppercase tracking-wider text-[#85725f]">
                      {fileName}
                    </p>
                  </div>
                )}
              </div>
              <div className="border-t border-[#e2d5c1] px-5 py-4">
                <p className="mb-2 font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Extracted text</p>
                <div className="max-h-36 overflow-y-auto rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] p-3.5">
                  <p className="font-mono text-[11px] leading-relaxed whitespace-pre-wrap text-[#2a1c12]">{ocr.text}</p>
                </div>
              </div>
            </div>

            {/* Explanation */}
            <div className="space-y-4">
              <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 sm:p-6">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Document type</p>
                    <h2 className="mt-1 font-serif text-[22px] font-normal text-[#2a1c12]">{explanation.documentType}</h2>
                  </div>
                  <Button size="sm" variant={editing ? 'primary' : 'secondary'} onClick={() => setEditing((v) => !v)}>
                    {editing ? <><Check className="size-3.5" /> Done</> : <><Pencil className="size-3.5" /> Edit</>}
                  </Button>
                </div>
                <p className="mt-3 text-[13px] leading-relaxed text-[#5b4a3b]">{explanation.summary}</p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Named Parties</p>
                  <ul className="mt-2.5 space-y-1.5">
                    {explanation.parties.map((p) => (
                      <li key={p} className="text-[12.5px] leading-relaxed text-[#2a1c12]">• {p}</li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Stated Amounts</p>
                  <div className="mt-2.5 space-y-2">
                    {amounts.map((a, i) => (
                      <div key={a.label}>
                        <p className="text-[11px] text-[#85725f]">{a.label}</p>
                        {editing ? (
                          <Input
                            value={a.value}
                            onChange={(e) => {
                              const next = [...amounts];
                              next[i] = { ...a, value: e.target.value };
                              setAmounts(next);
                            }}
                            className="mt-1 h-8 text-[12px]"
                          />
                        ) : (
                          <p className="font-serif text-[15px] font-normal text-[#2a1c12]">{a.value}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5">
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Key Statutory Dates</p>
                <div className="mt-3 divide-y divide-[#e2d5c1]">
                  {dates.map((d, i) => (
                    <div key={d.label} className="flex items-center gap-3 py-2.5 first:pt-0 last:pb-0">
                      <span className="flex-1 text-[12.5px] font-medium text-[#2a1c12]">{d.label}</span>
                      {editing ? (
                        <Input
                          value={d.value}
                          onChange={(e) => {
                            const next = [...dates];
                            next[i] = { ...d, value: e.target.value };
                            setDates(next);
                          }}
                          className="h-8 w-44 text-[12px]"
                        />
                      ) : (
                        <span className="font-mono text-[12px] font-medium text-[#9a6a35]">{d.value}</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Client Obligations</p>
                  <ul className="mt-2.5 space-y-2">
                    {explanation.obligations.map((o) => (
                      <li key={o} className="flex gap-2 text-[12px] leading-relaxed text-[#5b4a3b]">
                        <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-[#9a6a35]" /> {o}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-[2px] border border-[#9a3424]/30 bg-[#fbf2ef] p-5">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#9a3424]">Identified Legal Risks</p>
                  <ul className="mt-2.5 space-y-2">
                    {explanation.risks.map((r) => (
                      <li key={r} className="flex gap-2 text-[12px] leading-relaxed text-[#7a2517]">
                        <AlertTriangle className="mt-0.5 size-3.5 shrink-0 text-[#9a3424]" aria-hidden /> {r}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {explanation.citations && explanation.citations.length > 0 && (
                <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#85725f]">Laws cited</p>
                  <ul className="mt-2.5 space-y-2">
                    {explanation.citations.map((c, idx) => (
                      <li key={idx} className="text-[12px] leading-relaxed text-[#2a1c12]">
                        <span className="font-medium text-[#9a6a35]">{c.source_title}</span>
                        {c.section_or_paragraph ? ` — ${c.section_or_paragraph}` : ''}
                        {c.clause_heading ? `: ${c.clause_heading}` : ''}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex flex-col gap-3 sm:flex-row pt-2">
                <Button fullWidth onClick={addDates} disabled={saved}>
                  {saved ? <><Check className="size-4" /> Dates recorded</> : <><CalendarPlus className="size-4" /> Add dates to limitation tracker</>}
                </Button>
                <Button variant="secondary" onClick={() => router.push(dh('/vault'))}>
                  Save to vault <ArrowRight className="size-4" aria-hidden />
                </Button>
              </div>
              <div className="flex items-center justify-between pt-2">
                <Disclaimer text={explanation.disclaimer} />
                <button type="button" onClick={reset} className="shrink-0 text-[11px] font-mono uppercase tracking-[0.1em] text-[#9a6a35] hover:underline">
                  Scan another
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
