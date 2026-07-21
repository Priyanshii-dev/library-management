'use client';

import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowRight, Mail } from 'lucide-react';
import { forgotPasswordSchema, type ForgotPasswordInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { useState } from 'react';
import { toast } from '@/lib/toast';

export default function ForgotPasswordPage() {
  const { forgotPassword } = useAuth();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<ForgotPasswordInput>({ resolver: zodResolver(forgotPasswordSchema) });

  const onSubmit = async (values: ForgotPasswordInput) => {
    setError(null);
    setMessage(null);
    setIsSubmitting(true);
    try {
      const result = await forgotPassword(values);
      setMessage(result);
      toast({ type: 'success', message: result });
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Request failed';
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
          <div style={{ width: 42, height: 42, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(108,124,255,0.18)' }}>
            <Mail size={20} color="#8da0ff" />
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Reset password</h1>
            <p style={{ margin: 0, color: 'var(--muted)' }}>We will send a one-time code to your email.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gap: '0.9rem' }}>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Email</span>
            <input className="input" type="email" {...register('email')} />
            {errors.email && <small style={{ color: '#ff8b9a' }}>{errors.email.message}</small>}
          </label>
          {error && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)' }}>{error}</div>}
          {message && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(35,201,164,0.35)', background: 'rgba(35,201,164,0.12)' }}>{message}</div>}
          <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Sending...' : 'Send reset code'} <ArrowRight size={17} />
          </button>
        </form>

        <p style={{ color: 'var(--muted)', marginTop: '1rem' }}>
          <Link href="/login" style={{ color: '#8ca0ff' }}>Back to login</Link>
        </p>
      </div>
    </main>
  );
}
