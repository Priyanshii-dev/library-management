// Re-export sonner toast as a unified utility matching the old API shape.
import { toast as sonnerToast } from 'sonner';

export type ToastType = 'success' | 'error' | 'info';

export interface ToastPayload {
  id?: string;
  type: ToastType;
  message: string;
}

export function toast(payload: ToastPayload) {
  if (payload.type === 'success') return sonnerToast.success(payload.message, { id: payload.id });
  if (payload.type === 'error') return sonnerToast.error(payload.message, { id: payload.id });
  return sonnerToast(payload.message, { id: payload.id });
}
