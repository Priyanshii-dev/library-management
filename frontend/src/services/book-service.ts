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
  
  async borrowBook(bookId: number) {
    return apiClient.post<{ message: string; borrow_id: number }>('/users/book/borrow', {
      book_id: bookId
    });
  },

  async getBorrowHistory() {
    return apiClient.get<any[]>('/users/book/history');
  },

  async returnBook(borrowId: number) {
    return apiClient.post<{ message: string }>('/users/book/return', {
      borrow_id: borrowId
    });
  }
};
