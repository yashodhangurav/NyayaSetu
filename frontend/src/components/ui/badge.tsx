import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "stamp" | "gold" | "sand" | "dark" | "solid" | "outline";
}

export function Badge({
  className,
  variant = "stamp",
  children,
  ...props
}: BadgeProps) {
  const variantStyles = {
    stamp: "border border-[#e2d5c1] bg-[#fffaf2]/80 text-[#85725f]",
    gold: "border border-[#d1a46a] bg-[#fffaf2] text-[#9a6a35]",
    sand: "border border-[#e2d5c1] bg-[#ebe1d1] text-[#2a1c12]",
    dark: "border border-[#3f2c1f] bg-[#2f2116] text-[#d1a46a]",
    solid: "border border-[#2a1c12] bg-[#2a1c12] text-[#fffaf2]",
    outline: "border border-[#e2d5c1] bg-transparent text-[#5b4a3b]",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 text-[11px] font-medium font-sans uppercase tracking-[0.14em] rounded-none transition-colors",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
