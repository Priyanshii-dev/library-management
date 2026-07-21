'use client';

import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowRight, BookOpen } from 'lucide-react';
import { loginSchema, type LoginInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { toast } from '@/lib/toast';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (values: LoginInput) => {
    setError(null);
    setIsSubmitting(true);
    try {
      const message = await login(values);
      toast({ type: 'success', message });
      router.push('/dashboard');
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Unable to sign in';
      setError(message);
      toast({ type: 'error', message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-shell">
      <div className="card auth-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', marginBottom: '1.25rem' }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(108,124,255,0.18)' }}>
            <BookOpen size={20} color="#8da0ff" />
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Welcome back</h1>
            <p style={{ margin: 0, color: 'var(--muted)' }}>Sign in to your library account</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gap: '0.95rem' }}>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span style={{ fontSize: '0.95rem' }}>Email</span>
            <input className="input" type="email" placeholder="you@example.com" {...register('email')} />
            {errors.email && <small style={{ color: '#ff8b9a' }}>{errors.email.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span style={{ fontSize: '0.95rem' }}>Password</span>
            <input className="input" type="password" placeholder="Enter your password" {...register('password')} />
            {errors.password && <small style={{ color: '#ff8b9a' }}>{errors.password.message}</small>}
          </label>
          {error && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)' }}>{error}</div>}
          <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Signing in...' : 'Sign in'} <ArrowRight size={17} />
          </button>
        </form>

        <div style={{ marginTop: '1.1rem', display: 'flex', justifyContent: 'space-between', color: 'var(--muted)', fontSize: '0.95rem' }}>
          <Link href="/forgot-password">Forgot password?</Link>
          <Link href="/register">Create account</Link>
        </div>
      </div>
    </main>
  );
}
