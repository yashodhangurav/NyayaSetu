import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "bronze" | "darkOutline";
  size?: "sm" | "md" | "lg" | "icon";
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      isLoading,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "inline-flex items-center justify-center font-sans font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#9a6a35] disabled:opacity-50 disabled:pointer-events-none cursor-pointer rounded-none border";

    const variantStyles = {
      primary:
        "border-[#2a1c12] bg-[#2a1c12] text-[#fffaf2] hover:bg-[#9a6a35] hover:border-[#9a6a35] active:bg-[#7c5226]",
      secondary:
        "border-[#e2d5c1] bg-[#ebe1d1] text-[#2a1c12] hover:bg-[#e2d5c1] hover:border-[#cfbe9e] active:bg-[#cfbe9e]",
      outline:
        "border-[#2a1c12] bg-transparent text-[#2a1c12] hover:bg-[#2a1c12] hover:text-[#fffaf2] active:bg-[#7c5226]",
      bronze:
        "border-[#9a6a35] bg-[#9a6a35] text-[#fffaf2] hover:bg-[#7c5226] hover:border-[#7c5226] active:bg-[#2a1c12]",
      ghost:
        "border-transparent bg-transparent text-[#5b4a3b] hover:text-[#2a1c12] hover:bg-[#ebe1d1]/60",
      darkOutline:
        "border-[#d1a46a]/60 bg-[#2f2116] text-[#f3ece1] hover:bg-[#9a6a35] hover:border-[#9a6a35]",
    };

    const sizeStyles = {
      sm: "h-9 px-4 text-xs uppercase tracking-[0.08em]",
      md: "h-11 px-6 text-sm tracking-normal",
      lg: "h-13 px-8 text-base tracking-normal",
      icon: "h-10 w-10 p-0",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
        {...props}
      >
        {isLoading && (
          <span className="mr-2 inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-current border-t-transparent" />
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
