import { apiClient } from '@/services/api-client';
import type { BookItem, BookListResponse } from '@/types/book';

function normalizeBooks(payload: BookListResponse): BookItem[] {
  if (Array.isArray(payload)) {
    return payload;
  }

  return payload.items ?? payload.data ?? [];
}

export const bookService = {
  async listAvailableBooks() {
    const response = await apiClient.get<BookListResponse>('/users/book/list');

    return {
      ...response,
      data: normalizeBooks(response.data),
    };
  },
};
