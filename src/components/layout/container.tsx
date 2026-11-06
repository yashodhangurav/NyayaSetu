import * as React from "react";
import { cn } from "@/lib/utils";

export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl" | "full";
}

export function Container({
  className,
  size = "xl",
  children,
  ...props
}: ContainerProps) {
  const sizeStyles = {
    sm: "max-w-3xl",
    md: "max-w-5xl",
    lg: "max-w-6xl",
    xl: "max-w-[1424px]",
    full: "max-w-full",
  };

  return (
    <div
      className={cn(
        "mx-auto w-full px-6 sm:px-8 md:px-12 lg:px-16",
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
