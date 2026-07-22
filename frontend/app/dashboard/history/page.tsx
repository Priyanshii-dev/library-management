'use client';

import { BookHistory } from '@/features/dashboard/components/BookHistory';

export default function HistoryPage() {
  return (
    <div className="p-4 md:p-8 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl md:text-3xl font-bold">My Borrowing History</h1>
        <p className="text-muted-foreground text-sm mt-1">Track your active and past borrowed books</p>
      </div>
      <BookHistory />
    </div>
  );
}
