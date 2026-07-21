import { Suspense } from 'react';
import { VerifyOtpForm } from '@/features/auth/components/VerifyOtpForm';

export default function VerifyOtpPage() {
  return (
    <main className="min-h-screen grid place-items-center bg-background p-6">
      <Suspense fallback={<div className="text-slate-400">Loading verification...</div>}>
        <VerifyOtpForm />
      </Suspense>
    </main>
  );
}
