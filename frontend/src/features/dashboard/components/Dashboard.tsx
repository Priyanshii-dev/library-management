'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { BookOpen, BookOpenText, Loader2 } from 'lucide-react';
import { useAuthGuard } from '@/hooks/use-auth-guard';
import { useBooks } from '@/hooks/use-books';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { toast } from '@/lib/toast';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { BookHistory } from '@/features/dashboard/components/BookHistory';

export function Dashboard() {
  const router = useRouter();
  const { isAuthenticated, isCheckingAuth, userProfile } = useAuthGuard();
  const { books, isLoading: areBooksLoading, error: booksError, borrowBook, setBooks } = useBooks({ enabled: isAuthenticated });
  
  const [borrowingId, setBorrowingId] = useState<number | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedBook, setSelectedBook] = useState<any | null>(null);

  const handleBorrow = async () => {
    if (!selectedBook) return;
    
    try {
      setBorrowingId(selectedBook.id);
      const res = await borrowBook(selectedBook.id);
      toast({ type: 'success', message: res.message || 'Book borrowed successfully' });
      
      // Update local state to reduce quantity
      setBooks(prev => prev.map(b => 
        b.id === selectedBook.id 
          ? { ...b, available_quantity: b.available_quantity - 1 } 
          : b
      ));
      setIsDialogOpen(false);
    } catch (err: unknown) {
      const message = err && typeof err === 'object' && 'message' in err ? String((err as { message?: string }).message) : 'Failed to borrow book';
      toast({ type: 'error', message });
    } finally {
      setBorrowingId(null);
    }
  };

  if (isCheckingAuth) {
    return (
      <main className="min-h-screen bg-background p-4 md:p-8 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <BookOpenText className="animate-pulse text-primary" size={48} />
          <p className="text-muted-foreground">Loading your library dashboard…</p>
        </div>
      </main>
    );
  }

  return (
    <div className="p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* Greeting */}
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl md:text-3xl font-bold">Welcome back, {userProfile?.first_name ?? 'reader'} 👋</h1>
          <p className="text-muted-foreground text-sm">Browse the catalog below and borrow your next read.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="border-white/10 bg-card/80 backdrop-blur-md">
            <CardHeader className="pb-2">
              <p className="text-xs text-muted-foreground uppercase tracking-wide font-semibold">Available titles</p>
            </CardHeader>
            <CardContent>
              {areBooksLoading
                ? <Skeleton className="h-8 w-16" />
                : <p className="text-3xl font-bold">{books.length}</p>
              }
            </CardContent>
          </Card>

          <Card className="border-white/10 bg-card/80 backdrop-blur-md">
            <CardHeader className="pb-2">
              <p className="text-xs text-muted-foreground uppercase tracking-wide font-semibold">Membership</p>
            </CardHeader>
            <CardContent>
              <Badge className="bg-green-500/20 text-green-400 border-green-500/30 text-sm px-3 py-1">Active</Badge>
            </CardContent>
          </Card>
        </div>

        {/* Book catalog as table */}
        <Card className="border-white/10 bg-card/80 backdrop-blur-xl shadow-xl">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Featured collection</CardTitle>
              <span className="text-muted-foreground text-sm">Browse the library catalog</span>
            </div>
          </CardHeader>
          <Separator className="opacity-10" />
          <CardContent className="pt-0">
            {booksError && (
              <div className="py-4 text-destructive text-sm">{booksError}</div>
            )}
            {areBooksLoading ? (
              <div className="space-y-3 pt-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Skeleton key={i} className="h-12 w-full" />
                ))}
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow className="hover:bg-transparent border-white/10">
                    <TableHead className="text-muted-foreground">Title</TableHead>
                    <TableHead className="text-muted-foreground">Author</TableHead>
                    <TableHead className="text-muted-foreground">Price</TableHead>
                    <TableHead className="text-muted-foreground">Available</TableHead>
                    <TableHead className="text-muted-foreground text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {books.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} className="text-center text-muted-foreground py-12">
                        No books available right now.
                      </TableCell>
                    </TableRow>
                  ) : books.map((book) => (
                    <TableRow key={book.id} className="border-white/5 hover:bg-white/5">
                      <TableCell className="font-medium">
                        <div className="flex items-center gap-2">
                          <BookOpen size={15} className="text-primary shrink-0" />
                          {book.title}
                        </div>
                      </TableCell>
                      <TableCell className="text-muted-foreground">{book.author}</TableCell>
                      <TableCell>${book.price}</TableCell>
                      <TableCell>
                        <Badge
                          variant="outline"
                          className={book.available_quantity > 0
                            ? 'border-green-500/40 text-green-400 bg-green-500/10'
                            : 'border-destructive/40 text-destructive bg-destructive/10'
                          }
                        >
                          {book.available_quantity} left
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button 
                          size="sm" 
                          variant="secondary"
                          disabled={book.available_quantity <= 0}
                          onClick={() => {
                            setSelectedBook(book);
                            setIsDialogOpen(true);
                          }}
                        >
                          Borrow
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>

        <BookHistory />
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Borrow Book</DialogTitle>
            <DialogDescription>
              Are you sure you want to borrow "{selectedBook?.title}" by {selectedBook?.author}?
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <p className="text-sm text-muted-foreground">
              You will have 14 days to return this book. Standard library policies apply.
            </p>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDialogOpen(false)} disabled={borrowingId !== null}>
              Cancel
            </Button>
            <Button onClick={handleBorrow} disabled={borrowingId !== null}>
              {borrowingId !== null && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Confirm Borrow
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
