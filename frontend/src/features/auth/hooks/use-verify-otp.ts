import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { otpSchema, type OtpInput } from '@/lib/schemas';
import { useAuth } from '@/hooks/use-auth';
import { toast } from '@/lib/toast';

const RESEND_SECONDS = 55;

export function useVerifyOtp() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { registeredEmail, resendOtp, verifyEmail } = useAuth();
  const initialEmail = searchParams.get('email') ?? registeredEmail ?? '';
  
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [secondsLeft, setSecondsLeft] = useState(RESEND_SECONDS);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isResending, setIsResending] = useState(false);

  const form = useForm<OtpInput>({
    resolver: zodResolver(otpSchema),
    values: { email: initialEmail, otp_code: '' },
    mode: 'onTouched',
    reValidateMode: 'onChange',
  });

  useEffect(() => {
    if (!initialEmail) return;
    form.setValue('email', initialEmail);
  }, [initialEmail, form]);

  useEffect(() => {
    if (secondsLeft <= 0) return;
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
    const email = form.getValues('email');
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

  return {
    form,
    error,
    message,
    secondsLeft,
    isVerifying,
    isResending,
    onResendOtp,
    onSubmit: form.handleSubmit(onSubmit),
  };
}
