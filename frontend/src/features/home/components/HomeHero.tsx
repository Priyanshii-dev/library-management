import Link from 'next/link';
import { Sparkles, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export function HomeHero() {
  return (
    <section className="py-16 md:py-24 px-6">
      <div className="grid gap-6 max-w-3xl">
        <Badge variant="outline" className="w-fit gap-2 border-primary/30 text-primary bg-primary/10">
          <Sparkles size={14} />
          Modern library experience
        </Badge>

        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight tracking-tight">
          Read smarter with a beautifully crafted digital library.
        </h1>

        <p className="text-muted-foreground text-lg leading-relaxed">
          Discover books, track borrow history, manage membership plans, and keep your account secure from one polished dashboard.
        </p>

        <div className="flex gap-3 flex-wrap mt-2">
          <Button asChild size="lg">
            <Link href="/login">
              Start exploring <ArrowRight size={17} />
            </Link>
          </Button>
          <Button asChild size="lg" variant="secondary">
            <Link href="/register">Create account</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
