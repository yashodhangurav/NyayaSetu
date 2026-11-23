"use client";

import { useEffect, useEffectEvent, useRef, useState } from "react";
import { PlusCircle, Sparkles } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { useDashboardUI } from "@/lib/dashboard-ui-context";
import { Button } from "@/components/dashboard/ui";
import {
  getAssistantAnswer,
  type AssistantAnswer,
  type ScanExplainResult,
} from "@/services/dashboard/chat-assistant";
import { EmptyState } from "./components/EmptyState";
import { ThinkingState } from "./components/ThinkingState";
import { AssistantAnswerCard } from "./components/AssistantAnswerCard";
import { ChatComposer } from "./components/ChatComposer";
import { ScanExplainResultCard } from "./components/ScanExplainResultCard";
import { Toast, type ToastMessage } from "./components/Toast";

type ChatTurn =
  | { id: string; role: "user"; userText: string }
  | { id: string; role: "assistant"; assistantAnswer: AssistantAnswer };

export default function ChatPage() {
  const { user, language } = useAuth();
  const { pushNotification } = useDashboardUI();

  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [failedSend, setFailedSend] = useState<{ query: string; message: string } | null>(null);
  const [toast, setToast] = useState<ToastMessage | null>(null);
  const [activeScanResult, setActiveScanResult] = useState<ScanExplainResult | null>(null);

  const answerStart = useRef<HTMLDivElement>(null);
  const scrollAnchorRef = useRef<HTMLDivElement>(null);
  const initialTriggered = useRef(false);
  const messageCount = useRef(0);
  const activeRequest = useRef<AbortController | null>(null);

  const showToast = (message: string, type: ToastMessage["type"] = "success") => {
    setToast({
      id: `toast_${Date.now()}`,
      message,
      type,
    });
  };

  // Keep latest messages in view; no smooth scroll animation.
  useEffect(() => {
    if (turns[turns.length - 1]?.role === "assistant" && answerStart.current) {
      answerStart.current.scrollIntoView({ block: "start" });
    } else {
      scrollAnchorRef.current?.scrollIntoView({ block: "end" });
    }
  }, [turns, isThinking, failedSend, activeScanResult]);

  // Handle new conversation
  const handleNewChat = () => {
    setTurns([]);
    setInput("");
    setIsThinking(false);
    activeRequest.current?.abort();
    activeRequest.current = null;
    setFailedSend(null);
    setActiveScanResult(null);
    showToast("Started new consultation session");
  };

  const handleSend = async (rawQuery: string, retry = false) => {
    const query = rawQuery.trim();
    if (!query || activeRequest.current) return;

    const request = new AbortController();
    activeRequest.current = request;
    setFailedSend(null);
    if (!retry) {
      setInput("");
      const id = `user-${++messageCount.current}`;
      setTurns((prev) => [...prev, { id, role: "user", userText: query }]);
    }
    setIsThinking(true);

    try {
      const answer = await getAssistantAnswer(
        query,
        language,
        AbortSignal.any([request.signal, AbortSignal.timeout(30_000)]),
      );
      if (activeRequest.current === request) {
        setTurns((prev) => [...prev, { id: answer.id, role: "assistant", assistantAnswer: answer }]);
      }
    } catch (error) {
      if (activeRequest.current === request) {
        const timedOut = error instanceof DOMException && error.name === "TimeoutError";
        setFailedSend({
          query,
          message: timedOut
            ? "The assistant took too long to respond. Please retry."
            : "The assistant couldn't respond. Please retry.",
        });
      }
    } finally {
      if (activeRequest.current === request) {
        activeRequest.current = null;
        setIsThinking(false);
      }
    }
  };

  const sendInitialQuestion = useEffectEvent((query: string) => void handleSend(query));
  useEffect(() => {
    const question = new URLSearchParams(window.location.search).get("question");
    if (question && !initialTriggered.current) {
      initialTriggered.current = true;
      sendInitialQuestion(question);
    }
  }, []);

  // Handle Scan & Explain file attach
  const handleAttachFile = (file: File) => {
    const sizeKB = (file.size / 1024).toFixed(1) + " KB";
    const name = file.name;

    let whatThisIs = "Formal Statutory Demand Notice under Sec 138 NI Act / Section 106 TPA.";
    let deadlinesFound = "15 calendar days from date of receipt to tender settlement.";
    let amounts = "₹60,000 principal claim + 18% statutory penal interest.";
    let whatToDoNext = "Issue a formal advocate reply denying non-wear deductions or disputed liability.";

    if (/agreement|lease|rent/i.test(name)) {
      whatThisIs = "Registered Residential Tenancy Agreement under Karnataka Rent Act, 1999.";
      deadlinesFound = "30-day notice period required before termination of tenancy.";
      amounts = "Monthly rental ₹22,000 · Security Deposit held: ₹1,10,000.";
      whatToDoNext = "Compile handover inspection memo and bank transaction clearance slips.";
    }

    const mockResult: ScanExplainResult = {
      fileName: name,
      fileSize: sizeKB,
      whatThisIs,
      deadlinesFound,
      amounts,
      whatToDoNext,
    };

    setActiveScanResult(mockResult);
    showToast(`Scanned and analyzed ${name}`);
  };

  // Handle Voice input transcript
  const handleVoiceTranscript = (transcript: string, detectedLang: string) => {
    setInput(transcript);
    showToast(`Voice transcribed · Detected: ${detectedLang}`);
  };

  // Save to My Cases
  const handleSaveToCases = (title: string, summary: string) => {
    pushNotification({
      title: `Matter Saved: ${title}`,
      body: summary.slice(0, 90) + "...",
      href: "/dashboard/cases",
    });
  };

  // Request Consultation
  const handleRequestConsultation = (advocateName: string) => {
    pushNotification({
      title: `Consultation Dispatched: ${advocateName}`,
      body: "Preliminary matter profile transmitted for docket review.",
      href: "/dashboard/bookings",
    });
  };

  return (
    <div className="relative mx-auto flex h-full min-h-0 w-full max-w-[52rem] flex-col px-1 sm:px-4 animate-fade">
      {/* Toast Notification Container */}
      <Toast toast={toast} onDismiss={() => setToast(null)} />

      {/* Header: Title in Gambetta serif + small ghost "New chat" button */}
      <header className="flex shrink-0 items-center justify-between pb-5 border-b border-[#e2d5c1] select-none">
        <div className="flex items-center gap-2.5">
          <span className="grid size-9 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
            <Sparkles className="size-4.5" aria-hidden="true" />
          </span>
          <h1 className="font-serif text-[24px] sm:text-[28px] font-normal tracking-tight text-[#2a1c12] leading-none">
            AI Legal Assistant
          </h1>
        </div>

        <Button
          size="sm"
          variant="ghost"
          onClick={handleNewChat}
          className="h-8 text-xs text-[#5b4a3b] hover:text-[#2a1c12] hover:bg-[#ebe1d1]/50 rounded-[2px]"
          aria-label="Start new consultation chat"
        >
          <PlusCircle className="size-3.5 mr-1 text-[#9a6a35]" aria-hidden="true" />
          New chat
        </Button>
      </header>

      {/* Main Single Column Messages Area */}
      <main className="min-h-0 flex-1 space-y-6 overflow-y-scroll overscroll-contain py-6 pr-1 [scrollbar-gutter:stable]" aria-live="polite">
        {turns.length === 0 && !isThinking ? (
          <EmptyState
            userName={user?.name?.split(" ")[0]}
            onSelectPrompt={(p) => void handleSend(p)}
          />
        ) : (
          <div className="space-y-6">
            {turns.map((turn) => {
              if (turn.role === "user") {
                return (
                  <div key={turn.id} className="flex justify-end gap-2.5 animate-in-up">
                    <div className="max-w-[88%] sm:max-w-[80%]">
                      <div className="rounded-[2px] bg-[#2a1c12] px-4.5 py-3.5 text-xs sm:text-[13.5px] leading-relaxed text-[#fffaf2] shadow-xs select-text">
                        {turn.userText}
                      </div>
                      <div className="mt-1 flex items-center justify-end gap-1.5 text-[10.5px] font-mono text-[#85725f]">
                        <span className="size-1.5 rounded-full bg-[#2e7d32]" aria-hidden="true" />
                        Delivered
                      </div>
                    </div>
                  </div>
                );
              }

              if (turn.assistantAnswer.kind === "greeting") {
                return (
                  <div key={turn.id} ref={answerStart} className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-4 text-sm leading-relaxed">
                    {turn.assistantAnswer.explanation[0]}
                  </div>
                );
              }

              return (
                <div key={turn.id} ref={answerStart} className="scroll-mt-2">
                  <AssistantAnswerCard
                    answer={turn.assistantAnswer}
                    onSaveToCases={handleSaveToCases}
                    onRequestConsultation={handleRequestConsultation}
                    onFollowUpClick={(prompt) => void handleSend(prompt)}
                    onShowToast={(msg) => showToast(msg)}
                  />
                </div>
              );
            })}

            {/* Cycling Thinking State while awaiting response */}
            {isThinking && (
              <div className="animate-in-up">
                <ThinkingState />
              </div>
            )}

            {failedSend && (
              <div role="alert" className="flex flex-wrap items-center justify-between gap-3 border border-[#e2d5c1] bg-[#fffaf2] p-3 text-sm">
                <p>{failedSend.message}</p>
                <Button size="sm" variant="secondary" onClick={() => void handleSend(failedSend.query, true)}>
                  Retry
                </Button>
              </div>
            )}

            {/* Scan & Explain Inline Card Result */}
            {activeScanResult && (
              <ScanExplainResultCard
                result={activeScanResult}
                onClose={() => setActiveScanResult(null)}
                onAskFollowUp={(p) => void handleSend(p)}
              />
            )}

            {/* Scroll Anchor */}
            <div ref={scrollAnchorRef} className="h-2" />
          </div>
        )}
      </main>

      {/* Pinned / Sticky Clean Composer at Bottom */}
      <footer className="shrink-0 z-30 pt-3 pb-2 bg-[#f4efe6]/95 backdrop-blur-md border-t border-[#e2d5c1]/70">
        <ChatComposer
          input={input}
          setInput={setInput}
          onSend={(text) => void handleSend(text)}
          onAttachFile={handleAttachFile}
          onVoiceTranscript={handleVoiceTranscript}
          streaming={isThinking}
        />
      </footer>
    </div>
  );
}
