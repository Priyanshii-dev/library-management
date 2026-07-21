import { useEffect, useState } from 'react';
import { bookActions } from '@/actions/book-actions';
import type { BookItem } from '@/types/book';

interface UseBooksOptions {
  enabled?: boolean;
}

export function useBooks({ enabled = true }: UseBooksOptions = {}) {
  const [books, setBooks] = useState<BookItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) {
      return;
    }

    let isMounted = true;

    async function loadBooks() {
      setIsLoading(true);
      setError(null);

      try {
        const response = await bookActions.listAvailableBooks();
        if (isMounted) {
          setBooks(response.data);
        }
      } catch (err) {
        if (isMounted) {
          const message = err && typeof err === 'object' && 'message' in err
            ? String((err as { message?: string }).message)
            : 'Unable to load books';
          setError(message);
          setBooks([]);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    void loadBooks();

    return () => {
      isMounted = false;
    };
  }, [enabled]);

  return { books, isLoading, error };
}
