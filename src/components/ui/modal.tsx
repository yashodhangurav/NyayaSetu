"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export function Modal({
  isOpen,
  onClose,
  title,
  description,
  children,
  className,
}: ModalProps) {
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    if (isOpen) {
      document.body.style.overflow = "hidden";
      window.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.body.style.overflow = "unset";
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-[#24180f]/80 backdrop-blur-xs"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: 8 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className={cn(
              "relative z-10 w-full max-w-xl rounded-none border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-8 shadow-[0_20px_50px_rgba(36,24,15,0.25)]",
              className
            )}
          >
            <button
              type="button"
              onClick={onClose}
              className="absolute top-5 right-5 p-1 text-[#85725f] hover:text-[#2a1c12] transition-colors"
              aria-label="Close dialog"
            >
              <X className="h-5 w-5" />
            </button>

            {(title || description) && (
              <div className="mb-6 space-y-1.5 pr-8">
                {title && (
                  <h3 className="font-serif text-[24px] sm:text-[28px] font-normal leading-[1.15] tracking-[-0.03em] text-[#2a1c12]">
                    {title}
                  </h3>
                )}
                {description && (
                  <p className="text-sm text-[#5b4a3b] leading-[1.5]">
                    {description}
                  </p>
                )}
              </div>
            )}

            <div>{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
