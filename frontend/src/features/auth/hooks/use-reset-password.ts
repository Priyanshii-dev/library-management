import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { resetPasswordSchema, type ResetPasswordInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { toast } from '@/lib/toast';

export function useResetPassword() {
  const { resetPassword } = useAuth();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<ResetPasswordInput>({ resolver: zodResolver(resetPasswordSchema) });

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

  return {
    form,
    message,
    error,
    isSubmitting,
    onSubmit: form.handleSubmit(onSubmit),
  };
}
