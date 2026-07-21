'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Save, UserCircle2 } from 'lucide-react';
import { profileUpdateSchema, type ProfileUpdateInput } from '@/lib/schemas';
import { useAuthGuard } from '@/hooks/use-auth-guard';
import { toast } from '@/lib/toast';

export default function ProfilePage() {
  const { isCheckingAuth, userProfile, updateProfile } = useAuthGuard();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<ProfileUpdateInput>({
    resolver: zodResolver(profileUpdateSchema),
  });

  useEffect(() => {
    if (userProfile) {
      reset({ first_name: userProfile.first_name, last_name: userProfile.last_name, email: userProfile.email, phone: userProfile.phone ?? '' });
    }
  }, [reset, userProfile]);

  const onSubmit = async (values: ProfileUpdateInput) => {
    setError(null);
    setMessage(null);
    setIsSubmitting(true);
    try {
      const result = await updateProfile(values);
      setMessage(result);
      toast({ type: 'success', message: result });
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Update failed';
      setError(message);
      toast({ type: 'error', message });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isCheckingAuth) {
    return <main className="container" style={{ paddingTop: '3rem' }}>Loading profile...</main>;
  }

  return (
    <main className="container" style={{ padding: '2rem 0 4rem' }}>
      <section className="card auth-card" style={{ width: '100%', maxWidth: 640 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', marginBottom: '1rem' }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(108,124,255,0.18)' }}>
            <UserCircle2 size={20} color="#8da0ff" />
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.2rem' }}>Profile settings</h1>
            <p style={{ margin: 0, color: 'var(--muted)' }}>Keep your account details current.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'grid', gap: '0.9rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '0.9rem' }}>
            <label style={{ display: 'grid', gap: '0.35rem' }}>
              <span>First name</span>
              <input className="input" {...register('first_name')} />
              {errors.first_name && <small style={{ color: '#ff8b9a' }}>{errors.first_name.message}</small>}
            </label>
            <label style={{ display: 'grid', gap: '0.35rem' }}>
              <span>Last name</span>
              <input className="input" {...register('last_name')} />
              {errors.last_name && <small style={{ color: '#ff8b9a' }}>{errors.last_name.message}</small>}
            </label>
          </div>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Email</span>
            <input className="input" type="email" {...register('email')} />
            {errors.email && <small style={{ color: '#ff8b9a' }}>{errors.email.message}</small>}
          </label>
          <label style={{ display: 'grid', gap: '0.35rem' }}>
            <span>Phone</span>
            <input className="input" {...register('phone')} />
            {errors.phone && <small style={{ color: '#ff8b9a' }}>{errors.phone.message}</small>}
          </label>
          {error && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)' }}>{error}</div>}
          {message && <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(35,201,164,0.35)', background: 'rgba(35,201,164,0.12)' }}>{message}</div>}
          <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
            <Save size={17} /> {isSubmitting ? 'Saving...' : 'Save changes'}
          </button>
        </form>
      </section>
    </main>
  );
}
