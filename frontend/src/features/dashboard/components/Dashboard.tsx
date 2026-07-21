'use client';

import { useRouter } from 'next/navigation';
import { BookOpen, LogOut, UserCircle2, BookOpenText } from 'lucide-react';
import { useAuthGuard } from '@/hooks/use-auth-guard';
import { useBooks } from '@/hooks/use-books';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

export function Dashboard() {
  const router = useRouter();
  const { isAuthenticated, isCheckingAuth, userProfile, logout } = useAuthGuard();
  const { books, isLoading: areBooksLoading, error: booksError } = useBooks({ enabled: isAuthenticated });

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
    <main className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* Header */}
        <Card className="border-white/10 bg-card/80 backdrop-blur-xl shadow-xl">
          <CardContent className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pt-6">
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-primary mb-1">LibraryHub dashboard</p>
              <h1 className="text-2xl md:text-3xl font-bold">Welcome back, {userProfile?.first_name ?? 'reader'}.</h1>
            </div>
            <div className="flex gap-2">
              <Button variant="secondary" size="sm" onClick={() => router.push('/profile')}>
                <UserCircle2 size={16} /> Profile
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => void logout().then(() => router.push('/login'))}
              >
                <LogOut size={16} /> Logout
              </Button>
            </div>
          </CardContent>
        </Card>

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
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {books.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} className="text-center text-muted-foreground py-12">
                        No books available right now.
                      </TableCell>
                    </TableRow>
                  ) : books.map((book) => (
                    <TableRow key={book.id} className="border-white/5 hover:bg-white/5 cursor-pointer">
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
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>

      </div>
    </main>
  );
}
