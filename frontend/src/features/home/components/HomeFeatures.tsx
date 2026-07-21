import { BookOpen, ShieldCheck } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const features = [
  {
    icon: <BookOpen size={20} className="text-primary" />,
    title: 'Curated catalog',
    description: 'Browse categories, availability, and new arrivals in a clean experience.',
  },
  {
    icon: <ShieldCheck size={20} className="text-green-400" />,
    title: 'Secure auth',
    description: 'Email verification, password reset, and protected dashboards.',
  },
];

export function HomeFeatures() {
  return (
    <section className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 px-6 pb-20">
      {features.map((f) => (
        <Card key={f.title} className="border-white/10 bg-card/60 backdrop-blur-md hover:bg-card/80 transition-colors">
          <CardContent className="pt-5">
            <div className="flex items-center gap-3 mb-2">
              {f.icon}
              <strong className="text-foreground">{f.title}</strong>
            </div>
            <p className="text-muted-foreground text-sm">{f.description}</p>
          </CardContent>
        </Card>
      ))}
    </section>
  );
}
