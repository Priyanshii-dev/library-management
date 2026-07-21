import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { profileUpdateSchema, type ProfileUpdateInput } from '@/lib/schemas';
import { useAuthGuard } from '@/hooks/use-auth-guard';
import { toast } from '@/lib/toast';

export function useProfile() {
  const { isCheckingAuth, userProfile, updateProfile } = useAuthGuard();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<ProfileUpdateInput>({
    resolver: zodResolver(profileUpdateSchema),
  });

  useEffect(() => {
    if (userProfile) {
      form.reset({ 
        first_name: userProfile.first_name, 
        last_name: userProfile.last_name, 
        email: userProfile.email, 
        phone: userProfile.phone ?? '' 
      });
    }
  }, [form, userProfile]);

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

  return {
    form,
    message,
    error,
    isSubmitting,
    isCheckingAuth,
    onSubmit: form.handleSubmit(onSubmit),
  };
}
