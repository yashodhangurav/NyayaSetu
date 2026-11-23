"use client";

import React, { Suspense, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ArrowDown, PlusCircle, Sparkles } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { useDashboardUI } from "@/lib/dashboard-ui-context";
import { Button, PageLoader } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";
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
import { BrandMark } from "./components/primitives/BrandMark";
import { SectionLabel } from "./components/primitives/SectionLabel";
import styles from "./chat.module.css";

interface ChatTurn {
  id: string;
  role: "user" | "assistant";
  userText?: string;
  detectedLang?: string;
  assistantAnswer?: AssistantAnswer;
  isStreaming?: boolean;
  streamedText?: string;
  scanResult?: ScanExplainResult;
  timestamp: string;
}

export default function ChatPage() {
  return (
    <Suspense fallback={<PageLoader />}>
      <ChatContent />
    </Suspense>
  );
}

function ChatContent() {
  const searchParams = useSearchParams();
  const { user } = useAuth();
  const { pushNotification } = useDashboardUI();
  const initialQuestion = searchParams.get("question");

  const [turns, setTurns] = useState<ChatTurn[]>([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [streamingTurnId, setStreamingTurnId] = useState<string | null>(null);
  const [toast, setToast] = useState<ToastMessage | null>(null);
  const [activeScanResult, setActiveScanResult] = useState<ScanExplainResult | null>(null);
  const [showJumpToLatest, setShowJumpToLatest] = useState(false);

  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const scrollAnchorRef = useRef<HTMLDivElement>(null);
  const initialTriggered = useRef(false);

  const showToast = (message: string, type: ToastMessage["type"] = "success") => {
    setToast({
      id: `toast_${Date.now()}`,
      message,
      type,
    });
  };

  // Only follow the conversation when the reader is already near the bottom.
  const isNearBottom = () => {
    const el = messagesContainerRef.current;
    if (!el) return true;
    return el.scrollHeight - el.scrollTop - el.clientHeight < 120;
  };

  const scrollToBottom = (behavior: ScrollBehavior = "smooth") => {
    const el = messagesContainerRef.current;
    if (!el) return;
    el.scrollTo({ top: el.scrollHeight, behavior });
    setShowJumpToLatest(false);
  };

  useEffect(() => {
    if (isThinking || isNearBottom()) {
      const timeout = setTimeout(() => scrollToBottom("smooth"), 40);
      return () => clearTimeout(timeout);
    }
    setShowJumpToLatest(true);
  }, [turns, isThinking, streamingTurnId, activeScanResult]);

  // Handle new conversation
  const handleNewChat = () => {
    setTurns([]);
    setInput("");
    setIsThinking(false);
    setStreamingTurnId(null);
    setActiveScanResult(null);
    setShowJumpToLatest(false);
    showToast("Started new consultation session");
  };

  // Send message and execute mock streaming pipeline
  const handleSend = async (rawQuery: string) => {
    const query = rawQuery.trim();
    if (!query || isThinking || streamingTurnId) return;

    setInput("");
    const userTurnId = `usr_${Date.now()}`;
    const assistantTurnId = `ast_${Date.now() + 1}`;

    // Append user message
    setTurns((prev) => [
      ...prev,
      {
        id: userTurnId,
        role: "user",
        userText: query,
        timestamp: new Date().toISOString(),
      },
    ]);

    // Activate thinking state
    setIsThinking(true);

    try {
      // Fetch assistant response from typed mock service (600-900ms delay)
      const answer = await getAssistantAnswer(query);

      setIsThinking(false);
      setStreamingTurnId(assistantTurnId);

      // Initialize assistant turn in streaming mode
      setTurns((prev) => [
        ...prev,
        {
          id: assistantTurnId,
          role: "assistant",
          isStreaming: true,
          streamedText: "",
          assistantAnswer: answer,
          timestamp: new Date().toISOString(),
        },
      ]);

      // Stream words for natural agent reading experience
      const textToStream = answer.oneLineSummary;
      const words = textToStream.split(" ");
      let currentAcc = "";

      for (let i = 0; i < words.length; i++) {
        currentAcc += (i === 0 ? "" : " ") + words[i];
        const snapshot = currentAcc;
        setTurns((prev) =>
          prev.map((t) =>
            t.id === assistantTurnId
              ? { ...t, streamedText: snapshot }
              : t
          )
        );
        // Short token delay
        await new Promise((r) => setTimeout(r, 45));
      }

      // Finalize turn
      setTurns((prev) =>
        prev.map((t) =>
          t.id === assistantTurnId
            ? { ...t, isStreaming: false, streamedText: undefined }
            : t
        )
      );
    } catch {
      setIsThinking(false);
      showToast("Unable to process statutory inquiry. Please retry.", "warn");
    } finally {
      setStreamingTurnId(null);
    }
  };

  // Check URL query param on mount
  useEffect(() => {
    if (initialQuestion && !initialTriggered.current) {
      initialTriggered.current = true;
      void handleSend(initialQuestion);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialQuestion]);

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

  // Add to Court Deadlines
  const handleAddToDeadlines = (title: string, dueDate: string) => {
    pushNotification({
      title: `Deadline Scheduled: ${title}`,
      body: `Filing window due on ${dueDate} under statutory schedules.`,
      href: "/dashboard/deadlines",
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
    <>
      {/* Keep the page stationary on this route: only the conversation scrolls. */}
      <style>{`
        body:has(#chat-agent-root) { overflow: hidden !important; }
        body:has(#chat-agent-root) #main-content {
          padding-top: 0.75rem !important;
          padding-bottom: 0 !important;
          overflow: hidden !important;
          display: flex !important;
          flex-direction: column !important;
          height: calc(100dvh - 128px) !important;
        }
        @media (min-width: 1024px) {
          body:has(#chat-agent-root) #main-content { height: calc(100dvh - 64px) !important; }
        }
        body:has(#chat-agent-root) #main-content > div {
          height: 100% !important;
          display: flex !important;
          flex-direction: column !important;
        }
        body:has(#chat-agent-root) footer:not(#composer-container) { display: none !important; }
      `}</style>

      <div
        id="chat-agent-root"
        className="relative flex h-full w-full max-w-[720px] flex-col animate-fade mx-auto px-2 sm:px-4"
      >
        <Toast toast={toast} onDismiss={() => setToast(null)} />

        {/* Serif title + ghost "New chat", closed by a thin divider. */}
        <header className="flex shrink-0 select-none items-center justify-between gap-3 border-b border-[#e2d5c1] pb-4">
          <div className="flex min-w-0 items-center gap-2.5">
            <span className="grid size-9 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/50 text-[#9a6a35]">
              <Sparkles className="size-4" aria-hidden="true" />
            </span>
            <h1 className="truncate font-serif text-[22px] font-normal leading-none tracking-tight text-[#2a1c12] sm:text-[26px]">
              AI Legal Assistant
            </h1>
          </div>

          <Button
            size="sm"
            variant="ghost"
            onClick={handleNewChat}
            className="h-10 min-h-10 shrink-0 rounded-[2px] text-xs text-[#5b4a3b] hover:text-[#2a1c12] hover:bg-[#ebe1d1]/60 sm:h-8 sm:min-h-8"
            aria-label="Start new consultation chat"
          >
            <PlusCircle className="mr-1 size-3.5 text-[#9a6a35]" aria-hidden="true" />
            New chat
          </Button>
        </header>

        {/* Only this region scrolls, with soft cream fades at both ends. */}
        <div className={styles.conversationRegion}>
          <div
            ref={messagesContainerRef}
            onScroll={() => setShowJumpToLatest(!isNearBottom())}
            className={cn(styles.scrollArea, "select-text")}
            aria-live="polite"
          >
            {turns.length === 0 && !isThinking ? (
              <EmptyState
                userName={user?.name?.split(" ")[0]}
                onSelectPrompt={(p) => void handleSend(p)}
              />
            ) : (
              <div className="space-y-8">
                {turns.map((turn) => {
                  if (turn.role === "user") {
                    return (
                      <div key={turn.id} className={cn(styles.fadeIn, "flex justify-end")}>
                        <div
                          className={cn(
                            styles.userBubble,
                            "max-w-[88%] px-4 py-3 text-[13px] leading-relaxed sm:max-w-[80%]"
                          )}
                        >
                          {turn.userText}
                        </div>
                      </div>
                    );
                  }

                  if (turn.role === "assistant" && turn.assistantAnswer) {
                    // Streaming transition: brand mark + one line, no card.
                    if (turn.isStreaming) {
                      return (
                        <div key={turn.id} className={cn(styles.fadeIn, "space-y-2")}>
                          <div className="flex items-center gap-2.5">
                            <BrandMark />
                            <SectionLabel>SUMMARY</SectionLabel>
                          </div>
                          <p className="font-serif text-[17px] font-normal leading-snug text-[#2a1c12] sm:text-[19px]">
                            {turn.streamedText}
                            <span
                              className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-[#9a6a35] align-middle motion-reduce:animate-none"
                              aria-hidden="true"
                            />
                          </p>
                        </div>
                      );
                    }

                    // Fully populated structured answer anatomy.
                    return (
                      <AssistantAnswerCard
                        key={turn.id}
                        answer={turn.assistantAnswer}
                        onSaveToCases={handleSaveToCases}
                        onAddToDeadlines={handleAddToDeadlines}
                        onRequestConsultation={handleRequestConsultation}
                        onFollowUpClick={(prompt) => void handleSend(prompt)}
                        onShowToast={(msg) => showToast(msg)}
                      />
                    );
                  }

                  return null;
                })}

                {isThinking && (
                  <div className={styles.fadeIn}>
                    <ThinkingState />
                  </div>
                )}

                {activeScanResult && (
                  <ScanExplainResultCard
                    result={activeScanResult}
                    onClose={() => setActiveScanResult(null)}
                    onAskFollowUp={(p) => void handleSend(p)}
                  />
                )}

                <div ref={scrollAnchorRef} className="h-1" />
              </div>
            )}
          </div>
          <div className={styles.fadeTop} aria-hidden="true" />
          <div className={styles.fadeBottom} aria-hidden="true" />
        </div>

        {/* Pinned composer with a soft gradient rising above it. */}
        <footer
          id="composer-container"
          className="relative shrink-0 bg-[#f4efe6] pb-2 pt-2.5 pr-14 lg:pr-0"
        >
          {showJumpToLatest && (
            <div className="pointer-events-none absolute inset-x-0 bottom-full z-20 flex justify-center pb-2">
              <button
                type="button"
                onClick={() => scrollToBottom("smooth")}
                className={cn(
                  styles.jumpPill,
                  styles.fadeIn,
                  "pointer-events-auto inline-flex h-10 items-center gap-1.5 px-4 text-xs font-medium"
                )}
              >
                <ArrowDown className="size-3.5" aria-hidden="true" />
                Jump to latest
              </button>
            </div>
          )}
          <div className={styles.composerWrap}>
            <ChatComposer
              input={input}
              setInput={setInput}
              onSend={(text) => void handleSend(text)}
              onAttachFile={handleAttachFile}
              onVoiceTranscript={handleVoiceTranscript}
              streaming={isThinking || Boolean(streamingTurnId)}
            />
          </div>
        </footer>
      </div>
    </>
  );
}
