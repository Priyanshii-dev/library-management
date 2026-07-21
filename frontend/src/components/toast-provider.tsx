'use client';

import { useEffect, useState } from 'react';
import type { ToastPayload } from '@/lib/toast';

type ToastItem = Required<ToastPayload>;

export function ToastProvider() {
  const [items, setItems] = useState<ToastItem[]>([]);

  useEffect(() => {
    function handleToast(event: Event) {
      const detail = (event as CustomEvent<ToastPayload>).detail;
      if (!detail?.message) {
        return;
      }

      const id = detail.id ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
      setItems((current) => [...current, { id, type: detail.type, message: detail.message }]);
      window.setTimeout(() => {
        setItems((current) => current.filter((item) => item.id !== id));
      }, 4000);
    }

    window.addEventListener('app:toast', handleToast);
    return () => window.removeEventListener('app:toast', handleToast);
  }, []);

  return (
    <div className="toast-region" aria-live="polite" aria-atomic="true">
      {items.map((item) => (
        <div className={`toast toast-${item.type}`} key={item.id}>
          {item.message}
        </div>
      ))}
    </div>
  );
}
