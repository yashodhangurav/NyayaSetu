"use client";

import React, { useRef, useState, useEffect } from "react";
import { Paperclip, Mic, Send, Square } from "lucide-react";
import { Button } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";

interface ChatComposerProps {
  input: string;
  setInput: (value: string) => void;
  onSend: (text: string) => void;
  onAttachFile: (file: File) => void;
  onVoiceTranscript: (transcript: string, detectedLang: string) => void;
  streaming: boolean;
}

export function ChatComposer({
  input,
  setInput,
  onSend,
  onAttachFile,
  onVoiceTranscript,
  streaming,
}: ChatComposerProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);

  // Grow with the text up to roughly six lines.
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    const nextHeight = Math.min(el.scrollHeight, 160);
    el.style.height = `${Math.max(nextHeight, 44)}px`;
  }, [input]);

  // Voice recording simulation
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isRecording) {
      timer = setInterval(() => {
        setRecordingSeconds((seconds) => {
          if (seconds >= 2) {
            setIsRecording(false);
            const mockTranscript =
              "My landlord has not returned my security deposit of ₹60,000 after I vacated the tenancy in Belagavi.";
            onVoiceTranscript(mockTranscript, "English (India) · ಧ್ವನಿ ಗುರುತಿಸಲಾಗಿದೆ");
            return 0;
          }
          return seconds + 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isRecording, onVoiceTranscript]);

  const toggleRecording = () => {
    if (!isRecording) {
      setRecordingSeconds(0);
      setIsRecording(true);
    } else {
      setIsRecording(false);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      if (input.trim() && !streaming) {
        onSend(input);
      }
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onAttachFile(file);
      event.target.value = "";
    }
  };

  const iconButton =
    "grid size-10 shrink-0 place-items-center rounded-[2px] text-[#85725f] transition-colors hover:bg-[#ebe1d1]/60 hover:text-[#2a1c12] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] active:bg-[#e2d5c1] sm:size-9";

  return (
    <div className="w-full">
      {isRecording && (
        <div className="mb-2 flex items-center justify-between rounded-[2px] border border-[#b54708]/40 bg-[#fff8e7] px-3.5 py-2 text-xs text-[#b54708]">
          <div className="flex items-center gap-2">
            <span className="size-2 rounded-full bg-[#b54708] motion-safe:animate-pulse" />
            <span className="font-medium">Recording audio ({recordingSeconds}s)...</span>
          </div>
          <button
            type="button"
            onClick={() => setIsRecording(false)}
            className="inline-flex min-h-10 items-center gap-1 font-medium hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] sm:min-h-8"
          >
            <Square className="size-3 fill-current" aria-hidden="true" />
            Stop
          </button>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.png,.jpg,.jpeg,.doc,.docx"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* One container, one focus ring, no extra borders. */}
      <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-1.5 shadow-[0_1px_2px_rgba(42,28,18,0.04)] transition-colors focus-within:border-[#9a6a35] focus-within:ring-1 focus-within:ring-[#9a6a35]">
        <div className="flex items-end gap-1.5">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            aria-label="Scan & Explain document"
            title="Scan & Explain (PDF, notice, agreement)"
            className={iconButton}
          >
            <Paperclip className="size-4" aria-hidden="true" />
          </button>

          <textarea
            ref={textareaRef}
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder="Describe your problem in any language..."
            aria-label="Describe your problem in any language"
            className="max-h-40 min-h-11 flex-1 resize-none bg-transparent px-2 py-2.5 text-[13px] leading-relaxed text-[#2a1c12] placeholder:text-[#85725f]/60 focus:outline-none sm:text-sm"
          />

          <button
            type="button"
            onClick={toggleRecording}
            aria-label={isRecording ? "Stop voice recording" : "Voice input"}
            title="Speak your legal inquiry (simulates speech-to-text)"
            className={cn(
              iconButton,
              isRecording && "bg-[#b54708] text-[#fffaf2] hover:bg-[#9a3c06] hover:text-[#fffaf2]"
            )}
          >
            <Mic className="size-4" aria-hidden="true" />
          </button>

          <Button
            type="button"
            size="sm"
            variant="primary"
            onClick={() => {
              if (input.trim() && !streaming) onSend(input);
            }}
            disabled={!input.trim() || streaming}
            className="size-10 shrink-0 !px-0 rounded-[2px] sm:size-9"
            aria-label="Send query"
          >
            <Send className="size-3.5" aria-hidden="true" />
          </Button>
        </div>
      </div>

      <p className="mt-2 text-center text-xs leading-relaxed text-[#85725f]">
        Legal information, not legal advice. Confirm with an advocate for your situation.
      </p>
    </div>
  );
}
