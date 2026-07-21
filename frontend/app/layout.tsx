import './globals.css';
import type { Metadata } from 'next';
import { ToastProvider } from '@/components/toast-provider';

export const metadata: Metadata = {
  title: 'LibraryHub',
  description: 'A polished library management experience for readers and admins.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <ToastProvider />
      </body>
    </html>
  );
}
