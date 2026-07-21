import { bookService } from '@/services/book-service';

export const bookActions = {
  listAvailableBooks() {
    return bookService.listAvailableBooks();
  },
};
