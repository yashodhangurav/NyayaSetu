"use client";

import * as React from "react";
import { ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

interface AccordionItemProps {
  title: string;
  children: React.ReactNode;
  isOpen?: boolean;
  onToggle?: () => void;
  className?: string;
}

export function AccordionItem({
  title,
  children,
  isOpen = false,
  onToggle,
  className,
}: AccordionItemProps) {
  return (
    <div className={cn("border-b border-[#e2d5c1] py-5 transition-colors", className)}>
      <button
        type="button"
        onClick={onToggle}
        className="flex w-full items-center justify-between text-left font-serif text-[18px] sm:text-[21px] font-normal leading-[1.2] tracking-[-0.02em] text-[#2a1c12] hover:text-[#9a6a35] transition-colors focus:outline-none cursor-pointer"
        aria-expanded={isOpen}
      >
        <span className="pr-6">{title}</span>
        <ChevronDown
          className={cn(
            "h-5 w-5 shrink-0 text-[#85725f] transition-transform duration-300",
            isOpen && "rotate-180 text-[#9a6a35]"
          )}
        />
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{
              height: "auto",
              opacity: 1,
              transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
            }}
            exit={{
              height: 0,
              opacity: 0,
              transition: { duration: 0.2, ease: [0.16, 1, 0.3, 1] },
            }}
            className="overflow-hidden"
          >
            <div className="pt-4 pb-2 text-[15px] text-[#5b4a3b] leading-[1.65]">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

interface AccordionProps {
  items: { id: string; title: string; content: React.ReactNode }[];
  className?: string;
  allowMultiple?: boolean;
}

export function Accordion({
  items,
  className,
  allowMultiple = false,
}: AccordionProps) {
  const [openIds, setOpenIds] = React.useState<string[]>([]);

  const handleToggle = (id: string) => {
    if (allowMultiple) {
      setOpenIds((prev) =>
        prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
      );
    } else {
      setOpenIds((prev) => (prev.includes(id) ? [] : [id]));
    }
  };

  return (
    <div className={cn("divide-y divide-[#e2d5c1] border-t border-[#e2d5c1]", className)}>
      {items.map((item) => (
        <AccordionItem
          key={item.id}
          title={item.title}
          isOpen={openIds.includes(item.id)}
          onToggle={() => handleToggle(item.id)}
        >
          {item.content}
        </AccordionItem>
      ))}
    </div>
  );
}
