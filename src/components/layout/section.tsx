import * as React from "react";
import { cn } from "@/lib/utils";
import { Container } from "./container";
import { Badge } from "@/components/ui/badge";

export interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  containerSize?: "sm" | "md" | "lg" | "xl" | "full";
  badge?: string;
  title?: string;
  subtitle?: string;
  description?: string;
  align?: "left" | "center";
  theme?: "cream" | "sand" | "dark";
  borderTop?: boolean;
  borderBottom?: boolean;
}

export function Section({
  className,
  containerSize = "xl",
  badge,
  title,
  subtitle,
  description,
  align = "left",
  theme = "cream",
  borderTop = false,
  borderBottom = false,
  children,
  ...props
}: SectionProps) {
  const themeStyles = {
    cream: "bg-[#f3ece1] text-[#2a1c12]",
    sand: "bg-[#ebe1d1] text-[#2a1c12]",
    dark: "bg-[#24180f] text-[#f3ece1]",
  };

  const isDark = theme === "dark";

  return (
    <section
      className={cn(
        "py-16 sm:py-20 lg:py-28 transition-colors",
        themeStyles[theme],
        borderTop && (isDark ? "border-t border-[#3f2c1f]" : "border-t border-[#e2d5c1]"),
        borderBottom && (isDark ? "border-b border-[#3f2c1f]" : "border-b border-[#e2d5c1]"),
        className
      )}
      {...props}
    >
      <Container size={containerSize}>
        {(badge || title || subtitle || description) && (
          <div
            className={cn(
              "mb-12 sm:mb-16",
              align === "center" ? "text-center mx-auto max-w-3xl" : "max-w-3xl"
            )}
          >
            {badge && (
              <div className="mb-4">
                <Badge variant={isDark ? "dark" : "outline"}>{badge}</Badge>
              </div>
            )}
            {title && (
              <h2
                className={cn(
                  "font-serif text-[32px] sm:text-[44px] lg:text-[56px] xl:text-[67.2px] leading-[0.98] tracking-[-0.045em] font-normal",
                  isDark ? "text-[#f3ece1]" : "text-[#2a1c12]"
                )}
              >
                {title}
              </h2>
            )}
            {subtitle && (
              <p
                className={cn(
                  "mt-4 font-serif text-[20px] sm:text-[24px] lg:text-[28px] leading-[1.2] tracking-[-0.025em]",
                  isDark ? "text-[#e2d5c1]" : "text-[#5b4a3b]"
                )}
              >
                {subtitle}
              </p>
            )}
            {description && (
              <p
                className={cn(
                  "mt-4 text-[15px] sm:text-[16px] leading-[1.65] max-w-2xl",
                  isDark ? "text-[#b8a695]" : "text-[#5b4a3b]"
                )}
              >
                {description}
              </p>
            )}
          </div>
        )}
        {children}
      </Container>
    </section>
  );
}
