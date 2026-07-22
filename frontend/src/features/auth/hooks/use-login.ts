import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, type LoginInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { toast } from '@/lib/toast';

export function useLogin() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (values: LoginInput) => {
    setError(null);
    setIsSubmitting(true);
    try {
      const message = await login(values);
      toast({ type: 'success', message });
      
      const { useAuthStore } = await import('@/store/auth-store');
      const userRole = useAuthStore.getState().userRole;
      
      if (userRole === 'Admin') {
        router.push('/admin/dashboard');
      } else {
        router.push('/dashboard');
      }
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Unable to sign in';
      setError(message);
      toast({ type: 'error', message });
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    form,
    error,
    isSubmitting,
    onSubmit: form.handleSubmit(onSubmit),
  };
}
