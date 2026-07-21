'use client';

import Link from 'next/link';
import { ArrowRight, Mail } from 'lucide-react';
import { useForgotPassword } from '@/features/auth/hooks/use-forgot-password';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function ForgotPasswordForm() {
  const { form: { register, formState: { errors } }, message, error, isSubmitting, onSubmit } = useForgotPassword();

  return (
    <Card className="w-full max-w-md shadow-2xl border-white/10 bg-card/80 backdrop-blur-xl">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl grid place-items-center bg-primary/10">
            <Mail size={20} className="text-primary" />
          </div>
          <div>
            <CardTitle className="text-xl">Reset password</CardTitle>
            <CardDescription>We will send a one-time code to your email.</CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <form onSubmit={onSubmit} className="grid gap-4">
          <div className="grid gap-1.5">
            <Label htmlFor="fp-email">Email</Label>
            <Input id="fp-email" type="email" aria-invalid={Boolean(errors.email)} {...register('email')} />
            {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
          </div>

          {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
          {message && <Alert className="border-green-500/40 bg-green-500/10 text-green-400"><AlertDescription>{message}</AlertDescription></Alert>}

          <Button type="submit" disabled={isSubmitting} className="w-full mt-1">
            {isSubmitting ? 'Sending…' : 'Send reset code'} <ArrowRight size={16} />
          </Button>
        </form>

        <p className="text-muted-foreground mt-5 text-center text-sm">
          <Link href="/login" className="text-primary hover:underline font-medium">Back to login</Link>
        </p>
      </CardContent>
    </Card>
  );
}
