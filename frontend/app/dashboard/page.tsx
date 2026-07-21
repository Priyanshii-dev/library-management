'use client';

import { useRouter } from 'next/navigation';
import { BookOpen, LogOut, UserCircle2 } from 'lucide-react';
import { useAuthGuard } from '@/hooks/use-auth-guard';
import { useBooks } from '@/hooks/use-books';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, isCheckingAuth, userProfile, logout } = useAuthGuard();
  const { books, isLoading: areBooksLoading, error: booksError } = useBooks({ enabled: isAuthenticated });

  if (isCheckingAuth) {
    return <main className="container" style={{ paddingTop: '3rem' }}>Loading your library dashboard...</main>;
  }

  return (
    <main className="container" style={{ padding: '2rem 0 4rem' }}>
      <section className="card" style={{ padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <p style={{ margin: 0, textTransform: 'uppercase', letterSpacing: '0.2em', color: '#8da0ff' }}>LibraryHub dashboard</p>
          <h1 style={{ margin: '0.25rem 0 0', fontSize: '1.7rem' }}>Welcome back, {userProfile?.first_name ?? 'reader'}.</h1>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="btn btn-secondary" onClick={() => router.push('/profile')}>
            <UserCircle2 size={18} /> Profile
          </button>
          <button className="btn btn-secondary" onClick={() => void logout().then(() => router.push('/login'))}>
            <LogOut size={18} /> Logout
          </button>
        </div>
      </section>

      <section className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', marginTop: '1.25rem' }}>
        <div className="stat">
          <p style={{ margin: 0, color: 'var(--muted)' }}>Available titles</p>
          <h3 style={{ margin: '0.2rem 0 0', fontSize: '1.3rem' }}>{areBooksLoading ? '...' : books.length}</h3>
        </div>
        <div className="stat">
          <p style={{ margin: 0, color: 'var(--muted)' }}>Membership</p>
          <h3 style={{ margin: '0.2rem 0 0', fontSize: '1.3rem' }}>Active</h3>
        </div>
      </section>

      <section className="card" style={{ padding: '1.2rem', marginTop: '1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ margin: 0 }}>Featured collection</h2>
          <span style={{ color: 'var(--muted)' }}>Browse the library catalog</span>
        </div>
        {booksError && (
          <div className="card" style={{ padding: '0.8rem 1rem', borderColor: 'rgba(255,139,154,0.4)', background: 'rgba(255,139,154,0.12)', marginBottom: '1rem' }}>
            {booksError}
          </div>
        )}
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
          {books.map((book) => (
            <article key={book.id} className="card" style={{ padding: '1rem', background: 'rgba(255,255,255,0.04)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem' }}>
                <BookOpen size={18} color="#8da0ff" />
                <strong>{book.title}</strong>
              </div>
              <p style={{ color: 'var(--muted)', margin: '0.7rem 0' }}>{book.author}</p>
              <p style={{ margin: 0, fontSize: '0.95rem' }}>Price: ${book.price}</p>
              <p style={{ margin: '0.25rem 0 0', fontSize: '0.95rem' }}>{book.available_quantity} available</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
