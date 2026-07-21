import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';

export function useAuthGuard() {
  const router = useRouter();
  const auth = useAuth();

  useEffect(() => {
    void auth.initializeAuth();
  }, [auth.initializeAuth]);

  useEffect(() => {
    if (!auth.isCheckingAuth && !auth.isAuthenticated) {
      router.replace('/login');
    }
  }, [auth.isAuthenticated, auth.isCheckingAuth, router]);

  return auth;
}
