'use client';

import Link from 'next/link';
import { ArrowRight, UserRoundPlus } from 'lucide-react';
import { useRegister } from '@/features/auth/hooks/use-register';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function RegisterForm() {
  const { form: { register: formRegister, formState: { errors } }, error, success, isSubmitting, onSubmit } = useRegister();

  return (
    <Card className="w-full max-w-lg shadow-2xl border-white/10 bg-card/80 backdrop-blur-xl">
      <CardHeader className="pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl grid place-items-center bg-primary/10">
            <UserRoundPlus size={20} className="text-primary" />
          </div>
          <div>
            <CardTitle className="text-xl">Create account</CardTitle>
            <CardDescription>Join the library community</CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <form onSubmit={onSubmit} className="grid gap-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="grid gap-1.5">
              <Label htmlFor="reg-first">First name</Label>
              <Input id="reg-first" aria-invalid={Boolean(errors.first_name)} {...formRegister('first_name')} />
              {errors.first_name && <p className="text-destructive text-xs">{errors.first_name.message}</p>}
            </div>
            <div className="grid gap-1.5">
              <Label htmlFor="reg-last">Last name</Label>
              <Input id="reg-last" aria-invalid={Boolean(errors.last_name)} {...formRegister('last_name')} />
              {errors.last_name && <p className="text-destructive text-xs">{errors.last_name.message}</p>}
            </div>
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="reg-email">Email</Label>
            <Input id="reg-email" type="email" aria-invalid={Boolean(errors.email)} {...formRegister('email')} />
            {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="reg-phone">Phone</Label>
            <Input id="reg-phone" aria-invalid={Boolean(errors.phone)} {...formRegister('phone')} />
            {errors.phone && <p className="text-destructive text-xs">{errors.phone.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="reg-password">Password</Label>
            <Input id="reg-password" type="password" aria-invalid={Boolean(errors.password)} {...formRegister('password')} />
            {errors.password && <p className="text-destructive text-xs">{errors.password.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="reg-confirm">Confirm password</Label>
            <Input id="reg-confirm" type="password" aria-invalid={Boolean(errors.confirm_password)} {...formRegister('confirm_password')} />
            {errors.confirm_password && <p className="text-destructive text-xs">{errors.confirm_password.message}</p>}
          </div>

          {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
          {success && <Alert className="border-green-500/40 bg-green-500/10 text-green-400"><AlertDescription>{success}</AlertDescription></Alert>}

          <Button type="submit" disabled={isSubmitting} className="w-full mt-1">
            {isSubmitting ? 'Creating account…' : 'Create account'} <ArrowRight size={16} />
          </Button>
        </form>

        <p className="text-muted-foreground mt-5 text-center text-sm">
          Already have an account?{' '}
          <Link href="/login" className="text-primary hover:underline font-medium">Sign in</Link>
        </p>
      </CardContent>
    </Card>
  );
}
