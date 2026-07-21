'use client';

import Link from 'next/link';
import { BookOpen, ShieldCheck, Sparkles, ArrowRight } from 'lucide-react';

export default function HomePage() {
  return (
    <main className="container" style={{ padding: '3rem 0 5rem' }}>
      <section className="card hero" style={{ padding: '2.5rem' }}>
        <div style={{ display: 'grid', gap: '1.25rem', maxWidth: '720px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.6rem', width: 'fit-content', padding: '0.45rem 0.8rem', borderRadius: '999px', background: 'rgba(108,124,255,0.16)', color: '#93a2ff' }}>
            <Sparkles size={16} />
            <span>Modern library experience</span>
          </div>
          <h1 style={{ fontSize: 'clamp(2rem, 4vw, 3rem)', lineHeight: 1.1, margin: 0 }}>Read smarter with a beautifully crafted digital library.</h1>
          <p style={{ color: 'var(--muted)', fontSize: '1.03rem', margin: 0 }}>Discover books, track borrow history, manage membership plans, and keep your account secure from one polished dashboard.</p>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <Link href="/login" className="btn btn-primary">Start exploring <ArrowRight size={18} /></Link>
            <Link href="/register" className="btn btn-secondary">Create account</Link>
          </div>
        </div>
      </section>

      <section className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', marginTop: '1.5rem' }}>
        <div className="stat">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <BookOpen size={20} color="#6c7cff" />
            <strong>Curated catalog</strong>
          </div>
          <p style={{ color: 'var(--muted)', marginBottom: 0 }}>Browse categories, availability, and new arrivals in a clean experience.</p>
        </div>
        <div className="stat">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <ShieldCheck size={20} color="#23c9a4" />
            <strong>Secure auth</strong>
          </div>
          <p style={{ color: 'var(--muted)', marginBottom: 0 }}>Email verification, password reset, and protected dashboards.</p>
        </div>
      </section>
    </main>
  );
}
