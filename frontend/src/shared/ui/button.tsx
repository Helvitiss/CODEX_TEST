import * as React from 'react';
import type { ButtonHTMLAttributes } from 'react';
import { cn } from '@/shared/lib/utils';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive';
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', ...props }, ref) => (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:pointer-events-none disabled:opacity-50',
        variant === 'default' && 'bg-blue-600 text-white hover:bg-blue-700',
        variant === 'outline' && 'border border-slate-300 bg-white hover:bg-slate-100',
        variant === 'ghost' && 'hover:bg-slate-100',
        variant === 'destructive' && 'bg-red-600 text-white hover:bg-red-700',
        className
      )}
      ref={ref}
      {...props}
    />
  )
);
Button.displayName = 'Button';
