'use client';

import Link from 'next/link';
import { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowRight, MailCheck, RefreshCw } from 'lucide-react';
import { otpSchema, type OtpInput } from '@/lib/schemas';
import { toast } from '@/lib/toast';
import { useAuth } from '@/hooks/use-auth';

const RESEND_SECONDS = 55;

export default function VerifyOtpPage() {
  return (
    <Suspense fallback={<main className="auth-shell"><div className="card auth-card">Loading verification...</div></main>}>
      <VerifyOtpContent />
    </Suspense>
  );
}

function VerifyOtpContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { registeredEmail, resendOtp, verifyEmail } = useAuth();
  const initialEmail = searchParams.get('email') ?? registeredEmail ?? '';
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [secondsLeft, setSecondsLeft] = useState(RESEND_SECONDS);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isResending, setIsResending] = useState(false);

  const {
    register,
    handleSubmit,
    getValues,
    setValue,
    formState: { errors },
  } = useForm<OtpInput>({
    resolver: zodResolver(otpSchema),
    values: { email: initialEmail, otp_code: '' },
    mode: 'onTouched',
    reValidateMode: 'onChange',
  });

  useEffect(() => {
    if (!initialEmail) {
      return;
    }

    setValue('email', initialEmail);
  }, [initialEmail, setValue]);

  useEffect(() => {
    if (secondsLeft <= 0) {
      return;
    }

    const timer = window.setTimeout(() => setSecondsLeft((value) => value - 1), 1000);
    return () => window.clearTimeout(timer);
  }, [secondsLeft]);

  const onSubmit = async (values: OtpInput) => {
    setError(null);
    setMessage(null);
    setIsVerifying(true);
    try {
      const result = await verifyEmail(values);
      setMessage(result);
      toast({ type: 'success', message: result });
      window.setTimeout(() => router.push('/login'), 1000);
    } catch (err: unknown) {
      const nextMessage = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'OTP verification failed';
      setError(nextMessage);
      toast({ type: 'error', message: nextMessage });
    } finally {
      setIsVerifying(false);
    }
  };

  const onResendOtp = async () => {
    const email = getValues('email');
    if (!email) {
      const nextMessage = 'Enter your account email before requesting another OTP.';
      setError(nextMessage);
      toast({ type: 'error', message: nextMessage });
      return;
    }

    setError(null);
    setMessage(null);
    setIsResending(true);
    try {
      const result = await resendOtp(email);
      setMessage(result);
      setSecondsLeft(RESEND_SECONDS);
      toast({ type: 'success', message: result });
    } catch (err: unknown) {
      const nextMessage = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Unable to resend OTP';
      setError(nextMessage);
      toast({ type: 'error', message: nextMessage });
    } finally {
      setIsResending(false);
    }
  };

  return (
    <main className="auth-shell">
      <div className="card auth-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', marginBottom: '1rem' }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(35,201,164,0.16)' }}>
            <MailCheck size={20} color="#5ee0bc" />
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Verify email OTP</h1>
            <p style={{ margin: 0, color: 'var(--muted)' }}>Enter the code sent to your email.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gap: '0.9rem' }}>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Email</span>
            <input className="input" type="email" aria-invalid={Boolean(errors.email)} {...register('email')} />
            {errors.email && <small style={{ color: '#ff8b9a' }}>{errors.email.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>OTP code</span>
            <input className="input" inputMode="numeric" maxLength={6} aria-invalid={Boolean(errors.otp_code)} {...register('otp_code')} />
            {errors.otp_code && <small style={{ color: '#ff8b9a' }}>{errors.otp_code.message}</small>}
          </label>
          {error && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)' }}>{error}</div>}
          {message && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(35,201,164,0.35)', background: 'rgba(35,201,164,0.12)' }}>{message}</div>}
          <button className="btn btn-primary" type="submit" disabled={isVerifying}>
            {isVerifying ? 'Verifying...' : 'Verify OTP'} <ArrowRight size={17} />
          </button>
          <button className="btn btn-secondary" type="button" disabled={secondsLeft > 0 || isResending} onClick={onResendOtp}>
            <RefreshCw size={17} />
            {isResending ? 'Sending...' : secondsLeft > 0 ? `Resend OTP in ${secondsLeft}s` : 'Resend OTP'}
          </button>
        </form>

        <p style={{ color: 'var(--muted)', marginTop: '1rem', textAlign: 'center' }}>
          Already verified? <Link href="/login" style={{ color: '#8ca0ff' }}>Sign in</Link>
        </p>
      </div>
    </main>
  );
}
