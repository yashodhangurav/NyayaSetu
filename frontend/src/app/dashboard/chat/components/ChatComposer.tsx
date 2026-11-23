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

  // Auto-grow textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    const nextHeight = Math.min(el.scrollHeight, 180);
    el.style.height = `${Math.max(nextHeight, 44)}px`;
  }, [input]);

  // Voice recording simulation
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isRecording) {
      timer = setInterval(() => {
        setRecordingSeconds((s) => {
          if (s >= 2) {
            // Finish recording and populate mock transcript
            setIsRecording(false);
            const mockTranscript =
              "My landlord has not returned my security deposit of ₹60,000 after I vacated the tenancy in Belagavi.";
            onVoiceTranscript(mockTranscript, "English (India) · ಧ್ವನಿ ಗುರುತಿಸಲಾಗಿದೆ");
            return 0;
          }
          return s + 1;
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

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      if (input.trim() && !streaming) {
        onSend(input);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onAttachFile(file);
      e.target.value = "";
    }
  };

  return (
    <div className="w-full">
      {/* Voice Recording Active Waveform Indicator */}
      {isRecording && (
        <div className="mb-2 flex items-center justify-between rounded-[2px] border border-[#c0392b]/40 bg-[#fdf2f0] px-3.5 py-2 text-xs text-[#c0392b] animate-in-up">
          <div className="flex items-center gap-2">
            <span className="size-2 rounded-full bg-[#c0392b] animate-ping" />
            <span className="font-semibold">Recording audio ({recordingSeconds}s)...</span>
            <div className="flex items-center gap-0.5 ml-1" aria-hidden="true">
              <span className="h-3 w-1 bg-[#c0392b] animate-pulse" />
              <span className="h-4 w-1 bg-[#c0392b] animate-pulse delay-75" />
              <span className="h-2 w-1 bg-[#c0392b] animate-pulse delay-150" />
              <span className="h-5 w-1 bg-[#c0392b] animate-pulse delay-100" />
              <span className="h-3 w-1 bg-[#c0392b] animate-pulse delay-200" />
            </div>
          </div>
          <button
            type="button"
            onClick={() => setIsRecording(false)}
            className="flex items-center gap-1 font-semibold text-[11px] hover:underline"
          >
            <Square className="size-3 fill-current" /> Stop
          </button>
        </div>
      )}

      {/* Hidden File Input for Scan & Explain */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.png,.jpg,.jpeg,.doc,.docx"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Composer Input Box */}
      <div className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-1.5 shadow-[0_1px_2px_rgba(42,28,18,0.04)] transition-all focus-within:border-[#9a6a35] focus-within:ring-1 focus-within:ring-[#9a6a35]">
        <div className="flex items-end gap-1.5">
          {/* Scan & Explain File Attach */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            aria-label="Scan & Explain document"
            title="Scan & Explain (PDF, notice, agreement)"
            className="grid size-9 shrink-0 place-items-center rounded-[2px] text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12] transition-colors cursor-pointer"
          >
            <Paperclip className="size-4" aria-hidden="true" />
          </button>

          {/* Auto-growing Textarea */}
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            maxLength={2000}
            placeholder="Describe your problem in any language..."
            aria-label="Describe your problem in any language"
            className="max-h-44 min-h-[44px] flex-1 resize-none bg-transparent px-2 py-2.5 text-xs sm:text-sm leading-relaxed text-[#2a1c12] placeholder:text-[#85725f]/60 focus:outline-none"
          />

          {/* Voice Input Mic */}
          <button
            type="button"
            onClick={toggleRecording}
            aria-label={isRecording ? "Stop voice recording" : "Voice input"}
            title="Speak your legal inquiry (simulates speech-to-text)"
            className={cn(
              "grid size-9 shrink-0 place-items-center rounded-[2px] transition-colors cursor-pointer",
              isRecording
                ? "bg-[#c0392b] text-[#fffaf2]"
                : "text-[#85725f] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12]"
            )}
          >
            <Mic className="size-4" aria-hidden="true" />
          </button>

          {/* Send Button */}
          <Button
            type="button"
            size="sm"
            variant="primary"
            onClick={() => {
              if (input.trim() && !streaming) onSend(input);
            }}
            disabled={!input.trim() || streaming}
            className="size-9 !px-0 rounded-[2px] shrink-0"
            aria-label="Send query"
          >
            <Send className="size-3.5" aria-hidden="true" />
          </Button>
        </div>
      </div>

      {/* Static Disclaimer Line beneath - shown once only */}
      <p className="mt-2 text-center text-[11px] leading-relaxed text-[#85725f]">
        Legal information, not legal advice. Confirm with an advocate for your situation.
      </p>
    </div>
  );
}
