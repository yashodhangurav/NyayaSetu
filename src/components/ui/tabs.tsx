"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface TabItem {
  id: string;
  label: string;
  count?: number;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (id: string) => void;
  className?: string;
  variant?: "pill" | "underline";
}

export function Tabs({
  tabs,
  activeTab,
  onChange,
  className,
  variant = "pill",
}: TabsProps) {
  if (variant === "underline") {
    return (
      <div className={cn("flex space-x-6 border-b border-[#e2d5c1] overflow-x-auto hide-scrollbar", className)}>
        {tabs.map((tab) => {
          const isActive = tab.id === activeTab;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => onChange(tab.id)}
              className={cn(
                "pb-3.5 text-sm font-sans tracking-wide transition-all border-b-2 cursor-pointer whitespace-nowrap",
                isActive
                  ? "border-[#2a1c12] text-[#2a1c12] font-medium"
                  : "border-transparent text-[#85725f] hover:text-[#2a1c12]"
              )}
            >
              <span>{tab.label}</span>
              {tab.count !== undefined && (
                <span className="ml-2 text-xs opacity-60">({tab.count})</span>
              )}
            </button>
          );
        })}
      </div>
    );
  }

  return (
    <div
      className={cn(
        "inline-flex flex-wrap gap-2 border border-[#e2d5c1] bg-[#ebe1d1]/50 p-1.5 rounded-none",
        className
      )}
    >
      {tabs.map((tab) => {
        const isActive = tab.id === activeTab;
        return (
          <button
            key={tab.id}
            type="button"
            onClick={() => onChange(tab.id)}
            className={cn(
              "px-4 py-2 text-xs font-sans uppercase tracking-[0.12em] font-medium transition-all cursor-pointer rounded-none",
              isActive
                ? "bg-[#2a1c12] text-[#fffaf2] shadow-sm"
                : "text-[#5b4a3b] hover:text-[#2a1c12] hover:bg-[#fffaf2]/60"
            )}
          >
            <span>{tab.label}</span>
            {tab.count !== undefined && (
              <span className={cn("ml-2 text-[10px]", isActive ? "text-[#d1a46a]" : "text-[#85725f]")}>
                {tab.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

