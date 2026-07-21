'use client';

import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowRight, UserRoundPlus } from 'lucide-react';
import { registerSchema, type RegisterInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { toast } from '@/lib/toast';
import type { FieldErrors } from 'react-hook-form';

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register: formRegister, handleSubmit, formState: { errors } } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
    mode: 'onTouched',
    reValidateMode: 'onChange',
  });

  const onSubmit = async (values: RegisterInput) => {
    setError(null);
    setSuccess(null);
    setIsSubmitting(true);
    try {
      const result = await register(values);
      setSuccess(result);
      toast({ type: 'success', message: result });
      router.push(`/verify-otp?email=${encodeURIComponent(values.email)}`);
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Registration failed';
      setError(message);
      toast({ type: 'error', message });
    } finally {
      setIsSubmitting(false);
    }
  };

  const onInvalid = (formErrors: FieldErrors<RegisterInput>) => {
    const firstError = Object.values(formErrors)[0];
    const message = typeof firstError?.message === 'string'
      ? firstError.message
      : 'Please fix the highlighted fields before registering.';

    setError(message);
    toast({ type: 'error', message });
  };

  return (
    <main className="auth-shell">
      <div className="card auth-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', marginBottom: '1rem' }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(35,201,164,0.16)' }}>
            <UserRoundPlus size={20} color="#5ee0bc" />
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Create account</h1>
            <p style={{ margin: 0, color: 'var(--muted)' }}>Join the library community</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit, onInvalid)} style={{ display: 'grid', gap: '0.9rem' }}>
          <div style={{ display: 'grid', gap: '0.9rem', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))' }}>
            <label style={{ display: 'grid', gap: '0.35rem' }}>
              <span>First name</span>
              <input className="input" aria-invalid={Boolean(errors.first_name)} {...formRegister('first_name')} />
              {errors.first_name && <small style={{ color: '#ff8b9a' }}>{errors.first_name.message}</small>}
            </label>
            <label style={{ display: 'grid', gap: '0.35rem' }}>
              <span>Last name</span>
              <input className="input" aria-invalid={Boolean(errors.last_name)} {...formRegister('last_name')} />
              {errors.last_name && <small style={{ color: '#ff8b9a' }}>{errors.last_name.message}</small>}
            </label>
          </div>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Email</span>
            <input className="input" type="email" aria-invalid={Boolean(errors.email)} {...formRegister('email')} />
            {errors.email && <small style={{ color: '#ff8b9a' }}>{errors.email.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Phone</span>
            <input className="input" aria-invalid={Boolean(errors.phone)} {...formRegister('phone')} />
            {errors.phone && <small style={{ color: '#ff8b9a' }}>{errors.phone.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Password</span>
            <input className="input" type="password" aria-invalid={Boolean(errors.password)} {...formRegister('password')} />
            {errors.password && <small style={{ color: '#ff8b9a' }}>{errors.password.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Confirm password</span>
            <input className="input" type="password" aria-invalid={Boolean(errors.confirm_password)} {...formRegister('confirm_password')} />
            {errors.confirm_password && <small style={{ color: '#ff8b9a' }}>{errors.confirm_password.message}</small>}
          </label>
          {error && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)' }}>{error}</div>}
          {success && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(35,201,164,0.35)', background: 'rgba(35,201,164,0.12)' }}>{success}</div>}
          <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Creating account...' : 'Create account'} <ArrowRight size={17} />
          </button>
        </form>

        <p style={{ color: 'var(--muted)', marginTop: '1rem', textAlign: 'center' }}>
          Already have an account? <Link href="/login" style={{ color: '#8ca0ff' }}>Sign in</Link>
        </p>
      </div>
    </main>
  );
}
