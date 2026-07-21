'use client';

import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowRight, Lock } from 'lucide-react';
import { resetPasswordSchema, type ResetPasswordInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { useState } from 'react';
import { toast } from '@/lib/toast';

export default function ResetPasswordPage() {
  const { resetPassword } = useAuth();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<ResetPasswordInput>({ resolver: zodResolver(resetPasswordSchema) });

  const onSubmit = async (values: ResetPasswordInput) => {
    setError(null);
    setMessage(null);
    setIsSubmitting(true);
    try {
      const result = await resetPassword(values);
      setMessage(result);
      toast({ type: 'success', message: result });
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Reset failed';
      setError(message);
      toast({ type: 'error', message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-shell">
      <div className="card auth-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', marginBottom: '1rem' }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(35,201,164,0.16)' }}>
            <Lock size={20} color="#5ee0bc" />
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Set a new password</h1>
            <p style={{ margin: 0, color: 'var(--muted)' }}>Enter your OTP and a new secure password.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gap: '0.9rem' }}>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Email</span>
            <input className="input" type="email" {...register('email')} />
            {errors.email && <small style={{ color: '#ff8b9a' }}>{errors.email.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>OTP code</span>
            <input className="input" {...register('otp_code')} />
            {errors.otp_code && <small style={{ color: '#ff8b9a' }}>{errors.otp_code.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>New password</span>
            <input className="input" type="password" {...register('new_password')} />
            {errors.new_password && <small style={{ color: '#ff8b9a' }}>{errors.new_password.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Confirm password</span>
            <input className="input" type="password" {...register('confirm_new_password')} />
            {errors.confirm_new_password && <small style={{ color: '#ff8b9a' }}>{errors.confirm_new_password.message}</small>}
          </label>
          {error && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)' }}>{error}</div>}
          {message && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(35,201,164,0.35)', background: 'rgba(35,201,164,0.12)' }}>{message}</div>}
          <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Resetting...' : 'Reset password'} <ArrowRight size={17} />
          </button>
        </form>

        <p style={{ color: 'var(--muted)', marginTop: '1rem' }}>
          <Link href="/login" style={{ color: '#8ca0ff' }}>Back to login</Link>
        </p>
      </div>
    </main>
  );
}
