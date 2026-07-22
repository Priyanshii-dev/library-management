'use client';

import { useAuthGuard } from '@/hooks/use-auth-guard';
import { useBooks } from '@/hooks/use-books';
import { useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Input } from '@/components/ui/input';
import { toast } from '@/lib/toast';
import { BookOpen, Search, Loader2 } from 'lucide-react';
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

export default function BrowseBooksPage() {
  const { isAuthenticated } = useAuthGuard();
  const { books, isLoading, error, borrowBook, setBooks } = useBooks({ enabled: isAuthenticated });

  const [search, setSearch] = useState('');
  const [selectedBook, setSelectedBook] = useState<any | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [borrowingId, setBorrowingId] = useState<number | null>(null);

  const filtered = books.filter(b =>
    b.title.toLowerCase().includes(search.toLowerCase()) ||
    b.author.toLowerCase().includes(search.toLowerCase())
  );

  const handleBorrow = async () => {
    if (!selectedBook) return;
    try {
      setBorrowingId(selectedBook.id);
      const res = await borrowBook(selectedBook.id);
      toast({ type: 'success', message: res.message || 'Book borrowed successfully!' });
      setBooks(prev => prev.map(b =>
        b.id === selectedBook.id ? { ...b, available_quantity: b.available_quantity - 1 } : b
      ));
      setIsDialogOpen(false);
    } catch (err: any) {
      toast({ type: 'error', message: err.message || 'Failed to borrow book' });
    } finally {
      setBorrowingId(null);
    }
  };

  return (
    <div className="p-4 md:p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold">Browse Books</h1>
          <p className="text-muted-foreground text-sm mt-1">Find and borrow books from the library catalog</p>
        </div>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Search title or author..."
            className="pl-9 w-full sm:w-64"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
      </div>

      <Card className="border-white/10 bg-card/80 backdrop-blur-xl shadow-xl">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-primary" />
            Available Catalog
          </CardTitle>
          <CardDescription>
            {isLoading ? 'Loading...' : `${filtered.length} book${filtered.length !== 1 ? 's' : ''} found`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && <p className="text-destructive text-sm py-4">{error}</p>}
          {isLoading ? (
            <div className="space-y-3">
              {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-12 w-full" />)}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent border-white/10">
                  <TableHead>Title</TableHead>
                  <TableHead>Author</TableHead>
                  <TableHead>Price</TableHead>
                  <TableHead>Stock</TableHead>
                  <TableHead className="text-right">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filtered.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground py-12">
                      No books found{search ? ` for "${search}"` : ''}. Ask the admin to add some!
                    </TableCell>
                  </TableRow>
                ) : filtered.map(book => (
                  <TableRow key={book.id} className="border-white/5 hover:bg-white/5">
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        <BookOpen size={14} className="text-primary shrink-0" />
                        {book.title}
                      </div>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{book.author}</TableCell>
                    <TableCell>${book.price}</TableCell>
                    <TableCell>
                      <Badge variant="outline" className={
                        book.available_quantity > 0
                          ? 'border-green-500/40 text-green-400 bg-green-500/10'
                          : 'border-destructive/40 text-destructive bg-destructive/10'
                      }>
                        {book.available_quantity} left
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        size="sm"
                        disabled={book.available_quantity <= 0}
                        onClick={() => { setSelectedBook(book); setIsDialogOpen(true); }}
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

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Confirm Borrow</DialogTitle>
            <DialogDescription>
              Borrow <strong>"{selectedBook?.title}"</strong> by {selectedBook?.author}?
            </DialogDescription>
          </DialogHeader>
          <p className="text-sm text-muted-foreground py-2">
            You will have 14 days to return this book. Standard library policies apply.
          </p>
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
