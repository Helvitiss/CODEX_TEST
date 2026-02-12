import { cn } from '@/shared/lib/utils';

export function Badge({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) {
  return <span className={cn('inline-flex rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700', className)} {...props} />;
}
