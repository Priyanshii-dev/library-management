export type ToastType = 'success' | 'error' | 'info';

export interface ToastPayload {
  id?: string;
  type: ToastType;
  message: string;
}

export function toast(payload: ToastPayload) {
  if (typeof window === 'undefined') {
    return;
  }

  window.dispatchEvent(new CustomEvent<ToastPayload>('app:toast', { detail: payload }));
}
