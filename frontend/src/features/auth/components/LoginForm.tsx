'use client';

import Link from 'next/link';
import { ArrowRight, BookOpen } from 'lucide-react';
import { useLogin } from '@/features/auth/hooks/use-login';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function LoginForm() {
  const { form: { register, formState: { errors } }, error, isSubmitting, onSubmit } = useLogin();

  return (
    <Card className="w-full max-w-md shadow-2xl border-white/10 bg-card/80 backdrop-blur-xl">
      <CardHeader className="space-y-1 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl grid place-items-center bg-primary/10">
            <BookOpen size={20} className="text-primary" />
          </div>
          <div>
            <CardTitle className="text-xl">Welcome back</CardTitle>
            <CardDescription>Sign in to your library account</CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <form onSubmit={onSubmit} className="grid gap-4">
          <div className="grid gap-1.5">
            <Label htmlFor="login-email">Email</Label>
            <Input
              id="login-email"
              type="email"
              placeholder="you@example.com"
              aria-invalid={Boolean(errors.email)}
              {...register('email')}
            />
            {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
          </div>

          <div className="grid gap-1.5">
            <Label htmlFor="login-password">Password</Label>
            <Input
              id="login-password"
              type="password"
              placeholder="Enter your password"
              aria-invalid={Boolean(errors.password)}
              {...register('password')}
            />
            {errors.password && <p className="text-destructive text-xs">{errors.password.message}</p>}
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button type="submit" disabled={isSubmitting} className="w-full mt-1">
            {isSubmitting ? 'Signing in…' : 'Sign in'} <ArrowRight size={16} />
          </Button>
        </form>

        <div className="mt-5 flex items-center justify-between text-sm text-muted-foreground">
          <Link href="/forgot-password" className="hover:text-primary transition-colors">Forgot password?</Link>
          <Link href="/register" className="hover:text-primary transition-colors">Create account</Link>
        </div>
      </CardContent>
    </Card>
  );
}
