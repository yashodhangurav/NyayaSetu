import React from "react";
import { cn } from "@/lib/utils";

interface SectionLabelProps {
  children: React.ReactNode;
  className?: string;
}

export function SectionLabel({ children, className }: SectionLabelProps) {
  return (
    <p
      className={cn(
        "font-sans text-[12px] font-medium uppercase leading-none tracking-[0.14em] text-[#85725f]",
        className
      )}
    >
      {children}
    </p>
  );
}
