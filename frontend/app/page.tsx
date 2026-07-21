import { HomeHero } from '@/features/home/components/HomeHero';
import { HomeFeatures } from '@/features/home/components/HomeFeatures';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background text-foreground flex flex-col items-center">
      <div className="w-full max-w-5xl mx-auto flex flex-col">
        <HomeHero />
        <HomeFeatures />
      </div>
    </main>
  );
}
