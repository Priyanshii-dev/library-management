'use client';

import Link from 'next/link';
import { ArrowRight, MailCheck, RefreshCw } from 'lucide-react';
import { useVerifyOtp } from '@/features/auth/hooks/use-verify-otp';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function VerifyOtpForm() {
  const {
    form: { register, formState: { errors } },
    error,
    message,
    secondsLeft,
    isVerifying,
    isResending,
    onResendOtp,
    onSubmit,
  } = useVerifyOtp();

  return (
    <Card className="w-full max-w-md shadow-2xl border-white/10 bg-card/80 backdrop-blur-xl">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl grid place-items-center bg-primary/10">
            <MailCheck size={20} className="text-primary" />
          </div>
          <div>
            <CardTitle className="text-xl">Verify your email</CardTitle>
            <CardDescription>Enter the 6-digit code sent to your inbox.</CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <form onSubmit={onSubmit} className="grid gap-4">
          <div className="grid gap-1.5">
            <Label htmlFor="otp-email">Email</Label>
            <Input id="otp-email" type="email" aria-invalid={Boolean(errors.email)} {...register('email')} />
            {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="otp-code">OTP code</Label>
            <Input
              id="otp-code"
              className="tracking-[0.3em] text-center text-lg font-mono"
              inputMode="numeric"
              maxLength={6}
              placeholder="------"
              aria-invalid={Boolean(errors.otp_code)}
              {...register('otp_code')}
            />
            {errors.otp_code && <p className="text-destructive text-xs">{errors.otp_code.message}</p>}
          </div>

          {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
          {message && <Alert className="border-green-500/40 bg-green-500/10 text-green-400"><AlertDescription>{message}</AlertDescription></Alert>}

          <Button type="submit" disabled={isVerifying} className="w-full mt-1">
            {isVerifying ? 'Verifying…' : 'Verify OTP'} <ArrowRight size={16} />
          </Button>

          <Button
            type="button"
            variant="secondary"
            disabled={secondsLeft > 0 || isResending}
            onClick={onResendOtp}
            className="w-full"
          >
            <RefreshCw size={15} className={isResending ? 'animate-spin' : ''} />
            {isResending ? 'Sending…' : secondsLeft > 0 ? `Resend OTP in ${secondsLeft}s` : 'Resend OTP'}
          </Button>
        </form>

        <p className="text-muted-foreground mt-5 text-center text-sm">
          Already verified?{' '}
          <Link href="/login" className="text-primary hover:underline font-medium">Sign in</Link>
        </p>
      </CardContent>
    </Card>
  );
}
