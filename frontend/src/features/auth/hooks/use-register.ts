import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm, type FieldErrors } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema, type RegisterInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { toast } from '@/lib/toast';

export function useRegister() {
  const router = useRouter();
  const { register: registerAction } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
    mode: 'onTouched',
    reValidateMode: 'onChange',
  });

  const onSubmit = async (values: RegisterInput) => {
    setError(null);
    setSuccess(null);
    setIsSubmitting(true);
    try {
      const result = await registerAction(values);
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

  return {
    form,
    error,
    success,
    isSubmitting,
    onSubmit: form.handleSubmit(onSubmit, onInvalid),
  };
}
