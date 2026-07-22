'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PendingApprovals } from '@/features/admin/components/PendingApprovals';
import { AdminBooksManager } from '@/features/admin/components/AdminBooksManager';
import { AddBookModal } from '@/features/admin/components/AddBookModal';
import { adminService } from '@/services/admin-service';
import { useAuthGuard } from '@/hooks/use-auth-guard';
import { Loader2 } from 'lucide-react';

export default function AdminDashboardPage() {
  const router = useRouter();
  const { userRole, isAuthenticated, isCheckingAuth } = useAuthGuard();
  const [stats, setStats] = useState({ total_books: 0, active_users: 0 });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isCheckingAuth && (!isAuthenticated || userRole !== 'Admin')) {
      router.push('/admin-login');
      return;
    }

    if (isAuthenticated && userRole === 'Admin') {
      adminService.getDashboardStats()
        .then(res => setStats({
          total_books: res.data?.total_users ?? 0,
          active_users: res.data?.approved_users ?? 0,
        }))
        .finally(() => setIsLoading(false));
    }
  }, [isAuthenticated, isCheckingAuth, userRole, router]);

  if (isCheckingAuth || (isAuthenticated && userRole !== 'Admin')) {
    return (
      <main className="min-h-screen bg-background p-4 flex items-center justify-center">
        <Loader2 className="animate-spin text-primary h-8 w-8" />
      </main>
    );
  }

  return (
    <div className="container mx-auto py-10 px-4 space-y-6">
        <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
          <p className="text-muted-foreground">Manage library resources, users, and settings.</p>
        </div>
        <AddBookModal />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Total Books</CardTitle>
            <CardDescription>Inventory overview</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? <Loader2 className="animate-spin text-muted-foreground" size={24} /> : <p className="text-3xl font-bold">{stats.total_books}</p>}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Active Users</CardTitle>
            <CardDescription>Members currently registered</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? <Loader2 className="animate-spin text-muted-foreground" size={24} /> : <p className="text-3xl font-bold">{stats.active_users}</p>}
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <PendingApprovals />
      </div>

      <AdminBooksManager />
    </div>
  );
}
