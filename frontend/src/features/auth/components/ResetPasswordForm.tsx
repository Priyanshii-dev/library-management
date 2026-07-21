'use client';

import Link from 'next/link';
import { ArrowRight, Lock } from 'lucide-react';
import { useResetPassword } from '@/features/auth/hooks/use-reset-password';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function ResetPasswordForm() {
  const { form: { register, formState: { errors } }, message, error, isSubmitting, onSubmit } = useResetPassword();

  return (
    <Card className="w-full max-w-md shadow-2xl border-white/10 bg-card/80 backdrop-blur-xl">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl grid place-items-center bg-primary/10">
            <Lock size={20} className="text-primary" />
          </div>
          <div>
            <CardTitle className="text-xl">Set a new password</CardTitle>
            <CardDescription>Enter your OTP and choose a new secure password.</CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <form onSubmit={onSubmit} className="grid gap-4">
          <div className="grid gap-1.5">
            <Label htmlFor="rp-email">Email</Label>
            <Input id="rp-email" type="email" aria-invalid={Boolean(errors.email)} {...register('email')} />
            {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="rp-otp">OTP code</Label>
            <Input id="rp-otp" className="tracking-[0.25em]" aria-invalid={Boolean(errors.otp_code)} {...register('otp_code')} />
            {errors.otp_code && <p className="text-destructive text-xs">{errors.otp_code.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="rp-new">New password</Label>
            <Input id="rp-new" type="password" aria-invalid={Boolean(errors.new_password)} {...register('new_password')} />
            {errors.new_password && <p className="text-destructive text-xs">{errors.new_password.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="rp-confirm">Confirm password</Label>
            <Input id="rp-confirm" type="password" aria-invalid={Boolean(errors.confirm_new_password)} {...register('confirm_new_password')} />
            {errors.confirm_new_password && <p className="text-destructive text-xs">{errors.confirm_new_password.message}</p>}
          </div>

          {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
          {message && <Alert className="border-green-500/40 bg-green-500/10 text-green-400"><AlertDescription>{message}</AlertDescription></Alert>}

          <Button type="submit" disabled={isSubmitting} className="w-full mt-1">
            {isSubmitting ? 'Resetting…' : 'Reset password'} <ArrowRight size={16} />
          </Button>
        </form>

        <p className="text-muted-foreground mt-5 text-center text-sm">
          <Link href="/login" className="text-primary hover:underline font-medium">Back to login</Link>
        </p>
      </CardContent>
    </Card>
  );
}
