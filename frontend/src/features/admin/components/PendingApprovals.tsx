'use client';

import { useEffect, useState } from 'react';
import { adminService } from '@/services/admin-service';
import type { UserProfile } from '@/types/auth';
import { toast } from '@/lib/toast';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Check, X, Loader2 } from 'lucide-react';

export function PendingApprovals() {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [processingId, setProcessingId] = useState<number | null>(null);

  const fetchUsers = async () => {
    try {
      setIsLoading(true);
      const res = await adminService.getPendingApprovals();
      setUsers(res.data || []);
    } catch (err: unknown) {
      toast({ type: 'error', message: 'Failed to load pending approvals' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleApprove = async (userId: number) => {
    try {
      setProcessingId(userId);
      const res = await adminService.approveUser(userId);
      toast({ type: 'success', message: res.message || 'User approved' });
      setUsers(users.filter(u => u.id !== userId));
    } catch (err: unknown) {
      toast({ type: 'error', message: 'Failed to approve user' });
    } finally {
      setProcessingId(null);
    }
  };

  const handleReject = async (userId: number) => {
    try {
      setProcessingId(userId);
      const res = await adminService.rejectUser(userId);
      toast({ type: 'success', message: res.message || 'User rejected' });
      setUsers(users.filter(u => u.id !== userId));
    } catch (err: unknown) {
      toast({ type: 'error', message: 'Failed to reject user' });
    } finally {
      setProcessingId(null);
    }
  };

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Pending Approvals</CardTitle>
          <CardDescription>Loading users...</CardDescription>
        </CardHeader>
        <CardContent className="flex justify-center p-6">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Pending Approvals</CardTitle>
        <CardDescription>
          {users.length === 0 
            ? 'No pending users.' 
            : `You have ${users.length} users waiting for approval.`}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {users.length > 0 && (
          <div className="rounded-md border border-white/10">
            <Table>
              <TableHeader>
                <TableRow className="border-white/10 hover:bg-transparent">
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Phone</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id} className="border-white/10">
                    <TableCell className="font-medium">
                      {user.first_name} {user.last_name}
                    </TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>{user.phone || 'N/A'}</TableCell>
                    <TableCell className="text-right space-x-2">
                      <Button
                        size="sm"
                        variant="default"
                        onClick={() => handleApprove(user.id)}
                        disabled={processingId !== null}
                      >
                        {processingId === user.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Check className="h-4 w-4 mr-1" />}
                        Approve
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleReject(user.id)}
                        disabled={processingId !== null}
                      >
                        <X className="h-4 w-4 mr-1" />
                        Reject
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
