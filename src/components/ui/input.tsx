import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", label, error, helperText, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-xs font-sans uppercase tracking-[0.12em] font-medium text-[#5b4a3b]"
          >
            {label}
          </label>
        )}
        <input
          id={inputId}
          type={type}
          ref={ref}
          className={cn(
            "flex h-11 w-full rounded-none border border-[#e2d5c1] bg-[#fffaf2] px-4 py-2.5 text-sm text-[#2a1c12] placeholder:text-[#85725f]/60 transition-colors focus:border-[#9a6a35] focus:outline-none focus:ring-1 focus:ring-[#9a6a35] disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-[#9e2a2b] focus:border-[#9e2a2b] focus:ring-[#9e2a2b]",
            className
          )}
          {...props}
        />
        {helperText && !error && (
          <p className="text-xs text-[#85725f]">{helperText}</p>
        )}
        {error && <p className="text-xs text-[#9e2a2b] font-medium">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, helperText, id, rows = 4, ...props }, ref) => {
    const textareaId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label
            htmlFor={textareaId}
            className="block text-xs font-sans uppercase tracking-[0.12em] font-medium text-[#5b4a3b]"
          >
            {label}
          </label>
        )}
        <textarea
          id={textareaId}
          rows={rows}
          ref={ref}
          className={cn(
            "flex w-full rounded-none border border-[#e2d5c1] bg-[#fffaf2] px-4 py-2.5 text-sm text-[#2a1c12] placeholder:text-[#85725f]/60 transition-colors focus:border-[#9a6a35] focus:outline-none focus:ring-1 focus:ring-[#9a6a35] disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-[#9e2a2b] focus:border-[#9e2a2b] focus:ring-[#9e2a2b]",
            className
          )}
          {...props}
        />
        {helperText && !error && (
          <p className="text-xs text-[#85725f]">{helperText}</p>
        )}
        {error && <p className="text-xs text-[#9e2a2b] font-medium">{error}</p>}
      </div>
    );
  }
);
Textarea.displayName = "Textarea";

export interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: { value: string; label: string }[];
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, id, options, ...props }, ref) => {
    const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label
            htmlFor={selectId}
            className="block text-xs font-sans uppercase tracking-[0.12em] font-medium text-[#5b4a3b]"
          >
            {label}
          </label>
        )}
        <select
          id={selectId}
          ref={ref}
          className={cn(
            "flex h-11 w-full rounded-none border border-[#e2d5c1] bg-[#fffaf2] px-4 py-2.5 text-sm text-[#2a1c12] transition-colors focus:border-[#9a6a35] focus:outline-none focus:ring-1 focus:ring-[#9a6a35] disabled:cursor-not-allowed disabled:opacity-50 appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2220%22%20height%3D%2220%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22none%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cpath%20d%3D%22M6%208L10%2012L14%208%22%20stroke%3D%22%2385725f%22%20stroke-width%3D%221.5%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22/%3E%3C/svg%3E')] bg-[length:16px_16px] bg-[right_12px_center] bg-no-repeat pr-10",
            error && "border-[#9e2a2b] focus:border-[#9e2a2b] focus:ring-[#9e2a2b]",
            className
          )}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="text-xs text-[#9e2a2b] font-medium">{error}</p>}
      </div>
    );
  }
);
Select.displayName = "Select";
