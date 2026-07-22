'use client';

import { useEffect, useState } from 'react';
import { bookActions } from '@/actions/book-actions';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/lib/toast';
import { Clock, CheckCircle, RotateCcw, Loader2 } from 'lucide-react';

export function BookHistory() {
  const [history, setHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [processingId, setProcessingId] = useState<number | null>(null);

  const fetchHistory = async () => {
    try {
      setIsLoading(true);
      const res = await bookActions.getBorrowHistory();
      setHistory(res.data || []);
    } catch (err: any) {
      toast({ type: 'error', message: err.message || 'Failed to load borrowing history' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleReturn = async (borrowId: number) => {
    try {
      setProcessingId(borrowId);
      const res = await bookActions.returnBook(borrowId);
      toast({ type: 'success', message: res.message || 'Book returned successfully' });
      await fetchHistory(); // Refresh the list
    } catch (err: any) {
      toast({ type: 'error', message: err.message || 'Failed to return book' });
    } finally {
      setProcessingId(null);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Borrowed':
        return <Badge variant="outline" className="text-amber-500 border-amber-500/50 bg-amber-500/10">Borrowed</Badge>;
      case 'Returned':
        return <Badge variant="outline" className="text-green-500 border-green-500/50 bg-green-500/10">Returned</Badge>;
      case 'Overdue':
        return <Badge variant="outline" className="text-destructive border-destructive/50 bg-destructive/10">Overdue</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  return (
    <Card className="border-white/10 bg-card/80 backdrop-blur-xl shadow-xl mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="w-5 h-5 text-primary" />
          My Borrowing History
        </CardTitle>
        <CardDescription>Track your active and past borrowed books</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3 pt-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-12 w-full" />
            ))}
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent border-white/10">
                <TableHead className="text-muted-foreground">Book ID</TableHead>
                <TableHead className="text-muted-foreground">Status</TableHead>
                <TableHead className="text-muted-foreground">Borrowed On</TableHead>
                <TableHead className="text-muted-foreground">Due Date</TableHead>
                <TableHead className="text-muted-foreground text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {history.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                    You haven't borrowed any books yet.
                  </TableCell>
                </TableRow>
              ) : history.map((record) => (
                <TableRow key={record.id} className="border-white/5 hover:bg-white/5">
                  <TableCell className="font-medium">#{record.book_id}</TableCell>
                  <TableCell>{getStatusBadge(record.status)}</TableCell>
                  <TableCell>{new Date(record.borrowed_at).toLocaleDateString()}</TableCell>
                  <TableCell>{new Date(record.due_date).toLocaleDateString()}</TableCell>
                  <TableCell className="text-right">
                    {record.status === 'Borrowed' && (
                      <Button 
                        size="sm" 
                        variant="secondary"
                        onClick={() => handleReturn(record.id)}
                        disabled={processingId !== null}
                      >
                        {processingId === record.id ? <Loader2 className="h-4 w-4 mr-1 animate-spin" /> : <RotateCcw className="h-4 w-4 mr-1" />}
                        Return Book
                      </Button>
                    )}
                    {record.status === 'Returned' && (
                      <CheckCircle className="inline-block w-5 h-5 text-green-500 mr-2 opacity-50" />
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
