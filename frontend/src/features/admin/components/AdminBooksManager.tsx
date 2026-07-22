'use client';

import { useState, useEffect } from 'react';
import { adminService } from '@/services/admin-service';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/lib/toast';
import { Pencil, Trash2, Loader2, Search, BookOpen } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface Book {
  id: number;
  title: string;
  author: string;
  price: number;
  category_id: number;
  total_quantity: number;
  available_quantity: number;
  availability: string;
  publication_year?: number;
}

export function AdminBooksManager() {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [processingId, setProcessingId] = useState<number | null>(null);

  // Edit modal state
  const [editBook, setEditBook] = useState<Book | null>(null);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [editForm, setEditForm] = useState({ title: '', author: '', price: '', total_quantity: '' });
  const [isSaving, setIsSaving] = useState(false);

  // Delete confirm state
  const [deleteBook, setDeleteBook] = useState<Book | null>(null);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);

  const fetchBooks = async (q?: string) => {
    try {
      setIsLoading(true);
      const res = await adminService.listBooks({ limit: 50, search: q || undefined });
      const data = res.data;
      setBooks(Array.isArray(data) ? data : (data as any)?.items ?? []);
    } catch (err: any) {
      toast({ type: 'error', message: err.message || 'Failed to load books' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchBooks(search);
  };

  const openEdit = (book: Book) => {
    setEditBook(book);
    setEditForm({
      title: book.title,
      author: book.author,
      price: String(book.price),
      total_quantity: String(book.total_quantity),
    });
    setIsEditOpen(true);
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editBook) return;
    try {
      setIsSaving(true);
      await adminService.updateBook(editBook.id, {
        title: editForm.title,
        author: editForm.author,
        price: parseFloat(editForm.price),
        total_quantity: parseInt(editForm.total_quantity),
      });
      toast({ type: 'success', message: 'Book updated!' });
      setIsEditOpen(false);
      await fetchBooks(search || undefined);
    } catch (err: any) {
      toast({ type: 'error', message: err.message || 'Failed to update book' });
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteBook) return;
    try {
      setProcessingId(deleteBook.id);
      await adminService.deleteBook(deleteBook.id);
      toast({ type: 'success', message: 'Book deleted' });
      setIsDeleteOpen(false);
      setBooks(prev => prev.filter(b => b.id !== deleteBook.id));
    } catch (err: any) {
      toast({ type: 'error', message: err.message || 'Failed to delete book' });
    } finally {
      setProcessingId(null);
    }
  };

  return (
    <>
      <Card className="mt-6">
        <CardHeader>
          <div className="flex flex-col sm:flex-row justify-between gap-4">
            <div>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-primary" />
                Book Management
              </CardTitle>
              <CardDescription>Create, update, and delete books in the catalog</CardDescription>
            </div>
            <form onSubmit={handleSearchSubmit} className="flex gap-2">
              <Input
                placeholder="Search books..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="w-52"
              />
              <Button type="submit" size="sm" variant="secondary">
                <Search className="w-4 h-4" />
              </Button>
            </form>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-12 w-full" />)}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent border-white/10">
                  <TableHead>Title</TableHead>
                  <TableHead>Author</TableHead>
                  <TableHead>Price</TableHead>
                  <TableHead>Stock</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {books.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground py-10">
                      No books found. Click "Add Book" to add one.
                    </TableCell>
                  </TableRow>
                ) : books.map(book => (
                  <TableRow key={book.id} className="border-white/5 hover:bg-white/5">
                    <TableCell className="font-medium max-w-[180px] truncate">{book.title}</TableCell>
                    <TableCell className="text-muted-foreground">{book.author}</TableCell>
                    <TableCell>${book.price.toFixed(2)}</TableCell>
                    <TableCell>{book.available_quantity}/{book.total_quantity}</TableCell>
                    <TableCell>
                      <Badge variant="outline" className={
                        book.available_quantity > 0
                          ? 'text-green-500 border-green-500/40 bg-green-500/10'
                          : 'text-destructive border-destructive/40 bg-destructive/10'
                      }>
                        {book.available_quantity > 0 ? 'Available' : 'Out of Stock'}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right space-x-2">
                      <Button size="sm" variant="ghost" onClick={() => openEdit(book)}>
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        className="text-destructive hover:text-destructive"
                        onClick={() => { setDeleteBook(book); setIsDeleteOpen(true); }}
                        disabled={processingId === book.id}
                      >
                        {processingId === book.id
                          ? <Loader2 className="w-4 h-4 animate-spin" />
                          : <Trash2 className="w-4 h-4" />}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit Book</DialogTitle>
            <DialogDescription>Update the details for "{editBook?.title}"</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleUpdate} className="space-y-4 py-4">
            <div className="space-y-2">
              <Label>Title</Label>
              <Input value={editForm.title} onChange={e => setEditForm({ ...editForm, title: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>Author</Label>
              <Input value={editForm.author} onChange={e => setEditForm({ ...editForm, author: e.target.value })} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Price ($)</Label>
                <Input type="number" step="0.01" value={editForm.price} onChange={e => setEditForm({ ...editForm, price: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>Total Quantity</Label>
                <Input type="number" value={editForm.total_quantity} onChange={e => setEditForm({ ...editForm, total_quantity: e.target.value })} />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsEditOpen(false)}>Cancel</Button>
              <Button type="submit" disabled={isSaving}>
                {isSaving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Save Changes
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={isDeleteOpen} onOpenChange={setIsDeleteOpen}>
        <DialogContent className="sm:max-w-[400px]">
          <DialogHeader>
            <DialogTitle>Delete Book</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete <strong>"{deleteBook?.title}"</strong>? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDeleteOpen(false)}>Cancel</Button>
            <Button variant="destructive" onClick={handleDelete} disabled={processingId !== null}>
              {processingId !== null && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
