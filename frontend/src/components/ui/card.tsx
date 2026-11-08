import * as React from "react";
import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "warmWhite" | "sand" | "cream" | "dark" | "outline";
  hoverable?: boolean;
}

export function Card({
  className,
  variant = "warmWhite",
  hoverable = false,
  children,
  ...props
}: CardProps) {
  const variantStyles = {
    warmWhite: "bg-[#fffaf2] text-[#2a1c12] border border-[#e2d5c1]",
    sand: "bg-[#ebe1d1] text-[#2a1c12] border border-[#e2d5c1]",
    cream: "bg-[#f3ece1] text-[#2a1c12] border border-[#e2d5c1]",
    dark: "bg-[#2f2116] text-[#f3ece1] border border-[#3f2c1f]",
    outline: "bg-transparent text-[#2a1c12] border border-[#e2d5c1]",
  };

  return (
    <div
      className={cn(
        "rounded-none p-6 sm:p-8 transition-all duration-200",
        variantStyles[variant],
        hoverable && "hover:border-[#cfbe9e] hover:shadow-[0_4px_24px_rgba(42,28,18,0.06)]",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("mb-5 flex flex-col space-y-2", className)} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={cn(
        "font-serif text-[22px] sm:text-[26px] lg:text-[28px] font-normal leading-[1.15] tracking-[-0.03em] text-[#2a1c12]",
        className
      )}
      {...props}
    >
      {children}
    </h3>
  );
}

export function CardDescription({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p className={cn("text-[14px] sm:text-[15px] text-[#5b4a3b] leading-[1.6]", className)} {...props}>
      {children}
    </p>
  );
}

export function CardContent({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("space-y-4", className)} {...props}>
      {children}
    </div>
  );
}

export function CardFooter({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("mt-6 flex items-center pt-4 border-t border-[#e2d5c1]", className)}
      {...props}
    >
      {children}
    </div>
  );
}
