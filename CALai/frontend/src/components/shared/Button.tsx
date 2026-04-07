import React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "tertiary" | "outline";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    const baseStyles = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50";
    
    const variants = {
      primary: "bg-gradient-to-br from-primary to-[var(--color-primary-container)] text-white shadow hover:opacity-90",
      secondary: "bg-[var(--color-primary-fixed)] text-[var(--color-on-primary-fixed)] hover:bg-[var(--color-primary-fixed-dim)]",
      tertiary: "hover:bg-gray-100 text-[var(--color-primary)]",
      outline: "border border-[var(--color-outline)] bg-transparent hover:bg-gray-50 text-foreground",
    };
    
    const sizes = {
      default: "h-9 px-4 py-2",
      sm: "h-8 rounded-md px-3 text-xs",
      lg: "h-10 rounded-md px-8",
      icon: "h-9 w-9",
    };

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size === "md" ? "default" : size], className)}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
