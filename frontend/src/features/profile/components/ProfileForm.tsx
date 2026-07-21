'use client';

import { Save, UserCircle2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { useProfile } from '@/features/profile/hooks/use-profile';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';

export function ProfileForm() {
  const {
    form: { register, formState: { errors } },
    message,
    error,
    isSubmitting,
    isCheckingAuth,
    onSubmit,
  } = useProfile();

  if (isCheckingAuth) {
    return (
      <Card className="w-full max-w-2xl mx-auto border-white/10 bg-card/80 backdrop-blur-xl">
        <CardHeader>
          <Skeleton className="h-7 w-40" />
          <Skeleton className="h-4 w-56" />
        </CardHeader>
        <CardContent className="grid gap-5">
          <div className="grid grid-cols-2 gap-5">
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
          </div>
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-32" />
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="w-full max-w-2xl mx-auto space-y-4">
      <Link
        href="/dashboard"
        className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors text-sm font-medium"
      >
        <ArrowLeft size={15} /> Back to dashboard
      </Link>

      <Card className="border-white/10 bg-card/80 backdrop-blur-xl shadow-2xl">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl grid place-items-center bg-primary/10">
              <UserCircle2 size={20} className="text-primary" />
            </div>
            <div>
              <CardTitle>Profile settings</CardTitle>
              <CardDescription>Keep your account details current.</CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <form onSubmit={onSubmit} className="grid gap-5">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div className="grid gap-1.5">
                <Label htmlFor="prof-first">First name</Label>
                <Input id="prof-first" aria-invalid={Boolean(errors.first_name)} {...register('first_name')} />
                {errors.first_name && <p className="text-destructive text-xs">{errors.first_name.message}</p>}
              </div>
              <div className="grid gap-1.5">
                <Label htmlFor="prof-last">Last name</Label>
                <Input id="prof-last" aria-invalid={Boolean(errors.last_name)} {...register('last_name')} />
                {errors.last_name && <p className="text-destructive text-xs">{errors.last_name.message}</p>}
              </div>
            </div>

            <div className="grid gap-1.5">
              <Label htmlFor="prof-email">Email</Label>
              <Input id="prof-email" type="email" aria-invalid={Boolean(errors.email)} {...register('email')} />
              {errors.email && <p className="text-destructive text-xs">{errors.email.message}</p>}
            </div>

            <div className="grid gap-1.5">
              <Label htmlFor="prof-phone">Phone</Label>
              <Input id="prof-phone" aria-invalid={Boolean(errors.phone)} {...register('phone')} />
              {errors.phone && <p className="text-destructive text-xs">{errors.phone.message}</p>}
            </div>

            {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
            {message && <Alert className="border-green-500/40 bg-green-500/10 text-green-400"><AlertDescription>{message}</AlertDescription></Alert>}

            <div>
              <Button type="submit" disabled={isSubmitting}>
                <Save size={16} /> {isSubmitting ? 'Saving…' : 'Save changes'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
